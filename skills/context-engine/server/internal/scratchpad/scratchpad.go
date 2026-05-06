package scratchpad

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/nyecov/context-engine/internal/registry"
	"github.com/nyecov/context-engine/internal/storage"
)

const (
	SoftLimitChars = 8000
	HardLimitChars = 10000
)

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

// ensureDB ensures the database is initialized
func ensureDB() (*sql.DB, error) {
	db := storage.GetDB()
	if db == nil {
		d, err := storage.InitDB()
		if err != nil {
			return nil, err
		}
		return d, nil
	}
	return db, nil
}

// buildCurrentState queries the DB and builds the legacy compatible SessionState struct.
// This is necessary because the LLM context limits depend on the serialized byte length.
func buildCurrentState(ctx context.Context, db *sql.DB) (*SessionState, error) {
	state := &SessionState{
		UUID:        registry.GenerateUniqueUUID("scratchpad-sqlite"),
		Version:     1,
		LastUpdated: time.Now().Format(time.RFC3339),
		Findings:    []SessionEntry{},
	}

	query := `SELECT content, phase, created_at FROM scratchpad_findings ORDER BY id ASC`
	rows, err := db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var content, phase, createdAt string
		if err := rows.Scan(&content, &phase, &createdAt); err == nil {
			state.Findings = append(state.Findings, SessionEntry{
				Timestamp: createdAt,
				Phase:     phase,
				Finding:   content,
			})
			state.ActivePhase = phase
		}
	}
	return state, nil
}

// ------------------------------------------------------------------
// MCP Handlers
// ------------------------------------------------------------------

func HandleLogSessionFinding(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

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

	// Calculate state length before allowing insert to enforce Jidoka Hard Limit
	currentState, err := buildCurrentState(ctx, db)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to build state: %v", err)), nil
	}

	// Temporarily simulate the addition to check bounds
	simulatedState := *currentState
	simulatedState.Findings = append(simulatedState.Findings, SessionEntry{
		Timestamp: time.Now().Format(time.RFC3339),
		Phase:     phase,
		Finding:   findingText,
	})

	bytes, _ := json.MarshalIndent(simulatedState, "", "  ")

	if len(bytes) > HardLimitChars {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: HARD LIMIT BREACHED. The session state is over %d characters. You must use native workflow pruning to summarize the scratchpad before writing new findings.", HardLimitChars)), nil
	}

	// Insert new finding
	query := `INSERT INTO scratchpad_findings (content, phase, created_at) VALUES (?, ?, ?)`
	timestamp := time.Now().Format(time.RFC3339)
	if _, err := db.ExecContext(ctx, query, findingText, phase, timestamp); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Database insert failed: %v", err)), nil
	}

	// Check Soft Limit for warning payload
	successMessage := "Successfully logged finding."
	if len(bytes) > SoftLimitChars {
		successMessage += fmt.Sprintf("\n\n[WARNING: SCRATCHPAD SOFT LIMIT REACHED (%d/%d chars). Prune before hitting hard limit.]", len(bytes), HardLimitChars)
	}

	return mcp.NewToolResultText(successMessage), nil
}

func HandleReadSessionState(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	state, err := buildCurrentState(ctx, db)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to fetch state: %v", err)), nil
	}

	if len(state.Findings) == 0 {
		return mcp.NewToolResultText("Session state is currently empty."), nil
	}

	bytes, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to serialize state: %v", err)), nil
	}

	return mcp.NewToolResultText(string(bytes)), nil
}

func HandleDeleteSessionFinding(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	findingIndex, ok := args["index"].(float64)
	if !ok {
		return mcp.NewToolResultError("index (0-based) is required and must be a number"), nil
	}

	idx := int(findingIndex)
	if idx < 0 {
		return mcp.NewToolResultError("ToolError: Index must be non-negative"), nil
	}

	// SQLite doesn't natively support DELETE with LIMIT/OFFSET without compiling with specific flags.
	// We'll subquery the ID based on sorting and offset.
	query := `DELETE FROM scratchpad_findings WHERE id = (
		SELECT id FROM scratchpad_findings ORDER BY id ASC LIMIT 1 OFFSET ?
	)`

	res, err := db.ExecContext(ctx, query, idx)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Database delete failed: %v", err)), nil
	}

	rowsAffected, _ := res.RowsAffected()
	if rowsAffected == 0 {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Index %d out of bounds.", idx)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully deleted finding at index %d.", idx)), nil
}

func HandleClearSessionState(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	query := `DELETE FROM scratchpad_findings`
	if _, err := db.ExecContext(ctx, query); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to clear state: %v", err)), nil
	}

	// Reset sequences so ID starts at 1 again
	db.ExecContext(ctx, `DELETE FROM sqlite_sequence WHERE name='scratchpad_findings'`)

	return mcp.NewToolResultText("Session state successfully cleared."), nil
}
