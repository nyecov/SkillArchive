import sqlite3
import os

def wipe_all():
    # Target BOTH possible locations to be absolutely sure
    paths = [
        "g:\\Skill Archive\\.gemini\\mem\\engine.db",
        "g:\\Skill Archive\\skills\\.gemini\\mem\\engine.db"
    ]
    
    for db_path in paths:
        if not os.path.exists(db_path):
            print("DB not found at", db_path)
            continue

        print(f"Wiping {db_path}...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            tables = ["scratchpad_findings", "ontology_edges", "ingestion_history"]
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print(f"Successfully wiped all memory tables in {db_path}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    wipe_all()
