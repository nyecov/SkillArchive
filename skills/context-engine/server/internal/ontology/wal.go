package ontology

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type WALEntry struct {
	Action    string `json:"action"`
	Source    string `json:"source"`
	Type      string `json:"type"`
	Target    string `json:"target"`
	Timestamp string `json:"timestamp"`
}

var (
	globalGraph *OntologyGraph
	walFile     *os.File
	isInit      bool
)

// InitStorage loads the baseline ontology and replays the WAL.
func InitStorage() error {
	if isInit {
		return nil
	}

	memDir := getMemoryDir()
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
	bytes = append(bytes, '
')

	if _, err := walFile.Write(bytes); err != nil {
		return err
	}
	return walFile.Sync()
}
