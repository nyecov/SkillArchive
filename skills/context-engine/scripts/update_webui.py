import os

webui_path = r'G:\Skill Archive\.gemini\skills\context-engine\server\internal\webui\webui.go'
with open(webui_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Register new endpoints
content = content.replace('// 3. API: Graph (ontology_edges table)\n\tmux.HandleFunc(\"/api/graph\", handleGraph)\n\n', 
'''// 2. API: Scratchpad (scratchpad_findings table)
	mux.HandleFunc("/api/scratchpad", handleScratchpad)

	// 3. API: Ingestion (ingestion_history table)
	mux.HandleFunc("/api/ingestion", handleIngestion)

	// 4. API: Graph (ontology_edges table)
	mux.HandleFunc("/api/graph", handleGraph)

''')

# Add handler functions
new_handlers = '''
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

'''

content = content.replace('func handleStatus(w http.ResponseWriter, r *http.Request) {', new_handlers + 'func handleStatus(w http.ResponseWriter, r *http.Request) {')

with open(webui_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated webui.go with new handlers.')
