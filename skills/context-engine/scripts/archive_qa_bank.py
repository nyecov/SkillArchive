import os
import shutil

base_dir = r'G:\Skill Archive\.gemini\skills\context-engine'
archive_dir = os.path.join(base_dir, 'archive', 'qa_bank_feature')

os.makedirs(archive_dir, exist_ok=True)

# 1. Move files
interview_src = os.path.join(base_dir, 'server', 'internal', 'interview')
interview_dst = os.path.join(archive_dir, 'interview')
if os.path.exists(interview_src):
    shutil.move(interview_src, interview_dst)

test_src = os.path.join(base_dir, 'testing', 'test_qa_bank.py')
test_dst = os.path.join(archive_dir, 'test_qa_bank.py')
if os.path.exists(test_src):
    shutil.move(test_src, test_dst)

# 2. Modify main.go
main_go = os.path.join(base_dir, 'server', 'cmd', 'server', 'main.go')
if os.path.exists(main_go):
    with open(main_go, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    main_content = main_content.replace('\t\"github.com/nyecov/context-engine/internal/interview\"\n', '')
    
    # Remove registrations
    main_content = main_content.replace(
        '\t// Register Tool: append_interview_qa\n\tregisterAppendInterviewQATool(s)\n\n', ''
    )
    main_content = main_content.replace(
        '\t// Register Tool: retrieve_interview_patterns\n\tregisterRetrieveInterviewPatternsTool(s)\n\n', ''
    )
    main_content = main_content.replace(
        '\t// Register Tool: prune_interview_qa\n\tregisterPruneInterviewQATool(s)\n\n', ''
    )

    # Remove function blocks
    import re
    main_content = re.sub(r'func registerAppendInterviewQATool.*?\n}\n', '', main_content, flags=re.DOTALL)
    main_content = re.sub(r'func registerRetrieveInterviewPatternsTool.*?\n}\n', '', main_content, flags=re.DOTALL)
    main_content = re.sub(r'func registerPruneInterviewQATool.*?\n}\n', '', main_content, flags=re.DOTALL)

    with open(main_go, 'w', encoding='utf-8') as f:
        f.write(main_content)

# 3. Modify webui.go
webui_go = os.path.join(base_dir, 'server', 'internal', 'webui', 'webui.go')
if os.path.exists(webui_go):
    with open(webui_go, 'r', encoding='utf-8') as f:
        webui_content = f.read()

    webui_content = webui_content.replace('\t// 2. API: QA Bank (interview_qa table)\n\tmux.HandleFunc(\"/api/qa\", handleQA)\n\n', '')
    webui_content = re.sub(r'func handleQA\(.*?}\n', '', webui_content, flags=re.DOTALL)

    with open(webui_go, 'w', encoding='utf-8') as f:
        f.write(webui_content)

# 4. Modify sqlite.go
sqlite_go = os.path.join(base_dir, 'server', 'internal', 'storage', 'sqlite.go')
if os.path.exists(sqlite_go):
    with open(sqlite_go, 'r', encoding='utf-8') as f:
        sqlite_content = f.read()

    sqlite_content = re.sub(r'\t// 3\. Interview QA Table.*?\)\n\t\t\)\n\tif err != nil {\n\t\treturn err\n\t}\n\n', '', sqlite_content, flags=re.DOTALL)

    with open(sqlite_go, 'w', encoding='utf-8') as f:
        f.write(sqlite_content)

# 5. Modify index.html
index_html = os.path.join(base_dir, 'webui', 'index.html')
if os.path.exists(index_html):
    with open(index_html, 'r', encoding='utf-8') as f:
        index_content = f.read()

    index_content = re.sub(r'\s*<!-- Left Column: QA Bank -->\s*<section id="qa-panel" class="glass-panel">.*?</section>', '', index_content, flags=re.DOTALL)

    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(index_content)

# 6. Modify app.js
app_js = os.path.join(base_dir, 'webui', 'app.js')
if os.path.exists(app_js):
    with open(app_js, 'r', encoding='utf-8') as f:
        app_content = f.read()

    app_content = app_content.replace('    loadQA();\n', '')
    app_content = app_content.replace('    setInterval(loadQA, 10000);\n', '')
    
    search_filter = '''    // Search filter
    document.getElementById('qa-search').addEventListener('input', (e) => {
        filterQA(e.target.value);
    });

'''
    app_content = app_content.replace(search_filter, '')
    
    app_content = re.sub(r'async function loadQA\(\).*?}\n\n', '', app_content, flags=re.DOTALL)
    app_content = re.sub(r'function renderQA\(.*?\).*?}\n\n', '', app_content, flags=re.DOTALL)
    app_content = re.sub(r'function filterQA\(.*?\).*?}\n\n', '', app_content, flags=re.DOTALL)

    with open(app_js, 'w', encoding='utf-8') as f:
        f.write(app_content)

# 7. Modify testing_suite_guide.md
testing_md = os.path.join(base_dir, 'references', 'testing_suite_guide.md')
if os.path.exists(testing_md):
    with open(testing_md, 'r', encoding='utf-8') as f:
        testing_content = f.read()

    testing_content = testing_content.replace('seven critical architectural pillars across 22 automated test cases', 'six critical architectural pillars across 17 automated test cases')
    testing_content = re.sub(r'7\.  \*\*QA Bank \(Interview Memory\)\*\*.*?\n\n---', '\n---', testing_content, flags=re.DOTALL)

    with open(testing_md, 'w', encoding='utf-8') as f:
        f.write(testing_content)

print('Successfully archived QA Bank feature.')
