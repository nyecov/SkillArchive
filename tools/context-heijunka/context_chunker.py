import os
import argparse
import fnmatch

# A simple heuristic: 4 chars is roughly 1 token.
DEFAULT_MAX_CHARS = 20000  # ~5000 tokens

DEFAULT_IGNORE = [
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "*.pyc", "*.jpg", "*.png", "*.gif", "*.ico", "*.pdf", "*.zip", "*.tar.gz"
]

def is_ignored(path, ignore_patterns):
    name = os.path.basename(path)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def collect_files(source_dir, ignore_patterns):
    collected = []
    for root, dirs, files in os.walk(source_dir):
        # Filter directories in-place to avoid walking ignored dirs
        dirs[:] = [d for d in dirs if d not in ignore_patterns and not is_ignored(d, ignore_patterns)]
        
        for file in files:
            if not is_ignored(file, ignore_patterns):
                collected.append(os.path.join(root, file))
    return collected

def create_mission_brief(chunk_id, files_data, out_dir):
    brief_content = f"""# Swarm Mission Brief: Chunk {chunk_id}

## Objective
Analyze the provided file contents to identify any logic, patterns, or tools that could be synthesized into a new Agentic Skill. Focus on extracting methodologies, Poka-yokes (mistake-proofing), and architectural best practices.

## Instructions
1. Review each file carefully.
2. Identify if it contains a procedural workflow or a useful prompt technique.
3. Summarize findings and determine if this chunk warrants full synthesis into the Skill Archive.
4. Output your analysis using the Hō-Ren-Sō (Report) format.

---
## Source Files

"""
    for file_path, content in files_data:
        brief_content += f"### File: `{file_path}`
"
        brief_content += "```text
"
        brief_content += content + "
"
        brief_content += "```

"
        
    out_file = os.path.join(out_dir, f"mission_brief_{chunk_id:03d}.md")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(brief_content)
    print(f"Created {out_file} ({len(brief_content)} chars)")

def main():
    parser = argparse.ArgumentParser(description="Context Heijunka: Chunk a repository into manageable Swarm Mission Briefs.")
    parser.add_argument("--source", required=True, help="Source directory to analyze.")
    parser.add_argument("--out", required=True, help="Output directory for Mission Briefs.")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS, help="Max characters per chunk.")
    
    args = parser.parse_args()
    
    source_dir = os.path.abspath(args.source)
    out_dir = os.path.abspath(args.out)
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    all_files = collect_files(source_dir, DEFAULT_IGNORE)
    
    current_chunk = 1
    current_chars = 0
    current_files = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            file_chars = len(content)
            
            # If a single file is too large, we might need to chunk it further, but for simplicity, 
            # we'll allow it to push the chunk over the limit, then immediately cut a new chunk.
            if current_chars + file_chars > args.max_chars and current_files:
                create_mission_brief(current_chunk, current_files, out_dir)
                current_chunk += 1
                current_chars = 0
                current_files = []
                
            current_files.append((os.path.relpath(file_path, source_dir), content))
            current_chars += file_chars
            
        except Exception as e:
            print(f"Skipping {file_path} due to error: {e}")
            
    if current_files:
        create_mission_brief(current_chunk, current_files, out_dir)

if __name__ == "__main__":
    main()
