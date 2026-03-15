package storage

import (
	"context"
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"sync"

	_ "modernc.org/sqlite"
)

var (
	db            *sql.DB
	dbOnce        sync.Once
	globalInitErr error
)

// InitDB initializes the SQLite database running in WAL mode for Swarm concurrency.
func InitDB() (*sql.DB, error) {
	dbOnce.Do(func() {
		workspaceRoot := os.Getenv("WORKSPACE_ROOT")
		if workspaceRoot == "" {
			workspaceRoot = "/workspace"
		}

		memoryDir := os.Getenv("MEMORY_DIR")
		if memoryDir == "" {
			memoryDir = filepath.Join(workspaceRoot, ".gemini", "mem")
		}

		if err := os.MkdirAll(memoryDir, 0755); err != nil {
			globalInitErr = fmt.Errorf("failed to create memory directory: %w", err)
			return
		}

		dbPath := filepath.Join(memoryDir, "engine.db")

		// Query string to enforce DELETE mode, synchronous=NORMAL, and a busy_timeout
		// This prevents SQLITE_CANTOPEN errors when mounting Windows volumes into Docker containers
		// because WAL mode requires POSIX shared memory files (.shm) which fail across OS barriers.
		dsn := fmt.Sprintf("%s?_pragma=journal_mode(DELETE)&_pragma=synchronous(NORMAL)&_pragma=busy_timeout(5000)", dbPath)

		d, err := sql.Open("sqlite", dsn)
		if err != nil {
			globalInitErr = fmt.Errorf("failed to open sqlite db: %w", err)
			return
		}

		// Create tables if they do not exist
		if err := createSchemas(d); err != nil {
			d.Close()
			globalInitErr = fmt.Errorf("failed to create schemas: %w", err)
			return
		}

		db = d
	})

	if globalInitErr != nil {
		return nil, globalInitErr
	}

	return db, nil
}

// GetDB returns the initialized db instance
func GetDB() *sql.DB {
	return db
}

// CloseDB gracefully closes the db connection
func CloseDB() error {
	if db != nil {
		return db.Close()
	}
	return nil
}

func createSchemas(d *sql.DB) error {
	ctx := context.Background()
	tx, err := d.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// 1. Scratchpad Findings Table
	_, err = tx.Exec(`
		CREATE TABLE IF NOT EXISTS scratchpad_findings (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			content TEXT NOT NULL,
			phase TEXT NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		return err
	}

	// 2. Ontology Edges Table
	_, err = tx.Exec(`
		CREATE TABLE IF NOT EXISTS ontology_edges (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			source_entity TEXT NOT NULL,
			edge_type TEXT NOT NULL,
			target_entity TEXT NOT NULL,
			UNIQUE(source_entity, edge_type, target_entity)
		)
	`)
	if err != nil {
		return err
	}

	// 3. Ingestion History Table
	_, err = tx.Exec(`
		CREATE TABLE IF NOT EXISTS ingestion_history (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			target_path TEXT NOT NULL,
			query_filter TEXT,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		return err
	}

	// 4. Semantic Search FTS5 Virtual Table
	_, err = tx.Exec(`
		CREATE VIRTUAL TABLE IF NOT EXISTS ontology_fts USING fts5(
			source_entity, 
			target_entity, 
			edge_type, 
			content='ontology_edges', 
			content_rowid='id'
		)
	`)
	if err != nil {
		return err
	}

	// 5. Triggers for Auto-Syncing FTS Table
	_, err = tx.Exec(`
		CREATE TRIGGER IF NOT EXISTS ontology_ai AFTER INSERT ON ontology_edges BEGIN
			INSERT INTO ontology_fts(rowid, source_entity, target_entity, edge_type) 
			VALUES (new.id, new.source_entity, new.target_entity, new.edge_type);
		END;

		CREATE TRIGGER IF NOT EXISTS ontology_ad AFTER DELETE ON ontology_edges BEGIN
			INSERT INTO ontology_fts(ontology_fts, rowid, source_entity, target_entity, edge_type) 
			VALUES ('delete', old.id, old.source_entity, old.target_entity, old.edge_type);
		END;

		CREATE TRIGGER IF NOT EXISTS ontology_au AFTER UPDATE ON ontology_edges BEGIN
			INSERT INTO ontology_fts(ontology_fts, rowid, source_entity, target_entity, edge_type) 
			VALUES ('delete', old.id, old.source_entity, old.target_entity, old.edge_type);
			INSERT INTO ontology_fts(rowid, source_entity, target_entity, edge_type) 
			VALUES (new.id, new.source_entity, new.target_entity, new.edge_type);
		END;
	`)
	if err != nil {
		return err
	}

	return tx.Commit()
}
