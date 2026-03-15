import os

main_path = r'G:\Skill Archive\.gemini\skills\context-engine\server\cmd\server\main.go'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('webEnabled := flag.Bool("web", false,', 'webEnabled := flag.Bool("web", true,')
content = content.replace('webPort := flag.String("port", "8080",', 'webPort := flag.String("port", "6767",')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

dockerfile_path = r'G:\Skill Archive\.gemini\skills\context-engine\Dockerfile'
with open(dockerfile_path, 'r', encoding='utf-8') as f:
    docker_content = f.read()

docker_content = docker_content.replace('EXPOSE 8080', 'EXPOSE 6767')
with open(dockerfile_path, 'w', encoding='utf-8') as f:
    f.write(docker_content)

compose_path = r'G:\Skill Archive\.gemini\skills\context-engine\docker-compose\docker-compose.yml'
with open(compose_path, 'r', encoding='utf-8') as f:
    compose_content = f.read()

if '6767:6767' not in compose_content:
    compose_content = compose_content.replace(
        '    restart: "no"\n',
        '    restart: "no"\n    ports:\n      - "127.0.0.1:6767:6767"\n'
    )
    compose_content = compose_content.replace(
        '    command: [ "/context-engine-server" ]',
        '    ports:\n      - "127.0.0.1:6767:6767"\n    command: [ "/context-engine-server" ]'
    )
    with open(compose_path, 'w', encoding='utf-8') as f:
        f.write(compose_content)

print('Updated successfully.')
