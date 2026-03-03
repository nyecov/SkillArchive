package pokayoke

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/gofrs/flock"
	"github.com/nyecov/context-engine/internal/config"
)

const (
	SingletonLockFile  = ".engine.instance.lock"
	HeartbeatInterval  = 3 * time.Second
	StaleLockThreshold = 15 * time.Second
)

var fileLock *flock.Flock

// AcquireSingletonLock uses a Check-Wait-Seize heuristic.
// It tries to acquire the flock. If it fails, it waits up to StaleLockThreshold
// to see if the existing lock's ModTime stops updating (indicating a crashed container).
// If the lock is stale, it seizes it by breaking the file.
func AcquireSingletonLock() error {
	memDir := config.GetMemoryDir()
	lockPath := filepath.Join(memDir, SingletonLockFile)

	// Create memDir if it doesn't exist just in case
	if err := os.MkdirAll(memDir, 0755); err != nil {
		return fmt.Errorf("failed to create memory directory: %v", err)
	}

	for attempt := 0; attempt < 15; attempt++ {
		fileLock = flock.New(lockPath)
		locked, err := fileLock.TryLock()
		if err != nil {
			fmt.Fprintf(os.Stderr, "[SINGLETON] Error checking lock: %v\n", err)
		} else if locked {
			fmt.Fprintf(os.Stderr, "[SINGLETON] Lock acquired on %s.\n", lockPath)
			return nil
		}

		// Look at the file's ModTime to see if it's stale
		info, err := os.Stat(lockPath)
		if err == nil {
			if time.Since(info.ModTime()) > StaleLockThreshold {
				fmt.Fprintf(os.Stderr, "[SINGLETON] Found STALE lock (last touched %v ago). Seizing...\n", time.Since(info.ModTime()))
				// Break the lock by removing it
				os.Remove(lockPath)
				continue // Retry instantly
			}
		}

		fmt.Fprintf(os.Stderr, "[SINGLETON] Lock held by another active process. Waiting... (Attempt %d/15)\n", attempt+1)
		time.Sleep(1 * time.Second)
	}

	return fmt.Errorf("FATAL: Context Engine is already running and active (Staleness timeout exceeded)")
}

// StartHeartbeat continuously updates the lock file's ModTime to prove this instance is alive.
// If it fails to update 3 times in a row, it signals shutdown via the returned channel
// instead of calling os.Exit, allowing the main goroutine to clean up properly.
func StartHeartbeat(ctx context.Context) <-chan struct{} {
	shutdownCh := make(chan struct{})
	memDir := config.GetMemoryDir()
	lockPath := filepath.Join(memDir, SingletonLockFile)

	go func() {
		ticker := time.NewTicker(HeartbeatInterval)
		defer ticker.Stop()

		failCount := 0

		for {
			select {
			case <-ctx.Done():
				return
			case <-ticker.C:
				// "Touch" the file by updating its access/mod times
				now := time.Now()
				err := os.Chtimes(lockPath, now, now)
				if err != nil {
					failCount++
					fmt.Fprintf(os.Stderr, "[SINGLETON-HEARTBEAT] Warn: Failed to touch lock file: %v\n", err)
					if failCount >= 3 {
						// We lost the lock or the mount died. Signal shutdown to protect Ontology integrity.
						fmt.Fprintf(os.Stderr, "[SINGLETON-HEARTBEAT] FATAL: Lost access to lock file after 3 retries. Signaling graceful shutdown.\n")
						close(shutdownCh)
						return
					}
				} else {
					failCount = 0 // Reset on success
				}
			}
		}
	}()

	return shutdownCh
}

// ReleaseSingletonLock manually releases the file lock.
func ReleaseSingletonLock() {
	if fileLock != nil {
		fileLock.Unlock()
		// Clean up the file to be a good citizen
		memDir := config.GetMemoryDir()
		lockPath := filepath.Join(memDir, SingletonLockFile)
		os.Remove(lockPath)
		fmt.Fprintf(os.Stderr, "[SINGLETON] Lock released.\n")
	}
}
