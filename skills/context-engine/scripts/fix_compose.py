import os
compose_path = r'G:\Skill Archive\.gemini\skills\context-engine\docker-compose\docker-compose.yml'
with open(compose_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the port mapping to ONLY be in context-engine-daemon
content = content.replace('    restart: "no"\n    ports:\n      - "127.0.0.1:6767:6767"\n', '    restart: "no"\n')
with open(compose_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Cleaned ephemeral port map.')
