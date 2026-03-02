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
// It uses a heartbeat mechanism to allow safe takeovers after crashes.
func AcquireSingletonLock() error {
	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, SingletonLockFile)

	for i := 0; i < 3; i++ {
		info, err := os.Stat(lockPath)
		if os.IsNotExist(err) {
			break
		}

		if err == nil {
			// Check for stale lock (Forensic takeover)
			if time.Since(info.ModTime()) > StaleTimeout {
				fmt.Fprintf(os.Stderr, "[STALE LOCK DETECTED] Previous instance timed out. Seizing ownership...\n")
				os.Remove(lockPath)
				break
			}
		}

		if i == 2 {
			return fmt.Errorf("SINGLETON VIOLATION: Another instance of the Context Engine is already active on this volume. Halt and review 'docker ps'.")
		}
		
		fmt.Fprintf(os.Stderr, "Singleton check... (Lock exists and is fresh)\n")
		time.Sleep(2 * time.Second)
	}

	// Create/Touch the lock
	if err := touchLock(lockPath); err != nil {
		return err
	}

	// Start Heartbeat in background
	go startHeartbeat(lockPath)

	return nil
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

	for range ticker.C {
		// Just touch the file to update ModTime
		if err := os.Chtimes(path, time.Now(), time.Now()); err != nil {
			fmt.Fprintf(os.Stderr, "[HEARTBEAT ERROR] Failed to update singleton lock: %v\n", err)
		}
	}
}
