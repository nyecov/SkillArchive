import os

ingestion_path = r'G:\Skill Archive\.gemini\skills\context-engine\server\internal\ingestion\ingestion.go'
with open(ingestion_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add storage import
content = content.replace('\"strings\"\n', '\"strings\"\n\t\"github.com/nyecov/context-engine/internal/storage\"\n')

# Add logging logic at the end of HandleIngestContext
log_logic = '''
        // Log to ingestion history
        if db := storage.GetDB(); db != nil {
                queryStr := ""
                if hasQuery {
                        if q, ok := queryInterFace.(string); ok {
                                queryStr = q
                        }
                }
                db.Exec("INSERT INTO ingestion_history (target_path, query_filter) VALUES (?, ?)", targetPath, queryStr)
        }

        return mcp.NewToolResultText(content), nil
}
'''

content = content.replace('return mcp.NewToolResultText(content), nil\n}', log_logic)

with open(ingestion_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated ingestion.go with logging.')
