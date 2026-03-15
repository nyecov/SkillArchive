import os
import re

sqlite_path = r'G:\Skill Archive\.gemini\skills\context-engine\server\internal\storage\sqlite.go'
with open(sqlite_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Ingestion History Table
ingestion_table = '''
        // 3. Ingestion History Table
        _, err = tx.Exec(
                CREATE TABLE IF NOT EXISTS ingestion_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_path TEXT NOT NULL,
                        query_filter TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
        )
        if err != nil {
                return err
        }
'''

content = content.replace('return tx.Commit()', ingestion_table + '\n\treturn tx.Commit()')

with open(sqlite_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated sqlite.go with ingestion_history table.')
