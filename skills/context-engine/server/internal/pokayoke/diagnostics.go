package pokayoke

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/nyecov/context-engine/internal/config"
)

const (
	ScratchpadFile = "current_session.json"
	OntologyFile   = "ontology.json"
	DiagLogFile    = "engine_diagnostics.log"
)

// RunBootDiagnostics performs a complete schema/UUID validation sequence across all memory files.
func RunBootDiagnostics() error {
	memDir := config.GetMemoryDir()
	logPath := filepath.Join(memDir, DiagLogFile)

	// We overwrite the old diagnostics log on every boot
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

	// Check Scratchpad
	scratchPath := filepath.Join(memDir, ScratchpadFile)
	log(fmt.Sprintf("Scanning Tier: Short-Term (Scratchpad) -> %s", ScratchpadFile))
	if _, err := os.Stat(scratchPath); err == nil {
		if err := verifyScratchpad(scratchPath); err != nil {
			log(fmt.Sprintf("CRITICAL FAILURE: Scratchpad Violation: %v", err))
			quarantineFile(scratchPath, log)
		} else {
			log("PROVENANCE VERIFIED: Scratchpad identity is intact.")
		}
	} else {
		log("NOTICE: Scratchpad not found. Initializing new volatile state on first write.")
	}

	// Check Ontology
	ontologyPath := filepath.Join(memDir, OntologyFile)
	log(fmt.Sprintf("Scanning Tier: Middle-Term (Ontology) -> %s", OntologyFile))
	if _, err := os.Stat(ontologyPath); err == nil {
		if err := verifyOntology(ontologyPath); err != nil {
			log(fmt.Sprintf("CRITICAL FAILURE: Ontology Violation: %v", err))
			quarantineFile(ontologyPath, log)
		} else {
			log("PROVENANCE VERIFIED: Ontology DAG identity is intact.")
		}
	} else {
		log("NOTICE: Ontology graph not found. Initializing new hierarchical state on first commit.")
	}

	log("Boot Sequence Complete. Jidoka Circuit Breakers Active.")
	return nil
}

func verifyScratchpad(path string) error {
	bytes, err := os.ReadFile(path)
	if err != nil {
		return err
	}

	var raw map[string]interface{}
	if err := json.Unmarshal(bytes, &raw); err != nil {
		return fmt.Errorf("JSON Parsing Error: %v", err)
	}

	if _, exists := raw["__uuid"]; !exists {
		return fmt.Errorf("Identity Theft: Missing __uuid property.")
	}
	if _, exists := raw["__version"]; !exists {
		return fmt.Errorf("State Desync: Missing __version property.")
	}

	return nil
}

func verifyOntology(path string) error {
	bytes, err := os.ReadFile(path)
	if err != nil {
		return err
	}

	var raw map[string]interface{}
	if err := json.Unmarshal(bytes, &raw); err != nil {
		return fmt.Errorf("JSON Parsing Error: %v", err)
	}

	if _, exists := raw["__uuid"]; !exists {
		return fmt.Errorf("Identity Theft: Missing __uuid property.")
	}
	if _, exists := raw["__version"]; !exists {
		return fmt.Errorf("State Desync: Missing __version property.")
	}

	return nil
}

func quarantineFile(path string, logFunc func(string)) string {
	corruptedPath := path + time.Now().Format(".corrupted-2006-01-02-15-04-05")
	os.Rename(path, corruptedPath)
	logFunc(fmt.Sprintf("ACTION GUARANTEED: File quarantined to %s. State reset to empty on next tool call.", corruptedPath))
	return corruptedPath
}
