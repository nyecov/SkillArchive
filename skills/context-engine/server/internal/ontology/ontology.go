package ontology

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/google/uuid"
	"github.com/nyecov/context-engine/internal/registry"
	"github.com/mark3labs/mcp-go/mcp"
)

const (
	GraphFilename = "ontology.json"
	LockFilename  = ".ontology.lock"
	MaxLockTime   = 5 * time.Second
)

var HierarchicalEdges = map[string]bool{
	"REQUIRES":   true,
	"IMPLEMENTS": true,
	"DEPENDS_ON": true,
	"OWNS":       true,
}

var NonHierarchicalEdges = map[string]bool{
	"REFERENCES":     true,
	"CONFLICTS_WITH": true,
}

// Data structures mapping to JSON
type OntologyGraph struct {
	UUID        string              `json:"__uuid,omitempty"`
	Version     int                 `json:"__version"`
	LastUpdated string              `json:"last_updated"`
	Entities    map[string][]Edge   `json:"entities"`
}

type Edge struct {
	Type   string `json:"type"`
	Target string `json:"target"`
}

// ------------------------------------------------------------------
// MCP Handlers
// ------------------------------------------------------------------

func HandleCommitOntologyEdge(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}
	source, ok := args["source_entity"].(string)
	if !ok || source == "" {
		return mcp.NewToolResultError("source_entity is required"), nil
	}
	edgeType, ok := args["edge_type"].(string)
	if !ok || edgeType == "" {
		return mcp.NewToolResultError("edge_type is required"), nil
	}
	target, ok := args["target_entity"].(string)
	if !ok || target == "" {
		return mcp.NewToolResultError("target_entity is required"), nil
	}

	// Validate Edge
	isHierarchical := HierarchicalEdges[edgeType]
	if !isHierarchical && !NonHierarchicalEdges[edgeType] {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Invalid edge_type: %s", edgeType)), nil
	}

	// Lock File
	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, LockFilename)
	if err := acquireLock(lockPath); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Could not acquire lock: %v", err)), nil
	}
	defer releaseLock(lockPath)

	graphPath := filepath.Join(memDir, GraphFilename)
	graph, err := loadOntologyState(graphPath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to load graph: %v", err)), nil
	}

	// Cycle Detection for Hierarchical Edges
	if isHierarchical {
		if detectCycle(graph, source, target) {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: DAG Cycle Violation. Committing %s -> %s -> %s creates a circular dependency. Halt and review architecture. Use delete_ontology_edge if refactoring existing logic.", source, edgeType, target)), nil
		}
	}

	// Ensure Entity exists
	if _, exists := graph.Entities[source]; !exists {
		graph.Entities[source] = []Edge{}
	}
	
	// Prevent duplicate edges
	for _, e := range graph.Entities[source] {
		if e.Type == edgeType && e.Target == target {
			return mcp.NewToolResultText(fmt.Sprintf("Edge %s -> %s -> %s already exists. No mutation needed.", source, edgeType, target)), nil
		}
	}

	graph.Entities[source] = append(graph.Entities[source], Edge{
		Type:   edgeType,
		Target: target,
	})

	graph.Version++
	graph.LastUpdated = time.Now().Format(time.RFC3339)

	if err := saveOntologyState(graphPath, graph); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to save graph: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully committed %s -> %s -> %s.", source, edgeType, target)), nil
}

func HandleDeleteOntologyEdge(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}
	source, ok := args["source_entity"].(string)
	if !ok || source == "" {
		return mcp.NewToolResultError("source_entity is required"), nil
	}
	edgeType, ok := args["edge_type"].(string)
	if !ok || edgeType == "" {
		return mcp.NewToolResultError("edge_type is required"), nil
	}
	target, ok := args["target_entity"].(string)
	if !ok || target == "" {
		return mcp.NewToolResultError("target_entity is required"), nil
	}

	memDir := getMemoryDir()
	lockPath := filepath.Join(memDir, LockFilename)
	if err := acquireLock(lockPath); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Could not acquire lock: %v", err)), nil
	}
	defer releaseLock(lockPath)

	graphPath := filepath.Join(memDir, GraphFilename)
	graph, err := loadOntologyState(graphPath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to load graph: %v", err)), nil
	}

	edges, exists := graph.Entities[source]
	if !exists {
		return mcp.NewToolResultText(fmt.Sprintf("Source entity %s not found.", source)), nil
	}

	found := false
	filtered := []Edge{}
	for _, e := range edges {
		if e.Type == edgeType && e.Target == target {
			found = true
			continue // skip deleting it by not appending
		}
		filtered = append(filtered, e)
	}

	if !found {
		return mcp.NewToolResultText(fmt.Sprintf("Edge %s -> %s -> %s not found.", source, edgeType, target)), nil
	}

	graph.Entities[source] = filtered
	graph.Version++
	graph.LastUpdated = time.Now().Format(time.RFC3339)

	if err := saveOntologyState(graphPath, graph); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to save graph: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully deleted %s -> %s -> %s.", source, edgeType, target)), nil
}

func HandleReadOntologyGraph(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}
	targetEntity, ok := args["target_entity"].(string)
	if !ok || targetEntity == "" {
		return mcp.NewToolResultError("target_entity is required"), nil
	}

	memDir := getMemoryDir()
	graphPath := filepath.Join(memDir, GraphFilename)
	
	bytes, err := os.ReadFile(graphPath)
	if err != nil {
		if os.IsNotExist(err) {
			return mcp.NewToolResultText("Knowledge graph is currently empty."), nil
		}
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to read graph: %v", err)), nil
	}

	// Parse to extract specific subtree
	graph, err := loadOntologyState(graphPath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to load graph: %v", err)), nil
	}

	downstreamEdges, hasDownstream := graph.Entities[targetEntity]
	
	// Find all entities that target this entity (Upstream)
	upstreamEdges := make(map[string][]string)
	hasUpstream := false
	for sourceName, edges := range graph.Entities {
		for _, e := range edges {
			if e.Target == targetEntity {
				upstreamEdges[sourceName] = append(upstreamEdges[sourceName], e.Type)
				hasUpstream = true
			}
		}
	}

	if !hasDownstream && !hasUpstream {
		return mcp.NewToolResultText(fmt.Sprintf("Entity '%s' not found in graph. Here is the entire raw graph for context:\n\n%s", targetEntity, string(bytes))), nil
	}

	// Format specific payload
	output := fmt.Sprintf("=== Knowledge Graph Local Vector for: %s ===\n", targetEntity)
	if hasDownstream {
		output += "\nDownstream Dependencies (It relies on):\n"
		for _, e := range downstreamEdges {
			output += fmt.Sprintf("- [%s] -> %s\n", e.Type, e.Target)
		}
	}
	if hasUpstream {
		output += "\nUpstream Dependencies (Relies on it):\n"
		for source, types := range upstreamEdges {
			for _, typ := range types {
				output += fmt.Sprintf("- %s -> [%s]\n", source, typ)
			}
		}
	}
	return mcp.NewToolResultText(output), nil
}

func loadOntologyState(path string) (*OntologyGraph, error) {
	bytes, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return &OntologyGraph{
				UUID:     uuid.New().String(), // Generate on init
				Version:  0,
				Entities: make(map[string][]Edge),
			}, nil
		}
		return nil, err
	}

	var graph OntologyGraph
	if err := json.Unmarshal(bytes, &graph); err != nil {
		corruptedPath := path + time.Now().Format(".corrupted-2006-01-02-15-04-05")
		os.Rename(path, corruptedPath)
		return nil, fmt.Errorf("State format corruption detected. File quarantined to %s. Resetting state. Original error: %v", corruptedPath, err)
	}
	
	// Registry Heuristic UUID injection & Registry Tracking
	if graph.UUID == "" {
		graph.UUID = registry.GenerateUniqueUUID(path)
	} else {
		if err := registry.RegisterUUID(graph.UUID, path); err != nil {
			return nil, err
		}
	}
	if graph.Entities == nil {
		graph.Entities = make(map[string][]Edge)
	}

	return &graph, nil
}

func saveOntologyState(path string, graph *OntologyGraph) error {
	bytes, err := json.MarshalIndent(graph, "", "  ")
	if err != nil {
		return err
	}
	
	// Atomic write with Sync for TPS reliability
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

// detectCycle returns true if adding an edge from source to target creates a cycle via hierarchical edges.
// This executes a simple Depth First Search on the DAG.
func detectCycle(graph *OntologyGraph, source, target string) bool {
	// If the target *is* the source, immediate cycle.
	if source == target {
		return true
	}

	visited := make(map[string]bool)
	var dfs func(current string) bool

	dfs = func(current string) bool {
		if current == source {
			return true // We looped back to the source! Cycle detected.
		}
		if visited[current] {
			return false // Already checked this branch
		}
		visited[current] = true

		// Check all children of the current node
		for _, edge := range graph.Entities[current] {
			if HierarchicalEdges[edge.Type] {
				if dfs(edge.Target) {
					return true
				}
			}
		}
		return false
	}

	// We start the DFS from the target we are proposing to link TO.
	// If the target traces deeply back to the source, then source->target creates a cycle.
	return dfs(target)
}

// OS-Level Lock Helpers
func acquireLock(lockPath string) error {
	for i := 0; i < 60; i++ { // Try for 6 seconds total
		info, err := os.Stat(lockPath)
		if os.IsNotExist(err) {
			goto TAKE_OWNERSHIP
		}
		if err == nil {
			if time.Since(info.ModTime()) > MaxLockTime {
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

func getMemoryDir() string {
	dir := os.Getenv("MEMORY_DIR")
	if dir == "" {
		dir = "/workspace/.gemini/mem"
	}
	os.MkdirAll(dir, 0755)
	return dir
}
