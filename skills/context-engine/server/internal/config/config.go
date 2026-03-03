package config

import "os"

// GetMemoryDir resolves the memory volume path.
// Single source of truth — replaces 4 duplicate copies across packages.
func GetMemoryDir() string {
	dir := os.Getenv("MEMORY_DIR")
	if dir == "" {
		dir = "/workspace/.gemini/mem"
	}
	os.MkdirAll(dir, 0755)
	return dir
}
