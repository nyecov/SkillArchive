package ontology

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/google/uuid"
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/nyecov/context-engine/internal/registry"
)

const (
	GraphFilename = "ontology.json"
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

var (
	mu       sync.RWMutex
	initOnce sync.Once
	initErr  error
)

// Data structures mapping to JSON
type OntologyGraph struct {
	UUID        string            `json:"__uuid,omitempty"`
	Version     int               `json:"__version"`
	LastUpdated string            `json:"last_updated"`
	Entities    map[string][]Edge `json:"entities"`
}

type Edge struct {
	Type   string `json:"type"`
	Target string `json:"target"`
}

func ensureInit() error {
	initOnce.Do(func() {
		initErr = InitStorage()
	})
	return initErr
}

// ------------------------------------------------------------------
// MCP Handlers
// ------------------------------------------------------------------

func HandleCommitOntologyEdge(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	if err := ensureInit(); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

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

	// Cycle Detection for Hierarchical Edges
	if isHierarchical {
		if detectCycle(globalGraph, source, target) {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: DAG Cycle Violation. Committing %s -> %s -> %s creates a circular dependency. Halt and review architecture. Use delete_ontology_edge if refactoring existing logic.", source, edgeType, target)), nil
		}
	}

	// Ensure Entity exists
	if _, exists := globalGraph.Entities[source]; !exists {
		globalGraph.Entities[source] = []Edge{}
	}

	// Prevent duplicate edges
	for _, e := range globalGraph.Entities[source] {
		if e.Type == edgeType && e.Target == target {
			return mcp.NewToolResultText(fmt.Sprintf("Edge %s -> %s -> %s already exists. No mutation needed.", source, edgeType, target)), nil
		}
	}

	// Mutate memory and append to WAL
	applyWALEntry(globalGraph, WALEntry{
		Action:    "ADD_EDGE",
		Source:    source,
		Type:      edgeType,
		Target:    target,
		Timestamp: time.Now().Format(time.RFC3339),
	})

	if err := appendToWAL("ADD_EDGE", source, edgeType, target); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to append to WAL: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully committed %s -> %s -> %s.", source, edgeType, target)), nil
}

func HandleDeleteOntologyEdge(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.Lock()
	defer mu.Unlock()

	if err := ensureInit(); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

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

	edges, exists := globalGraph.Entities[source]
	if !exists {
		return mcp.NewToolResultText(fmt.Sprintf("Source entity %s not found.", source)), nil
	}

	found := false
	for _, e := range edges {
		if e.Type == edgeType && e.Target == target {
			found = true
			break
		}
	}

	if !found {
		return mcp.NewToolResultText(fmt.Sprintf("Edge %s -> %s -> %s not found.", source, edgeType, target)), nil
	}

	// Mutate memory and append to WAL
	applyWALEntry(globalGraph, WALEntry{
		Action:    "DELETE_EDGE",
		Source:    source,
		Type:      edgeType,
		Target:    target,
		Timestamp: time.Now().Format(time.RFC3339),
	})

	if err := appendToWAL("DELETE_EDGE", source, edgeType, target); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to append to WAL: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully deleted %s -> %s -> %s.", source, edgeType, target)), nil
}

func HandleReadOntologyGraph(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	mu.RLock()
	defer mu.RUnlock()

	if err := ensureInit(); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}
	targetEntity, ok := args["target_entity"].(string)
	if !ok || targetEntity == "" {
		return mcp.NewToolResultError("target_entity is required"), nil
	}

	if len(globalGraph.Entities) == 0 {
		return mcp.NewToolResultText("Knowledge graph is currently empty."), nil
	}

	downstreamEdges, hasDownstream := globalGraph.Entities[targetEntity]

	// Find all entities that target this entity (Upstream)
	upstreamEdges := make(map[string][]string)
	hasUpstream := false
	for sourceName, edges := range globalGraph.Entities {
		for _, e := range edges {
			if e.Target == targetEntity {
				upstreamEdges[sourceName] = append(upstreamEdges[sourceName], e.Type)
				hasUpstream = true
			}
		}
	}

	if !hasDownstream && !hasUpstream {
		// Dump current state as fallback context
		bytes, _ := json.MarshalIndent(globalGraph, "", "  ")
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

func detectCycle(graph *OntologyGraph, source, target string) bool {
	if source == target {
		return true
	}

	visited := make(map[string]bool)
	var dfs func(current string) bool

	dfs = func(current string) bool {
		if current == source {
			return true
		}
		if visited[current] {
			return false
		}
		visited[current] = true

		for _, edge := range graph.Entities[current] {
			if HierarchicalEdges[edge.Type] {
				if dfs(edge.Target) {
					return true
				}
			}
		}
		return false
	}

	return dfs(target)
}

func getMemoryDir() string {
	dir := os.Getenv("MEMORY_DIR")
	if dir == "" {
		dir = "/workspace/.gemini/mem"
	}
	os.MkdirAll(dir, 0755)
	return dir
}
