package ontology

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/nyecov/context-engine/internal/config"
)

type WALEntry struct {
	Action    string `json:"action"`
	Source    string `json:"source"`
	Type      string `json:"type"`
	Target    string `json:"target"`
	Timestamp string `json:"timestamp"`
}

const (
	// CheckpointThreshold defines how many WAL mutations accumulate before
	// the in-memory graph is flushed to ontology.json and the WAL is truncated.
	CheckpointThreshold = 10
)

var (
	globalGraph    *OntologyGraph
	walFile        *os.File
	isInit         bool
	mutationsSinceCheckpoint int
)

// InitStorage loads the baseline ontology and replays the WAL.
func InitStorage() error {
	if isInit {
		return nil
	}

	memDir := config.GetMemoryDir()
	graphPath := filepath.Join(memDir, GraphFilename)

	// Load baseline graph
	graph, err := loadOntologyState(graphPath)
	if err != nil {
		return err
	}
	globalGraph = graph

	walPath := filepath.Join(memDir, "ontology.wal")

	// Replay WAL
	if err := replayWAL(walPath, globalGraph); err != nil {
		return err
	}

	// Open WAL for appending
	f, err := os.OpenFile(walPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	walFile = f
	isInit = true
	mutationsSinceCheckpoint = 0

	return nil
}

func replayWAL(walPath string, graph *OntologyGraph) error {
	file, err := os.Open(walPath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil
		}
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Bytes()
		if len(line) == 0 {
			continue
		}
		var entry WALEntry
		if err := json.Unmarshal(line, &entry); err != nil {
			// Ignore corrupted WAL lines or log them
			continue
		}
		applyWALEntry(graph, entry)
	}
	return scanner.Err()
}

func applyWALEntry(graph *OntologyGraph, entry WALEntry) {
	if entry.Action == "ADD_EDGE" {
		if _, exists := graph.Entities[entry.Source]; !exists {
			graph.Entities[entry.Source] = []Edge{}
		}
		graph.Entities[entry.Source] = append(graph.Entities[entry.Source], Edge{
			Type:   entry.Type,
			Target: entry.Target,
		})
	} else if entry.Action == "DELETE_EDGE" {
		edges, exists := graph.Entities[entry.Source]
		if !exists {
			return
		}
		filtered := []Edge{}
		for _, e := range edges {
			if e.Type == entry.Type && e.Target == entry.Target {
				continue
			}
			filtered = append(filtered, e)
		}
		graph.Entities[entry.Source] = filtered
	}
	graph.Version++
	graph.LastUpdated = entry.Timestamp
}

func appendToWAL(action, source, edgeType, target string) error {
	entry := WALEntry{
		Action:    action,
		Source:    source,
		Type:      edgeType,
		Target:    target,
		Timestamp: time.Now().Format(time.RFC3339),
	}
	bytes, err := json.Marshal(entry)
	if err != nil {
		return err
	}
	bytes = append(bytes, '\n')

	if _, err := walFile.Write(bytes); err != nil {
		return err
	}
	return walFile.Sync()
}

// maybeCheckpoint flushes the in-memory graph to ontology.json and truncates the WAL
// when the mutation count exceeds CheckpointThreshold. This prevents unbounded WAL
// growth and ensures the baseline snapshot stays current.
func maybeCheckpoint() {
	mutationsSinceCheckpoint++
	if mutationsSinceCheckpoint < CheckpointThreshold {
		return
	}

	memDir := config.GetMemoryDir()
	graphPath := filepath.Join(memDir, GraphFilename)

	if err := checkpoint(graphPath); err != nil {
		fmt.Fprintf(os.Stderr, "[ONTOLOGY-CHECKPOINT] Warning: checkpoint failed: %v\n", err)
		return
	}

	mutationsSinceCheckpoint = 0
	fmt.Fprintf(os.Stderr, "[ONTOLOGY-CHECKPOINT] Graph flushed to %s. WAL truncated.\n", GraphFilename)
}

// checkpoint atomically writes the in-memory graph to ontology.json and truncates the WAL.
func checkpoint(graphPath string) error {
	// 1. Atomic write graph to disk via tmp + rename
	bytes, err := json.MarshalIndent(globalGraph, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal error: %v", err)
	}

	tmpPath := graphPath + ".tmp"
	f, err := os.OpenFile(tmpPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return fmt.Errorf("tmp file error: %v", err)
	}

	if _, err := f.Write(bytes); err != nil {
		f.Close()
		return fmt.Errorf("write error: %v", err)
	}
	if err := f.Sync(); err != nil {
		f.Close()
		return fmt.Errorf("sync error: %v", err)
	}
	f.Close()

	if err := os.Rename(tmpPath, graphPath); err != nil {
		return fmt.Errorf("rename error: %v", err)
	}

	// 2. Truncate WAL (close, truncate, reopen for append)
	if walFile != nil {
		walFile.Close()
	}

	walPath := filepath.Join(config.GetMemoryDir(), "ontology.wal")
	if err := os.Truncate(walPath, 0); err != nil {
		return fmt.Errorf("WAL truncate error: %v", err)
	}

	wf, err := os.OpenFile(walPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("WAL reopen error: %v", err)
	}
	walFile = wf

	return nil
}
