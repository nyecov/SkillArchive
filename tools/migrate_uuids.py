import os
import uuid
import re
import yaml

def inject_uuid(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        print(f"  [SKIP] No frontmatter: {file_path}")
        return False

    fm_content = fm_match.group(1)
    try:
        data = yaml.safe_load(fm_content)
        if not data: data = {}
        
        if 'id' in data:
            print(f"  [SKIP] Already has ID: {data['id']} at {file_path}")
            return False
        
        new_id = str(uuid.uuid4())
        # Add id at the top for visibility
        new_fm = f"id: {new_id}\n{fm_content}"
        
        new_content = content.replace(f"---\n{fm_content}\n---", f"---\n{new_id_block(new_id, fm_content)}\n---", 1)
        
        # Better replacement to avoid nested --- issues
        full_new_content = re.sub(r'^---\s*\n.*?\n---\s*\n', f'---\nid: {new_id}\n{fm_content}\n---\n', content, flags=re.DOTALL)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_new_content)
        
        print(f"  [OK] Injected {new_id} -> {file_path}")
        return True
    except Exception as e:
        print(f"  [ERROR] Processing {file_path}: {e}")
        return False

def new_id_block(uid, old_fm):
    return f"id: {uid}\n{old_fm}"

def main():
    skills_dir = "skills"
    workflows_dir = "workflows"
    
    print("Processing Skills...")
    for root, dirs, files in os.walk(skills_dir):
        for file in files:
            if file == "SKILL.md":
                inject_uuid(os.path.join(root, file))
                
    print("\nProcessing Workflows...")
    for file in os.listdir(workflows_dir):
        if file.endswith(".md"):
            inject_uuid(os.path.join(workflows_dir, file))

if __name__ == "__main__":
    main()
