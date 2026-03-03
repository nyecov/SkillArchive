package pokayoke

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/gofrs/flock"
)

const (
	SingletonLockFile = ".engine.instance.lock"
)

var fileLock *flock.Flock

// AcquireSingletonLock ensures only one instance of the engine is active
// on the shared memory volume. It uses a cross-platform POSIX file lock
// which the OS automatically releases if the container crashes or dies,
// eliminating the stale lock problem while enforcing cross-container safety.
func AcquireSingletonLock() error {
	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, SingletonLockFile)

	fileLock = flock.New(lockPath)

	locked, err := fileLock.TryLock()
	if err != nil {
		fmt.Fprintf(os.Stderr, "[SINGLETON] Error attempting to acquire lock: %v\n", err)
		return fmt.Errorf("FATAL: Failed to check lock status: %v", err)
	}

	if !locked {
		fmt.Fprintf(os.Stderr, "[SINGLETON] Lock is currently held by another process or container.\n")
		return fmt.Errorf("FATAL: Context Engine is already running (Volume lock active)")
	}

	fmt.Fprintf(os.Stderr, "[SINGLETON] File lock acquired on %s.\n", lockPath)
	return nil
}

// ReleaseSingletonLock manually releases the file lock.
func ReleaseSingletonLock() {
	if fileLock != nil {
		fileLock.Unlock()
		fmt.Fprintf(os.Stderr, "[SINGLETON] Lock released.\n")
	}
}
