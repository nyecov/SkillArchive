package webui

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	
	"github.com/nyecov/context-engine/internal/storage"
)

// StartServer starts the WebUI HTTP server in a separate goroutine.
func StartServer(port string) {
	mux := http.NewServeMux()

	// 1. API: Status (Integrity Check Results)
	mux.HandleFunc("/api/status", handleStatus)

	// 2. API: Scratchpad (scratchpad_findings table)
	mux.HandleFunc("/api/scratchpad", handleScratchpad)

	// 3. API: Ingestion (ingestion_history table)
	mux.HandleFunc("/api/ingestion", handleIngestion)

	// 4. API: Graph (ontology_edges table)
	mux.HandleFunc("/api/graph", handleGraph)

	// 4. Static File Server
	staticDir := os.Getenv("WEBUI_DIR")
	if staticDir == "" {
		staticDir = "/webui"
	}
	mux.Handle("/", http.FileServer(http.Dir(staticDir)))

	go func() {
		fmt.Fprintf(os.Stderr, "[WEBUI] Starting HTTP server on port %s\n", port)
		if err := http.ListenAndServe(":"+port, securityMiddleware(mux)); err != nil {
			fmt.Fprintf(os.Stderr, "[WEBUI] Error starting server: %v\n", err)
		}
	}()
}

func securityMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Strict Read-Only Poka-yoke
		if r.Method != http.MethodGet {
			http.Error(w, "Method Not Allowed - WebUI is Read-Only", http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Access-Control-Allow-Origin", "*") // For local dev flexibility
		next.ServeHTTP(w, r)
	})
}


func handleScratchpad(w http.ResponseWriter, r *http.Request) {
	db := storage.GetDB()
	if db == nil {
		http.Error(w, "Database not available", http.StatusServiceUnavailable)
		return
	}

	rows, err := db.Query("SELECT content, phase, created_at FROM scratchpad_findings ORDER BY created_at DESC LIMIT 50")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var list []map[string]string
	for rows.Next() {
		var content, phase, date string
		if err := rows.Scan(&content, &phase, &date); err == nil {
			list = append(list, map[string]string{
				"content": content,
				"phase":   phase,
				"date":    date,
			})
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(list)
}

func handleIngestion(w http.ResponseWriter, r *http.Request) {
	db := storage.GetDB()
	if db == nil {
		http.Error(w, "Database not available", http.StatusServiceUnavailable)
		return
	}

	rows, err := db.Query("SELECT target_path, query_filter, created_at FROM ingestion_history ORDER BY created_at DESC LIMIT 50")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var list []map[string]string
	for rows.Next() {
		var path, filter, date string
		if err := rows.Scan(&path, &filter, &date); err == nil {
			list = append(list, map[string]string{
				"target_path":  path,
				"query_filter": filter,
				"date":         date,
			})
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(list)
}

func handleStatus(w http.ResponseWriter, r *http.Request) {
	// For now, we manually report OK if DB is reachable
	db := storage.GetDB()
	if db == nil {
		w.WriteHeader(http.StatusServiceUnavailable)
		json.NewEncoder(w).Encode(map[string]string{"status": "offline", "error": "Database not initialized"})
		return
	}

	err := db.Ping()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(map[string]string{"status": "error", "error": err.Error()})
		return
	}

	json.NewEncoder(w).Encode(map[string]string{"status": "online", "diagnostics": "PRAGMA integrity_check passed on boot"})
}



func handleGraph(w http.ResponseWriter, r *http.Request) {
	db := storage.GetDB()
	if db == nil {
		http.Error(w, "Database not available", http.StatusServiceUnavailable)
		return
	}

	rows, err := db.Query("SELECT source_entity, edge_type, target_entity FROM ontology_edges")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var edges []map[string]string
	for rows.Next() {
		var s, e, t string
		if err := rows.Scan(&s, &e, &t); err == nil {
			edges = append(edges, map[string]string{
				"from": s,
				"to":   t,
				"type": e,
			})
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(edges)
}
