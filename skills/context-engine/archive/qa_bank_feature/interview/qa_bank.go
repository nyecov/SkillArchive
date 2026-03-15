package interview

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/nyecov/context-engine/internal/storage"
)

const (
	MaxReturnChars = 16000 // Safe context window heuristic
)

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

// HandleAppendInterviewQA handles the logic for appending a TOON-formatted Q&A pair.
func HandleAppendInterviewQA(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	qaPair, ok := args["toon_qa_pair"].(string)
	if !ok || qaPair == "" {
		return mcp.NewToolResultError("toon_qa_pair is required and must be a string"), nil
	}

	// Validate basic TOON structure (simple heuristic)
	if !strings.Contains(qaPair, "[Q:") || !strings.Contains(qaPair, "[A:") {
		return mcp.NewToolResultError("ToolError: Invalid TOON format. Expected [Q: ...] and [A: ...] tags."), nil
	}

	// Ensure the string ends with a newline
	if !strings.HasSuffix(qaPair, "\n") {
		qaPair += "\n"
	}

	timestamp := time.Now().Format(time.RFC3339)
	entry := fmt.Sprintf("\n[META: Timestamp: %s]\n%s", timestamp, qaPair)

	query := `INSERT INTO interview_qa (toon_pair, created_at) VALUES (?, ?)`
	if _, err := db.ExecContext(ctx, query, entry, timestamp); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to insert Q&A pair: %v", err)), nil
	}

	return mcp.NewToolResultText("Successfully appended Q&A pair to the Interview memory bank."), nil
}

// HandleRetrieveInterviewPatterns retrieves relevant Q&A pairs.
func HandleRetrieveInterviewPatterns(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	queryParam, ok := args["query"].(string)
	if !ok {
		queryParam = "" // Optional query
	}

	// Build exact query - retrieve earliest to latest so narrative reads chronologically
	// But in DB, it's easier to retrieve what we want. We'll select all matching and stop when we exceed MaxReturnChars.
	var rows *sql.Rows
	if queryParam != "" {
		dbQuery := `SELECT toon_pair FROM interview_qa WHERE toon_pair LIKE ? ORDER BY id ASC`
		searchStr := "%" + queryParam + "%"
		rows, err = db.QueryContext(ctx, dbQuery, searchStr)
	} else {
		dbQuery := `SELECT toon_pair FROM interview_qa ORDER BY id DESC LIMIT 50`
		rows, err = db.QueryContext(ctx, dbQuery)
	}

	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to read QA bank: %v", err)), nil
	}
	defer rows.Close()

	var resultBuilder strings.Builder
	var blocks []string

	for rows.Next() {
		var content string
		if err := rows.Scan(&content); err == nil {
			blocks = append(blocks, content)
		}
	}

	// If it was a generic query (no params), we fetched DESC to get the newest, but we should reverse it to read chronologically
	if queryParam == "" {
		for i, j := 0, len(blocks)-1; i < j; i, j = i+1, j-1 {
			blocks[i], blocks[j] = blocks[j], blocks[i]
		}
	}

	for _, block := range blocks {
		if resultBuilder.Len()+len(block) > MaxReturnChars {
			resultBuilder.WriteString(fmt.Sprintf("\n\n[WARNING: TRUNCATED AT %d CHARS to protect context limits. Please refine your query.]\n", MaxReturnChars))
			break
		}
		resultBuilder.WriteString(block)
	}

	result := resultBuilder.String()
	if result == "" {
		if queryParam != "" {
			return mcp.NewToolResultText(fmt.Sprintf("No Q&A pairs found matching query: '%s'", queryParam)), nil
		}
		return mcp.NewToolResultText("Interview QA bank is currently empty."), nil
	}

	return mcp.NewToolResultText(result), nil
}

// HandlePruneInterviewQA allows manual deletion of entries based on date or keyword.
func HandlePruneInterviewQA(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	beforeDateStr, _ := args["before_date"].(string)
	queryParam, _ := args["query"].(string)

	if beforeDateStr == "" && queryParam == "" {
		return mcp.NewToolResultError("ToolError: You must provide either 'before_date' or 'query' to prune."), nil
	}

	var conditions []string
	var vals []interface{}

	if beforeDateStr != "" {
		_, err := time.Parse(time.RFC3339, beforeDateStr)
		if err != nil {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: Invalid date format. Use RFC3339 (e.g., 2026-03-01T00:00:00Z). Error: %v", err)), nil
		}
		conditions = append(conditions, `created_at < ?`)
		vals = append(vals, beforeDateStr)
	}

	if queryParam != "" {
		conditions = append(conditions, `toon_pair LIKE ?`)
		vals = append(vals, "%"+queryParam+"%")
	}

	whereClause := strings.Join(conditions, " OR ")
	deleteQuery := fmt.Sprintf(`DELETE FROM interview_qa WHERE %s`, whereClause)

	res, err := db.ExecContext(ctx, deleteQuery, vals...)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Database delete failed: %v", err)), nil
	}

	rowsAffected, _ := res.RowsAffected()

	// Get remaining count
	var remainingCount int
	db.QueryRowContext(ctx, `SELECT COUNT(*) FROM interview_qa`).Scan(&remainingCount)

	return mcp.NewToolResultText(fmt.Sprintf("Pruning complete. Removed %d entries. %d entries remain in the Memory Bank.", rowsAffected, remainingCount)), nil
}
