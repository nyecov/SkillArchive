import subprocess
import sys

def run_script(script_name):
    print(f"\n{'='*50}")
    print(f"🚀 Running: {script_name}")
    print(f"{'='*50}")
    
    import os
    script_path = os.path.join("tools", script_name)
    result = subprocess.run([sys.executable, script_path], capture_output=False)
    
    if result.returncode != 0:
        print(f"\n❌ [ERROR] {script_name} failed with exit code {result.returncode}.")
        print("Halting orchestration pipeline.")
        sys.exit(result.returncode)
    else:
        print(f"✅ [SUCCESS] {script_name} completed.")

def main():
    print("Starting Skill Archive Orchestration Pipeline (VSM Optimized)\n")
    
    # 1. Poka-yoke: Validate all frontmatter and schema compliance
    run_script("validate_frontmatter.py")
    
    # 2. Check inner references
    run_script("check_refs.py")
    
    # 3. Update discovery metadata
    run_script("update_metadata.py")
    
    # 4. Generate README documentation
    run_script("generate_readme.py")
    
    # 5. Sync allowed skills to the working `.gemini/skills` directory
    run_script("sync_skills.py")
    
    # 6. Sync workflows to the working `.gemini/workflows` directory
    run_script("sync_workflows.py")

    print(f"\n{'='*50}")
    print("🎉 Pipeline completed successfully!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
