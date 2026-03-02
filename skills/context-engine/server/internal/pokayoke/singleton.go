package pokayoke

import (
	"fmt"
	"os"
	"path/filepath"
	"time"
)

const (
	SingletonLockFile = ".engine.instance.lock"
	HeartbeatInterval = 5 * time.Second
	StaleTimeout      = 15 * time.Second
)

// AcquireSingletonLock ensures only one instance of the engine is active.
// It uses a resilient "Check-Wait-Seize" mechanism to resolve lockouts.
func AcquireSingletonLock() error {
	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, SingletonLockFile)

	// Attempt immediate acquisition
	if acquired, err := attemptAcquire(lockPath); acquired {
		return nil
	} else if err != nil {
		return err
	}

	fmt.Fprintf(os.Stderr, "[SINGLETON] Lock is currently held by another instance. Waiting 15s for autonomous release...\n")

	timeout := time.After(StaleTimeout)
	tick := time.NewTicker(2 * time.Second)
	defer tick.Stop()

	for {
		select {
		case <-timeout:
			fmt.Fprintf(os.Stderr, "[SINGLETON] Timeout reached. Seizing ownership from conflicting instance (Jidoka Restart).\n")
			// Forced removal to break stale handles
			os.Remove(lockPath)
			if err := touchLock(lockPath); err != nil {
				return fmt.Errorf("FATAL: Failed to seize singleton lock after timeout: %v", err)
			}
			go startHeartbeat(lockPath)
			return nil

		case <-tick.C:
			fmt.Fprintf(os.Stderr, "Singleton check... (Lock exists and is fresh)\n")
			if acquired, _ := attemptAcquire(lockPath); acquired {
				fmt.Fprintf(os.Stderr, "[SINGLETON] Lock acquired during wait cycle.\n")
				return nil
			}
		}
	}
}

// attemptAcquire tries to create the lock file atomically.
func attemptAcquire(path string) (bool, error) {
	// Check if stale before even trying EXCL to avoid unnecessary errors
	if info, err := os.Stat(path); err == nil {
		if time.Since(info.ModTime()) > StaleTimeout {
			fmt.Fprintf(os.Stderr, "[STALE LOCK DETECTED] Previous instance timed out. Seizing ownership...\n")
			os.Remove(path)
		} else {
			return false, nil
		}
	}

	f, err := os.OpenFile(path, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0644)
	if err != nil {
		if os.IsExist(err) {
			return false, nil
		}
		return false, err
	}
	f.Close()
	go startHeartbeat(path)
	return true, nil
}

// ReleaseSingletonLock manually removes the lock (used during graceful shutdown).
func ReleaseSingletonLock() {
	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, SingletonLockFile)
	os.Remove(lockPath)
}

func touchLock(path string) error {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
	if err != nil {
		return err
	}
	f.Close()
	return nil
}

func startHeartbeat(path string) {
	ticker := time.NewTicker(HeartbeatInterval)
	defer ticker.Stop()

	// Initial ModTime for identity check
	info, _ := os.Stat(path)
	lastMod := info.ModTime()

	for range ticker.C {
		// Poka-yoke: Check if our lock was seized or deleted
		currentInfo, err := os.Stat(path)
		if err != nil || !currentInfo.ModTime().Equal(lastMod) {
			fmt.Fprintf(os.Stderr, "[JIDOKA HALT] Singleton lock lost or seized. Self-terminating to prevent collision.\n")
			os.Exit(1)
		}

		// Update ModTime to signal we are alive
		now := time.Now()
		if err := os.Chtimes(path, now, now); err != nil {
			fmt.Fprintf(os.Stderr, "[HEARTBEAT ERROR] Failed to update singleton lock: %v\n", err)
		}
		lastMod = now
	}
}
