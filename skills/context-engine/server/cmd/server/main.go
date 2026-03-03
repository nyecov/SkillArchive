package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/nyecov/context-engine/internal/ingestion"
	"github.com/nyecov/context-engine/internal/interview"
	"github.com/nyecov/context-engine/internal/ontology"
	"github.com/nyecov/context-engine/internal/pokayoke"
	"github.com/nyecov/context-engine/internal/scratchpad"
)

func main() {
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

	// Register Tool: append_interview_qa
	registerAppendInterviewQATool(s)

	// Register Tool: retrieve_interview_patterns
	registerRetrieveInterviewPatternsTool(s)

	// Register Tool: prune_interview_qa
	registerPruneInterviewQATool(s)

	// Run Poka-yoke Boot Diagnostics
	if err := pokayoke.RunBootDiagnostics(); err != nil {
		fmt.Fprintf(os.Stderr, "Boot Diagnostics Failed: %v\n", err)
	}

	// Structural Singleton Check (Jidoka Halt)
	if err := pokayoke.AcquireSingletonLock(); err != nil {
		fmt.Fprintf(os.Stderr, "FATAL ERROR: %v\n", err)
		os.Exit(1)
	}
	defer pokayoke.ReleaseSingletonLock()

	// Initialize the Heartbeat to prove we are alive and hold the lock.
	// StartHeartbeat returns a channel that fires if the lock is lost.
	heartbeatCtx, cancelHeartbeat := context.WithCancel(context.Background())
	defer cancelHeartbeat()
	heartbeatLost := pokayoke.StartHeartbeat(heartbeatCtx)

	// Handle Graceful Shutdown from OS signals or heartbeat loss
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		select {
		case <-sigs:
			fmt.Fprintf(os.Stderr, "\n[SHUTDOWN] Signal received. Canceling heartbeat and releasing singleton lock...\n")
		case <-heartbeatLost:
			fmt.Fprintf(os.Stderr, "\n[SHUTDOWN] Heartbeat lost. Initiating graceful shutdown to protect data integrity...\n")
		}
		cancelHeartbeat()
		pokayoke.ReleaseSingletonLock()
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

func registerAppendInterviewQATool(s *server.MCPServer) {
	tool := mcp.NewTool("append_interview_qa",
		mcp.WithDescription("Appends a Socratic Q&A pair to the Interview Memory Bank using TOON format. MUST be used to log interview insights safely."),
		mcp.WithString("toon_qa_pair", mcp.Required(), mcp.Description("The Q&A pair in strict TOON format, starting with [Q: ...] and ending with [A: ...].")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return interview.HandleAppendInterviewQA(ctx, request)
	})
}

func registerRetrieveInterviewPatternsTool(s *server.MCPServer) {
	tool := mcp.NewTool("retrieve_interview_patterns",
		mcp.WithDescription("Retrieves semantic chunks from the Interview Memory Bank. Uses a streaming parser to respect the 16k context window."),
		mcp.WithString("query", mcp.Description("(Optional) Keyword or semantic string to filter the TOON blocks. If empty, retrieves the latest blocks.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return interview.HandleRetrieveInterviewPatterns(ctx, request)
	})
}

func registerPruneInterviewQATool(s *server.MCPServer) {
	tool := mcp.NewTool("prune_interview_qa",
		mcp.WithDescription("Manually removes Q&A blocks from the Interview Memory Bank based on date or keyword. AT LEAST ONE parameter is required."),
		mcp.WithString("before_date", mcp.Description("(Optional) Remove all entries older than this date. Format: RFC3339 (e.g. 2026-01-01T00:00:00Z).")),
		mcp.WithString("query", mcp.Description("(Optional) Remove all entries matching this keyword or phrase.")),
	)

	s.AddTool(tool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return interview.HandlePruneInterviewQA(ctx, request)
	})
}
