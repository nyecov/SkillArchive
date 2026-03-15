package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/nyecov/context-engine/internal/ingestion"
	"github.com/nyecov/context-engine/internal/ontology"
	"github.com/nyecov/context-engine/internal/pokayoke"
	"github.com/nyecov/context-engine/internal/scratchpad"
	"github.com/nyecov/context-engine/internal/webui"
)

func main() {
	// Parse Flags
	webEnabled := flag.Bool("web", true, "Enable the WebUI HTTP server")
	webPort := flag.String("port", "6767", "Port for the WebUI HTTP server")
	flag.Parse()

	if *webEnabled {
		webui.StartServer(*webPort)
	}

	// Initialize the MCP Server
	s := server.NewMCPServer(
		"Context Engine",
		"1.0.0",
	)

	// Register Tool: ingest_context
	registerIngestContextTool(s)

	// Register Tool: log_session_finding
	registerLogSessionFindingTool(s)

	// Register Tool: read_session_state
	registerReadSessionStateTool(s)

	// Register Tool: delete_session_finding
	registerDeleteSessionFindingTool(s)

	// Register Tool: clear_session_state
	registerClearSessionStateTool(s)

	// Register Tool: commit_ontology_edge
	registerCommitOntologyEdgeTool(s)

	// Register Tool: delete_ontology_edge
	registerDeleteOntologyEdgeTool(s)

	// Register Tool: read_ontology_graph
	registerReadOntologyGraphTool(s)

	// Register Tool: search_ontology_semantic
	registerSearchOntologySemanticTool(s)

	// Run Poka-yoke Boot Diagnostics
	if err := pokayoke.RunBootDiagnostics(); err != nil {
		fmt.Fprintf(os.Stderr, "Boot Diagnostics Failed: %v\n", err)
	}

	// Handle Graceful Shutdown from OS signals
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigs
		fmt.Fprintf(os.Stderr, "\n[SHUTDOWN] Signal received. Initiating graceful shutdown...\n")
		os.Exit(0)
	}()

	// Start the stdio server (This blocks indefinitely, serving JSON-RPC over stdin/stdout)
	if err := server.ServeStdio(s); err != nil {
		fmt.Fprintf(os.Stderr, "Context Engine MCP Server exited: %v\n", err)
	}
}

// ------------------------------------------------------------------
// Tool Registration Functions
// ------------------------------------------------------------------

func registerIngestContextTool(s *server.MCPServer) {
	tool := mcp.NewTool("ingest_context",
		mcp.WithDescription("Ingests a file safely. Truncates and chunks files exceeding 16k chars. Handles TOON, JSON, and Markdown."),
		mcp.WithString("target_path", mcp.Required(), mcp.Description("Absolute/relative path to the file to ingest.")),
		mcp.WithString("query", mcp.Description("(Optional) Specific keyword query to extract relevant chunks.")),
		mcp.WithNumber("start_offset", mcp.Description("(Optional) Byte offset to start reading from for paginated file ingestion.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ingestion.HandleIngestContext(ctx, request)
	})
}

func registerLogSessionFindingTool(s *server.MCPServer) {
	tool := mcp.NewTool("log_session_finding",
		mcp.WithDescription("Writes a critical finding to the volatile short-term scratchpad. Limits size dynamically."),
		mcp.WithString("finding_text", mcp.Required(), mcp.Description("The finding to record.")),
		mcp.WithString("phase", mcp.Required(), mcp.Description("The current phase: [planning, execution, verification, blocked]")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return scratchpad.HandleLogSessionFinding(ctx, request)
	})
}

func registerReadSessionStateTool(s *server.MCPServer) {
	tool := mcp.NewTool("read_session_state",
		mcp.WithDescription("Retrieves the current state of volatile session memory."),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return scratchpad.HandleReadSessionState(ctx, request)
	})
}

func registerDeleteSessionFindingTool(s *server.MCPServer) {
	tool := mcp.NewTool("delete_session_finding",
		mcp.WithDescription("Removes a specific finding from the volatile scratchpad by its 0-based index."),
		mcp.WithNumber("index", mcp.Required(), mcp.Description("The 0-based index of the finding to delete.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return scratchpad.HandleDeleteSessionFinding(ctx, request)
	})
}

func registerClearSessionStateTool(s *server.MCPServer) {
	tool := mcp.NewTool("clear_session_state",
		mcp.WithDescription("Resets the volatile scratchpad, permanently deleting all session findings."),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return scratchpad.HandleClearSessionState(ctx, request)
	})
}

func registerCommitOntologyEdgeTool(s *server.MCPServer) {
	tool := mcp.NewTool("commit_ontology_edge",
		mcp.WithDescription("Hard-commits a new relationship to the Knowledge Graph. Hierarchical edges fail if it creates a DAG cycle."),
		mcp.WithString("source_entity", mcp.Required(), mcp.Description("Source node name.")),
		mcp.WithString("edge_type", mcp.Required(), mcp.Description("Enum: REQUIRES, IMPLEMENTS, DEPENDS_ON, OWNS, REFERENCES, CONFLICTS_WITH.")),
		mcp.WithString("target_entity", mcp.Required(), mcp.Description("Target node name.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ontology.HandleCommitOntologyEdge(ctx, request)
	})
}

func registerDeleteOntologyEdgeTool(s *server.MCPServer) {
	tool := mcp.NewTool("delete_ontology_edge",
		mcp.WithDescription("Removes an existing edge from the Knowledge Graph. Use to resolve DAG cycles."),
		mcp.WithString("source_entity", mcp.Required(), mcp.Description("Source node name.")),
		mcp.WithString("edge_type", mcp.Required(), mcp.Description("Edge type to remove.")),
		mcp.WithString("target_entity", mcp.Required(), mcp.Description("Target node name.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ontology.HandleDeleteOntologyEdge(ctx, request)
	})
}

func registerReadOntologyGraphTool(s *server.MCPServer) {
	tool := mcp.NewTool("read_ontology_graph",
		mcp.WithDescription("Queries the Knowledge Graph for an entity's dependencies."),
		mcp.WithString("target_entity", mcp.Required(), mcp.Description("Entity node to query.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ontology.HandleReadOntologyGraph(ctx, request)
	})
}

func registerSearchOntologySemanticTool(s *server.MCPServer) {
	tool := mcp.NewTool("search_ontology_semantic",
		mcp.WithDescription("Searches the Knowledge Graph for entities and relationships using fuzzy/semantic keyword matching. Use this when you forget the exact node name."),
		mcp.WithString("query", mcp.Required(), mcp.Description("The search query (e.g., 'Redis cache', 'authentication').")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ontology.HandleSearchOntologySemantic(ctx, request)
	})
}



