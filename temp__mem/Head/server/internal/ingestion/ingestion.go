package ingestion

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/mark3labs/mcp-go/mcp"
)

// Constants for Poka-yoke strict boundaries
const (
	MaxFileSizeBytes = 5 * 1024 * 1024 // 5MB limit
	MaxReturnChars   = 16000           // Safe context window heuristic
)

// HandleIngestContext handles the business logic for the ingest_context MCP tool.
func HandleIngestContext(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	targetPath, ok := args["target_path"].(string)
	if !ok || targetPath == "" {
		return mcp.NewToolResultError("target_path is required and must be a string"), nil
	}

	// Resolve actual workspace path
	workspaceRoot := os.Getenv("WORKSPACE_ROOT")
	if workspaceRoot == "" {
		workspaceRoot = "/workspace" // Fallback to Docker default
	}

	// Clean and join paths to prevent directory traversal
	cleanPath := filepath.Clean(targetPath)
	absPath := filepath.Join(workspaceRoot, cleanPath)

	// Poka-yoke: Prevent traversal outside workspace
	// Ensure absPath truly starts with workspaceRoot to prevent ../ escapes
	if !strings.HasPrefix(absPath, workspaceRoot) {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Access Denied. Path %s attempts to traverse outside the workspace root.", targetPath)), nil
	}

	// Stat the file for the Zip-Bomb check
	info, err := os.Stat(absPath)
	if err != nil {
		if os.IsNotExist(err) {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: File not found at %s. Are you sure you are using the correct path relative to the workspace?", targetPath)), nil
		}
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Could not stat file: %v", err)), nil
	}

	if info.IsDir() {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: %s is a directory. ingest_context targets specific files only.", targetPath)), nil
	}

	if info.Size() > MaxFileSizeBytes {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Zip-Bomb Guardrail Triggered. File size (%d bytes) exceeds safe limit of 5MB.", info.Size())), nil
	}

	// Read file contents
	fileBytes, err := os.ReadFile(absPath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to read file: %v", err)), nil
	}

	content := string(fileBytes)

	// Apply Optional Query Targeting filter if provided
	queryInterFace, hasQuery := args["query"]
	if hasQuery {
		query, isStr := queryInterFace.(string)
		if isStr && query != "" {
			// Basic filtering logic: Find the query and extract a surrounding window
			content = extractQueryWindow(content, query)
		}
	}

	// Apply Strict Context Truncation Heuristic
	if len(content) > MaxReturnChars {
		truncated := content[:MaxReturnChars]
		warning := fmt.Sprintf("\n\n[WARNING: OUTPUT TRUNCATED AT %d CHARS to protect LLM context limits. File is larger than safe threshold.]", MaxReturnChars)
		return mcp.NewToolResultText(truncated + warning), nil
	}

	return mcp.NewToolResultText(content), nil
}

// extractQueryWindow finds the first instance of the query and returns a chunk of text around it
func extractQueryWindow(content, query string) string {
	index := strings.Index(strings.ToLower(content), strings.ToLower(query))
	if index == -1 {
		return fmt.Sprintf("[Query '%s' not found in file. Returning truncated file start instead.]\n\n%s", query, truncate(content, MaxReturnChars))
	}

	// We want to capture some context before and after the hit
	start := index - 2000
	if start < 0 {
		start = 0
	}

	end := index + MaxReturnChars - 2000
	if end > len(content) {
		end = len(content)
	}

	return fmt.Sprintf("[Query '%s' found. Returning targeted chunk.]\n\n%s", query, content[start:end])
}

func truncate(s string, limit int) string {
	if len(s) > limit {
		return s[:limit]
	}
	return s
}
