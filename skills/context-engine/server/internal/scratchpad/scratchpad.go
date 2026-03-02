package scratchpad

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/nyecov/context-engine/internal/registry"
	"github.com/mark3labs/mcp-go/mcp"
)

const (
	SessionFilename       = "current_session.json"
	LockFilename          = ".current_session.lock"
	MaxLockDuration       = 5 * time.Second
	SoftLimitChars        = 8000
	HardLimitChars        = 10000
)

var mu sync.Mutex

type SessionEntry struct {
	Timestamp string `json:"timestamp"`
	Phase     string `json:"phase"`
	Finding   string `json:"finding"`
}

type SessionState struct {
	UUID        string         `json:"__uuid,omitempty"`
	Version     int            `json:"__version"`
	LastUpdated string         `json:"last_updated"`
	ActivePhase string         `json:"active_phase"`
	Findings    []SessionEntry `json:"findings"`
}

// ------------------------------------------------------------------
// MCP Handlers
// ------------------------------------------------------------------

func HandleLogSessionFinding(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	findingText, ok := args["finding_text"].(string)
	if !ok || findingText == "" {
		return mcp.NewToolResultError("finding_text is required and must be a string"), nil
	}

	phase, ok := args["phase"].(string)
	if !ok || phase == "" {
		return mcp.NewToolResultError("phase is required and must be one of: planning, execution, verification, blocked"), nil
	}

	// Wait for and acquire lock
	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, LockFilename)
	if err := acquireLock(lockPath); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Could not acquire file lock: %v", err)), nil
	}
	defer releaseLock(lockPath)

	statePath := filepath.Join(memDir, SessionFilename)
	state, err := loadSessionState(statePath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to load session state: %v", err)), nil
	}

	// Append the new finding
	state.Findings = append(state.Findings, SessionEntry{
		Timestamp: time.Now().Format(time.RFC3339),
		Phase:     phase,
		Finding:   findingText,
	})

	state.Version++
	state.LastUpdated = time.Now().Format(time.RFC3339)
	state.ActivePhase = phase

	// Serialize and Check Hard Limit
	bytes, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to serialize state: %v", err)), nil
	}

	if len(bytes) > HardLimitChars {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: HARD LIMIT BREACHED. The session state is over %d characters. You must use native workflow pruning to summarize the scratchpad before writing new findings.", HardLimitChars)), nil
	}

	if err := saveSessionState(statePath, state); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to finalize state: %v", err)), nil
	}

	// Check Soft Limit for warning payload
	successMessage := "Successfully logged finding."
	if len(bytes) > SoftLimitChars {
		successMessage += fmt.Sprintf("\n\n[WARNING: SCRATCHPAD SOFT LIMIT REACHED (%d/%d chars). Prune before hitting hard limit.]", len(bytes), HardLimitChars)
	}

	return mcp.NewToolResultText(successMessage), nil
}

func HandleReadSessionState(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	memDir := getMemoryDir()
	statePath := filepath.Join(memDir, SessionFilename)
	
	bytes, err := os.ReadFile(statePath)
	if err != nil {
		if os.IsNotExist(err) {
			return mcp.NewToolResultText("Session state is currently empty."), nil
		}
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to read session state: %v", err)), nil
	}

	return mcp.NewToolResultText(string(bytes)), nil
}

func HandleDeleteSessionFinding(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	findingIndex, ok := args["index"].(float64)
	if !ok {
		return mcp.NewToolResultError("index (0-based) is required and must be a number"), nil
	}

	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, LockFilename)
	if err := acquireLock(lockPath); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Could not acquire lock: %v", err)), nil
	}
	defer releaseLock(lockPath)

	statePath := filepath.Join(memDir, SessionFilename)
	state, err := loadSessionState(statePath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to load state: %v", err)), nil
	}

	idx := int(findingIndex)
	if idx < 0 || idx >= len(state.Findings) {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Index %d out of bounds (0-%d)", idx, len(state.Findings)-1)), nil
	}

	// Remove finding
	state.Findings = append(state.Findings[:idx], state.Findings[idx+1:]...)
	state.Version++
	state.LastUpdated = time.Now().Format(time.RFC3339)

	if err := saveSessionState(statePath, state); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to save state: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully deleted finding at index %d.", idx)), nil
}

func HandleClearSessionState(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, LockFilename)
	if err := acquireLock(lockPath); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Could not acquire lock: %v", err)), nil
	}
	defer releaseLock(lockPath)

	statePath := filepath.Join(memDir, SessionFilename)
	// Atomic reset
	state := &SessionState{
		UUID:        registry.GenerateUniqueUUID(statePath),
		Version:     0,
		LastUpdated: time.Now().Format(time.RFC3339),
		Findings:    []SessionEntry{},
	}

	if err := saveSessionState(statePath, state); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to clear state: %v", err)), nil
	}

	return mcp.NewToolResultText("Session state successfully cleared."), nil
}

func saveSessionState(path string, state *SessionState) error {
	bytes, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return err
	}

	tmpPath := path + ".tmp"
	f, err := os.OpenFile(tmpPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return err
	}
	defer f.Close()

	if _, err := f.Write(bytes); err != nil {
		return err
	}
	if err := f.Sync(); err != nil {
		return err
	}
	f.Close()

	return os.Rename(tmpPath, path)
}

// ------------------------------------------------------------------
// Internal Helpers
// ------------------------------------------------------------------

func getMemoryDir() string {
	dir := os.Getenv("MEMORY_DIR")
	if dir == "" {
		dir = "/workspace/.gemini/mem"
	}
	// Ensure directory exists
	os.MkdirAll(dir, 0755)
	return dir
}

func loadSessionState(path string) (*SessionState, error) {
	bytes, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			// Return blank initialized state with a new unique UUID (Provenance Heuristic)
			return &SessionState{
				UUID:     registry.GenerateUniqueUUID(path),
				Version:  0,
				Findings: []SessionEntry{},
			}, nil
		}
		return nil, err
	}

	var state SessionState
	if err := json.Unmarshal(bytes, &state); err != nil {
		// State Corruption Guardrail: Rename file and reset
		corruptedPath := path + time.Now().Format(".corrupted-2006-01-02-15-04-05")
		os.Rename(path, corruptedPath)
		return nil, fmt.Errorf("State format corruption detected. File quarantined to %s. Resetting state. Original error: %v", corruptedPath, err)
	}

	// Registry Injection/Verification
	if state.UUID == "" {
		state.UUID = registry.GenerateUniqueUUID(path)
	} else {
		if err := registry.RegisterUUID(state.UUID, path); err != nil {
			return nil, err // Collision or conflict
		}
	}

	return &state, nil
}

// acquireLock implements the deterministic Timeout Heuristic
func acquireLock(lockPath string) error {
	for i := 0; i < 60; i++ { // Try for 6 seconds total
		info, err := os.Stat(lockPath)
		if os.IsNotExist(err) {
			goto TAKE_OWNERSHIP
		}
		
		if err == nil {
			if time.Since(info.ModTime()) > MaxLockDuration {
				os.Remove(lockPath)
				goto TAKE_OWNERSHIP
			}
		}
		time.Sleep(100 * time.Millisecond)
	}

TAKE_OWNERSHIP:
	file, err := os.OpenFile(lockPath, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0666)
	if err != nil {
		return fmt.Errorf("Could not write lock file. Unresolved concurrent access.")
	}
	file.Close()
	return nil
}

func releaseLock(lockPath string) {
	os.Remove(lockPath)
}
