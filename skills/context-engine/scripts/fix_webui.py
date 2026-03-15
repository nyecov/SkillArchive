import os

webui_path = r'G:\Skill Archive\.gemini\skills\context-engine\server\internal\webui\webui.go'
with open(webui_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_str = '\trows, err := db.Query(\"SELECT toon_pair, created_at FROM interview_qa ORDER BY created_at DESC LIMIT 50\")'
end_str = '\tjson.NewEncoder(w).Encode(qaList)\n}\n'

if start_str in content and end_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find(end_str) + len(end_str)
    content = content[:start_idx] + content[end_idx:]

with open(webui_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed webui.go')
