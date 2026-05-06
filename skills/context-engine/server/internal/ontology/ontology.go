package ontology

import (
	"context"
	"database/sql"
	"fmt"
	"strings"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/nyecov/context-engine/internal/storage"
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

// ------------------------------------------------------------------
// MCP Handlers
// ------------------------------------------------------------------

func HandleCommitOntologyEdge(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
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

	// Cycle Detection for Hierarchical Edges using Recursive CTE
	if isHierarchical {
		hasCycle, err := detectCycleInDB(db, source, target)
		if err != nil {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: Cycle detection failed: %v", err)), nil
		}
		if hasCycle {
			return mcp.NewToolResultError(fmt.Sprintf("ToolError: DAG Cycle Violation. Committing %s -> %s -> %s creates a circular dependency. Halt and review architecture. Use delete_ontology_edge if refactoring existing logic.", source, edgeType, target)), nil
		}
	}

	// Insert into SQLite
	// ON CONFLICT DO NOTHING relies on the UNIQUE(source_entity, edge_type, target_entity) constraint
	query := `INSERT INTO ontology_edges (source_entity, edge_type, target_entity) VALUES (?, ?, ?) ON CONFLICT DO NOTHING`
	result, err := db.ExecContext(ctx, query, source, edgeType, target)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Database insert failed: %v", err)), nil
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		return mcp.NewToolResultText(fmt.Sprintf("Edge %s -> %s -> %s already exists. No mutation needed.", source, edgeType, target)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully committed %s -> %s -> %s.", source, edgeType, target)), nil
}

func HandleDeleteOntologyEdge(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
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

	query := `DELETE FROM ontology_edges WHERE source_entity = ? AND edge_type = ? AND target_entity = ?`
	res, err := db.ExecContext(ctx, query, source, edgeType, target)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Database delete failed: %v", err)), nil
	}

	rowsAffected, _ := res.RowsAffected()
	if rowsAffected == 0 {
		return mcp.NewToolResultText(fmt.Sprintf("Edge %s -> %s -> %s not found.", source, edgeType, target)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Successfully deleted %s -> %s -> %s.", source, edgeType, target)), nil
}

func HandleReadOntologyGraph(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
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

	// 1. Check if Graph is entirely empty
	var count int
	if err := db.QueryRowContext(ctx, `SELECT COUNT(*) FROM ontology_edges`).Scan(&count); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: DB count failed: %v", err)), nil
	}
	if count == 0 {
		return mcp.NewToolResultText("Knowledge graph is currently empty."), nil
	}

	// 2. Fetch Downstream
	downQuery := `SELECT edge_type, target_entity FROM ontology_edges WHERE source_entity = ?`
	downRows, err := db.QueryContext(ctx, downQuery, targetEntity)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: DB downstream query failed: %v", err)), nil
	}
	defer downRows.Close()

	var downstreamEdges []string
	for downRows.Next() {
		var eType, eTarget string
		if err := downRows.Scan(&eType, &eTarget); err == nil {
			downstreamEdges = append(downstreamEdges, fmt.Sprintf("- [%s] -> %s", eType, eTarget))
		}
	}

	// 3. Fetch Upstream
	upQuery := `SELECT source_entity, edge_type FROM ontology_edges WHERE target_entity = ?`
	upRows, err := db.QueryContext(ctx, upQuery, targetEntity)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: DB upstream query failed: %v", err)), nil
	}
	defer upRows.Close()

	var upstreamEdges []string
	for upRows.Next() {
		var eSource, eType string
		if err := upRows.Scan(&eSource, &eType); err == nil {
			upstreamEdges = append(upstreamEdges, fmt.Sprintf("- %s -> [%s]", eSource, eType))
		}
	}

	if len(downstreamEdges) == 0 && len(upstreamEdges) == 0 {
		// Dump the whole graph as a fallback context since the entity wasn't found directly
		dumpQuery := `SELECT source_entity, edge_type, target_entity FROM ontology_edges`
		dumpRows, err := db.QueryContext(ctx, dumpQuery)
		if err == nil {
			defer dumpRows.Close()
			var dump []string
			for dumpRows.Next() {
				var s, t, tar string
				if err := dumpRows.Scan(&s, &t, &tar); err == nil {
					dump = append(dump, fmt.Sprintf("%s -> [%s] -> %s", s, t, tar))
				}
			}
			return mcp.NewToolResultText(fmt.Sprintf("Entity '%s' not found in graph. Here is the entire raw graph for context:\n\n%s", targetEntity, strings.Join(dump, "\n"))), nil
		}
	}

	// Format specific payload
	output := fmt.Sprintf("=== Knowledge Graph Local Vector for: %s ===\n", targetEntity)
	if len(downstreamEdges) > 0 {
		output += "\nDownstream Dependencies (It relies on):\n"
		output += strings.Join(downstreamEdges, "\n") + "\n"
	}
	if len(upstreamEdges) > 0 {
		output += "\nUpstream Dependencies (Relies on it):\n"
		output += strings.Join(upstreamEdges, "\n") + "\n"
	}

	return mcp.NewToolResultText(output), nil
}

func HandleSearchOntologySemantic(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	db, err := ensureDB()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("ToolError: Failed to init storage: %v", err)), nil
	}

	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("Arguments must be a JSON object"), nil
	}
	query, ok := args["query"].(string)
	if !ok || query == "" {
		return mcp.NewToolResultError("query is required and cannot be empty"), nil
	}
	if len(query) > 100 {
		return mcp.NewToolResultError("query is too long"), nil
	}

	// We use parameterized queries to prevent SQL injection (Poka-yoke / KYT)
	ftsQuery := `SELECT source_entity, target_entity, edge_type 
	             FROM ontology_fts 
	             WHERE ontology_fts MATCH ? ORDER BY rank LIMIT 10;`

	rows, err := db.QueryContext(ctx, ftsQuery, query)
	if err != nil {
		// If query is malformed for FTS5 syntax, gracefully return an empty set or error text rather than crashing
		return mcp.NewToolResultText(fmt.Sprintf("Search failed or no matches found for '%s': %v", query, err)), nil
	}
	defer rows.Close()

	var results []string
	for rows.Next() {
		var src, tgt, etype string
		if err := rows.Scan(&src, &tgt, &etype); err == nil {
			results = append(results, fmt.Sprintf("- %s -> [%s] -> %s", src, etype, tgt))
		}
	}

	if len(results) == 0 {
		return mcp.NewToolResultText(fmt.Sprintf("No semantic matches found for query: '%s'.", query)), nil
	}

	output := fmt.Sprintf("=== Semantic Search Results for: '%s' ===\n", query)
	output += strings.Join(results, "\n")
	return mcp.NewToolResultText(output), nil
}

// detectCycleInDB checks if inserting source -> target creates a cycle.
// It checks if a path exists from target down to source.
func detectCycleInDB(db *sql.DB, source, target string) (bool, error) {
	if source == target {
		return true, nil
	}

	query := `WITH RECURSIVE
	  paths(node, visited) AS (
	    SELECT target_entity, ',' || source_entity || ',' || target_entity || ','
	    FROM ontology_edges
	    WHERE source_entity = ? AND edge_type IN ('REQUIRES', 'IMPLEMENTS', 'DEPENDS_ON', 'OWNS')
	    
	    UNION ALL
	    
	    SELECT oe.target_entity, p.visited || oe.target_entity || ','
	    FROM ontology_edges oe
	    JOIN paths p ON oe.source_entity = p.node
	    WHERE oe.edge_type IN ('REQUIRES', 'IMPLEMENTS', 'DEPENDS_ON', 'OWNS')
	      AND instr(p.visited, ',' || oe.target_entity || ',') = 0
	  )
	SELECT 1 FROM paths WHERE node = ? LIMIT 1;`

	var found int
	err := db.QueryRow(query, target, source).Scan(&found)
	if err == sql.ErrNoRows {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	return found == 1, nil
}
