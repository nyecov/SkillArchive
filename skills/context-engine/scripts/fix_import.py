import os
import re

webui_path = r'G:\Skill Archive\.gemini\skills\context-engine\server\internal\webui\webui.go'
with open(webui_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\"path/filepath\"\n', '')

with open(webui_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed unused import.')
