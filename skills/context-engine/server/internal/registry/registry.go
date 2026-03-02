package registry

import (
	"fmt"
	"path/filepath"
	"sync"

	"github.com/google/uuid"
)

var (
	// uuidMap tracks active UUIDs to physical file paths to guarantee O(1) collision detection.
	uuidMap = make(map[string]string)
	mu      sync.RWMutex
)

// RegisterUUID confirms a UUID belongs to an active memory file.
func RegisterUUID(id, path string) error {
	mu.Lock()
	defer mu.Unlock()

	if id == "" {
		return fmt.Errorf("RegistryError: Cannot register empty UUID")
	}

	cleanPath := filepath.Clean(path)
	if existingPath, exists := uuidMap[id]; exists && existingPath != cleanPath {
		return fmt.Errorf("RegistryError: UUID Collision! ID %s is already claimed by %s", id, existingPath)
	}

	uuidMap[id] = cleanPath
	return nil
}

// GenerateUniqueUUID produces a new UUIDv4 and verifies O(1) uniqueness against the map.
func GenerateUniqueUUID(path string) string {
	mu.Lock()
	defer mu.Unlock()

	for {
		newID := uuid.New().String()
		if _, exists := uuidMap[newID]; !exists {
			uuidMap[newID] = filepath.Clean(path)
			return newID
		}
		// If collision (astronomically rare), loop continues
	}
}

// ClearRegistry resets the map (used primarily for test cleanup).
func ClearRegistry() {
	mu.Lock()
	defer mu.Unlock()
	uuidMap = make(map[string]string)
}
