import sqlite3
import os

def check():
    db_path = "g:\\Skill Archive\\.gemini\\mem\\engine.db"
    print(f"Checking DB at: {db_path}")
    if not os.path.exists(db_path):
        print("DB DOES NOT EXIST")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    for table in tables:
        tname = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {tname}")
        count = cursor.fetchone()[0]
        print(f"Table {tname}: {count} rows")
    
    conn.close()

if __name__ == "__main__":
    check()
