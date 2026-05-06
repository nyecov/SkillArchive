package pokayoke

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/nyecov/context-engine/internal/storage"
)

const (
	DiagLogFile = "engine_diagnostics.log"
)

// RunBootDiagnostics performs an integrity check on the SQLite DB.
func RunBootDiagnostics() error {
	db, err := storage.InitDB()
	if err != nil {
		return fmt.Errorf("FATAL: Cannot initialize storage DB: %v", err)
	}

	workspaceRoot := os.Getenv("WORKSPACE_ROOT")
	if workspaceRoot == "" {
		workspaceRoot = "/workspace"
	}
	memDir := os.Getenv("MEMORY_DIR")
	if memDir == "" {
		memDir = filepath.Join(workspaceRoot, ".gemini", "mem")
	}

	logPath := filepath.Join(memDir, DiagLogFile)
	logFile, err := os.OpenFile(logPath, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0666)
	if err != nil {
		return fmt.Errorf("FATAL: Cannot initialize diagnostic log: %v", err)
	}
	defer logFile.Close()

	log := func(msg string) {
		timestamp := time.Now().Format(time.RFC3339)
		logFile.WriteString(fmt.Sprintf("[%s] %s\n", timestamp, msg))
		fmt.Fprintf(os.Stderr, "[%s] %s\n", timestamp, msg)
	}

	log("Starting Context Engine Boot Sequence.")
	log(fmt.Sprintf("Memory Directory Context: %s", memDir))

	// Run SQLite Integrity Check
	log("Running PRAGMA integrity_check on engine.db...")
	var checkResult string
	err = db.QueryRowContext(context.Background(), "PRAGMA integrity_check;").Scan(&checkResult)
	if err != nil {
		log(fmt.Sprintf("CRITICAL FAILURE: DB Integrity Violation: %v", err))
		return err
	}

	if checkResult != "ok" {
		log(fmt.Sprintf("CRITICAL FAILURE: SQLite returned corruption status: %s", checkResult))
		// Instruct agent on self-healing or quarantine
		return fmt.Errorf("DB corruption detected: %s", checkResult)
	}

	log("Integrity Check Passed: engine.db is OK.")
	log("Boot Sequence Complete. Jidoka Circuit Breakers Active.")

	return nil
}
