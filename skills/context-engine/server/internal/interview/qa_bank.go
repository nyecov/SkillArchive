package interview

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
)

const (
	QABankFilename = "interview_qa_bank.toon"
	MaxReturnChars = 16000 // Safe context window heuristic
)

var mu sync.Mutex

// HandleAppendInterviewQA handles the logic for appending a TOON-formatted Q&A pair.
func HandleAppendInterviewQA(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

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

	// Ensure the string ends with a newline for clean appends
	if !strings.HasSuffix(qaPair, "\n") {
		qaPair += "\n"
	}

	// Add timestamp block for context
	timestamp := time.Now().Format(time.RFC3339)
	entry := fmt.Sprintf("\n[META: Timestamp: %s]\n%s", timestamp, qaPair)

	memDir := getMemoryDir()
	bankPath := filepath.Join(memDir, QABankFilename)

	// Append to file
	f, err := os.OpenFile(bankPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to open QA bank: %v", err)), nil
	}
	defer f.Close()

	if _, err := f.WriteString(entry); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to write to QA bank: %v", err)), nil
	}
	
	// Ensure it hits the disk for cross-container consistency
	if err := f.Sync(); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to sync QA bank to disk: %v", err)), nil
	}

	return mcp.NewToolResultText("Successfully appended Q&A pair to the Interview memory bank."), nil
}

// HandleRetrieveInterviewPatterns retrieves relevant Q&A pairs from the TOON file.
func HandleRetrieveInterviewPatterns(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	query, ok := args["query"].(string)
	if !ok {
		query = "" // Optional query
	}

	memDir := getMemoryDir()
	bankPath := filepath.Join(memDir, QABankFilename)

	file, err := os.Open(bankPath)
	if err != nil {
		if os.IsNotExist(err) {
			return mcp.NewToolResultText("Interview QA bank is currently empty."), nil
		}
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to read QA bank: %v", err)), nil
	}
	defer file.Close()

	var resultBuilder strings.Builder
	scanner := bufio.NewScanner(file)
	
	// Optional: Increase scanner buffer size if TOON blocks get extremely large
	// buf := make([]byte, 0, 64*1024)
	// scanner.Buffer(buf, 1024*1024)

	var currentBlock strings.Builder
	inBlock := false
	matchFoundInBlock := false

	queryLower := strings.ToLower(query)

	for scanner.Scan() {
		line := scanner.Text()

		// TOON Block start heuristic (Timestamp meta tag starts a new entry)
		if strings.HasPrefix(line, "[META: Timestamp:") {
			// Process previous block
			if inBlock {
				if query == "" || matchFoundInBlock {
					// Check length before appending
					if resultBuilder.Len()+currentBlock.Len() > MaxReturnChars {
						resultBuilder.WriteString(fmt.Sprintf("\n\n[WARNING: TRUNCATED AT %d CHARS to protect context limits. Please refine your query.]\n", MaxReturnChars))
						break // Stop scanning
					}
					resultBuilder.WriteString(currentBlock.String())
				}
			}
			
			// Reset for new block
			currentBlock.Reset()
			inBlock = true
			matchFoundInBlock = false
		}

		if inBlock {
			currentBlock.WriteString(line + "\n")
			if query != "" && strings.Contains(strings.ToLower(line), queryLower) {
				matchFoundInBlock = true
			}
		}
	}

	if err := scanner.Err(); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Error parsing QA bank: %v", err)), nil
	}

	// Process the final block
	if inBlock && (query == "" || matchFoundInBlock) {
		if resultBuilder.Len()+currentBlock.Len() <= MaxReturnChars {
			resultBuilder.WriteString(currentBlock.String())
		} else {
			resultBuilder.WriteString(fmt.Sprintf("\n\n[WARNING: TRUNCATED AT %d CHARS to protect context limits. Please refine your query.]\n", MaxReturnChars))
		}
	}

	result := resultBuilder.String()
	if result == "" {
		return mcp.NewToolResultText(fmt.Sprintf("No Q&A pairs found matching query: '%s'", query)), nil
	}

	return mcp.NewToolResultText(result), nil
}

// HandlePruneInterviewQA allows manual deletion of entries based on date or keyword.
func HandlePruneInterviewQA(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}

	beforeDateStr, _ := args["before_date"].(string)
	query, _ := args["query"].(string)

	if beforeDateStr == "" && query == "" {
		return mcp.NewToolResultError("ToolError: You must provide either 'before_date' or 'query' to prune."), nil
	}

	var cutoff time.Time
	var err error
	if beforeDateStr != "" {
		cutoff, err = time.Parse(time.RFC3339, beforeDateStr)
		if err != nil {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: Invalid date format. Use RFC3339 (e.g., 2026-03-01T00:00:00Z). Error: %v", err)), nil
		}
	}

	memDir := getMemoryDir()
	bankPath := filepath.Join(memDir, QABankFilename)
	tempPath := bankPath + ".tmp"

	// Acquire POSIX cross-container lock (reuse logic from pokayoke via main process context)
	// Note: We don't call AcquireSingletonLock here because the server process already holds it.
	
	file, err := os.Open(bankPath)
	if err != nil {
		if os.IsNotExist(err) {
			return mcp.NewToolResultText("QA Bank is already empty."), nil
		}
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to open bank for pruning: %v", err)), nil
	}
	defer file.Close()

	tempFile, err := os.Create(tempPath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to create temp file: %v", err)), nil
	}
	defer tempFile.Close()

	scanner := bufio.NewScanner(file)
	writer := bufio.NewWriter(tempFile)
	
	var currentBlock []string
	prunedCount := 0
	keptCount := 0
	
	flushBlock := func() error {
		if len(currentBlock) == 0 {
			return nil
		}
		
		blockText := strings.Join(currentBlock, "\n") + "\n"
		shouldPrune := false
		
		// 1. Check Date
		if !cutoff.IsZero() {
			for _, line := range currentBlock {
				if strings.HasPrefix(line, "[META: Timestamp:") {
					tsStr := strings.TrimSuffix(strings.TrimPrefix(line, "[META: Timestamp: "), "]")
					ts, err := time.Parse(time.RFC3339, tsStr)
					if err == nil && ts.Before(cutoff) {
						shouldPrune = true
						break
					}
				}
			}
		}
		
		// 2. Check Query
		if !shouldPrune && query != "" {
			if strings.Contains(strings.ToLower(blockText), strings.ToLower(query)) {
				shouldPrune = true
			}
		}
		
		if shouldPrune {
			prunedCount++
		} else {
			keptCount++
			if _, err := writer.WriteString(blockText); err != nil {
				return err
			}
		}
		return nil
	}

	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "[META: Timestamp:") {
			if err := flushBlock(); err != nil {
				return mcp.NewToolResultError(fmt.Sprintf("ToolError: Write failure: %v", err)), nil
			}
			currentBlock = []string{line}
		} else {
			currentBlock = append(currentBlock, line)
		}
	}
	// Final block
	if err := flushBlock(); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Write failure: %v", err)), nil
	}

	writer.Flush()
	tempFile.Close()
	file.Close()

	// Atomic Switch
	if err := os.Rename(tempPath, bankPath); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Atomic swap failed: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Pruning complete. Removed %d entries. %d entries remain in the Memory Bank.", prunedCount, keptCount)), nil
}

func getMemoryDir() string {
	dir := os.Getenv("MEMORY_DIR")
	if dir == "" {
		dir = "/workspace/.gemini/mem"
	}
	// Ensure directory exists
	os.MkdirAll(dir, 0755)
	return dir
}
