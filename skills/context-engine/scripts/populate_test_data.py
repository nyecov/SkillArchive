import sqlite3
import os
import datetime

def populate():
    workspace_root = os.environ.get("WORKSPACE_ROOT", "g:\\Skill Archive")
    db_path = os.path.join(workspace_root, ".gemini", "mem", "engine.db")
    
    print(f"Connecting to database at: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Short-Term: Scratchpad
        print("Populating Scratchpad Findings...")
        cursor.execute("DELETE FROM scratchpad_findings")
        findings = [
            ("Initial system audit completed. All core modules verified.", "planning"),
            ("Implemented OpenAI shim for phi3 compatibility.", "execution"),
            ("Running BDD tests for context-engine. 12/12 passing.", "verification"),
            ("Blocked on UI latency in dashboard.", "blocked")
        ]
        for content, phase in findings:
            cursor.execute("INSERT INTO scratchpad_findings (content, phase, created_at) VALUES (?, ?, ?)", 
                           (content, phase, datetime.datetime.now().isoformat()))

        # 2. Middle-Term: Ontology (Brainmap)
        print("Populating Ontology Edges...")
        cursor.execute("DELETE FROM ontology_edges")
        edges = [
            ("CoreEngine", "REQUIRES", "SQLite"),
            ("SQLite", "IMPLEMENTS", "PersistentStorage"),
            ("CoreEngine", "OWNS", "WebUI"),
            ("WebUI", "DEPENDS_ON", "VisJS"),
            ("Agent", "REFERENCES", "CoreEngine")
        ]
        for source, edge_type, target in edges:
            cursor.execute("INSERT OR IGNORE INTO ontology_edges (source_entity, edge_type, target_entity) VALUES (?, ?, ?)", 
                           (source, edge_type, target))

        # 3. Long-Term: Ingestion History
        print("Populating Ingestion History...")
        cursor.execute("DELETE FROM ingestion_history")
        history = [
            ("g:\\Skill Archive\\README.md", "TPS standards"),
            ("g:\\Skill Archive\\skills\\context-engine\\SKILL.md", "implementation details"),
            ("g:\\Skill Archive\\server\\main.go", "routing logic")
        ]
        for path, query in history:
            cursor.execute("INSERT INTO ingestion_history (target_path, query_filter, created_at) VALUES (?, ?, ?)", 
                           (path, query, datetime.datetime.now().isoformat()))

        conn.commit()
        print("Successfully populated test data.")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate()
