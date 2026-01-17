#!/usr/bin/env python3
"""
GitHub Setup Script - No syntax errors
Simple and clean version
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success"""
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                              capture_output=True, text=True, cwd=cwd)
        print(f"✓ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {cmd}")
        print(f"  Error: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("GITHUB SETUP FOR LAKE KARIBA PROJECT")
    print("=" * 60)
    
    # Set project directory
    project_dir = Path("/home/chawas/deployed/charara")
    os.chdir(project_dir)
    
    print(f"Project directory: {project_dir}")
    
    # Ask for repository name
    repo_name = input("\nGitHub repository name: ").strip()
    if not repo_name:
        repo_name = "lake-kariba-wind-analysis"
    
    print(f"\nRepository will be: https://github.com/chawas/{repo_name}")
    
    # Step 1: Initialize Git
    print("\n" + "="*60)
    print("STEP 1: INITIALIZING GIT")
    print("="*60)
    
    if not (project_dir / ".git").exists():
        run_command("git init")
    else:
        print("✓ Git already initialized")
    
    # Configure Git
    run_command('git config user.name "chawas"')
    
    # Check email
    email_check = subprocess.run("git config user.email", 
                                shell=True, capture_output=True, text=True)
    if not email_check.stdout.strip():
        run_command('git config user.email "chawas@users.noreply.github.com"')
    
    # Step 2: Create .gitignore
    print("\n" + "="*60)
    print("STEP 2: CREATING .gitignore")
    print("="*60)
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class

# Data files
data/era5_downloads/*.nc
data/era5_downloads/*.nc4
output/
logs/

# IDE
.vscode/
.idea/

# OS
.DS_Store
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")
    
    # Step 3: Create README.md
    print("\n" + "="*60)
    print("STEP 3: CREATING README.md")
    print("="*60)
    
    # Create README without f-string issues
    readme_lines = [
        "# Lake Kariba Wind Analysis",
        "",
        "Wind analysis for floating solar panels at Charara area, Lake Kariba.",
        "",
        "## Features",
        "- Seasonal wind pattern analysis",
        "- Time series visualization",
        "- Statistical analysis and reporting",
        "- Automated documentation",
        "",
        "## Quick Start",
        "```bash",
        "# Install dependencies",
        "pip install -r scripts/requirements.txt",
        "",
        "# Run analysis",
        "python scripts/run_analysis.py",
        "```",
        "",
        f"## Repository",
        f"https://github.com/chawas/{repo_name}",
        "",
        "## License",
        "MIT License"
    ]
    
    with open("README.md", "w") as f:
        f.write("\n".join(readme_lines))
    print("✓ Created README.md")
    
    # Step 4: Add and commit
    print("\n" + "="*60)
    print("STEP 4: COMMITTING FILES")
    print("="*60)
    
    run_command("git add .")
    
    commit_msg = f"""Initial commit: Lake Kariba Wind Analysis

Repository: https://github.com/chawas/{repo_name}
Project: Wind analysis for floating solar panels
Location: Charara area, Lake Kariba
"""
    
    run_command(f'git commit -m "{commit_msg}"')
    
    # Step 5: Create repository on GitHub
    print("\n" + "="*60)
    print("STEP 5: CREATE GITHUB REPOSITORY")
    print("="*60)
    
    print(f"\nPlease create the repository on GitHub:")
    print(f"1. Go to: https://github.com/new")
    print(f"2. Repository name: {repo_name}")
    print(f"3. Description: Wind analysis for floating solar at Lake Kariba")
    print(f"4. Choose Public or Private")
    print(f"5. DO NOT initialize with README, .gitignore, or license")
    print(f"6. Click 'Create repository'")
    
    input("\nPress Enter AFTER creating the repository on GitHub...")
    
    # Step 6: Add remote and push
    print("\n" + "="*60)
    print("STEP 6: PUSHING TO GITHUB")
    print("="*60)
    
    # Add remote
    remote_url = f"https://github.com/chawas/{repo_name}.git"
    run_command(f"git remote add origin {remote_url}")
    
    # Rename branch
    run_command("git branch -M main")
    
    # Push
    print("\nPushing to GitHub...")
    print("You may be asked for GitHub credentials")
    success = run_command("git push -u origin main")
    
    if success:
        print(f"\n✅ SUCCESS!")
        print(f"Your code is now on GitHub:")
        print(f"https://github.com/chawas/{repo_name}")
    else:
        print("\n⚠ Push failed. Common issues:")
        print("1. Repository not created yet")
        print("2. Need GitHub token for authentication")
        print("\nYou can manually push later with:")
        print(f"  git push -u origin main")
    
    # Step 7: Create GitHub Actions
    print("\n" + "="*60)
    print("STEP 7: GITHUB ACTIONS (Optional)")
    print("="*60)
    
    create_actions = input("\nCreate GitHub Actions workflow? (y/n): ").lower()
    if create_actions == 'y':
        # Create .github directory
        github_dir = project_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r scripts/requirements.txt
    - name: Test configuration
      run: |
        python -c "import sys; sys.path.append('scripts'); print('Setup test passed')"
"""
        
        workflow_file = github_dir / "ci.yml"
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)
        
        print("✓ Created GitHub Actions workflow")
        
        # Commit and push workflow
        run_command("git add .github/")
        run_command('git commit -m "Add GitHub Actions workflow"')
        run_command("git push")
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    print(f"\nYour project is ready!")
    print(f"Repository: https://github.com/chawas/{repo_name}")
    print("\nNext steps:")
    print("1. Visit your repository")
    print("2. Check the Actions tab (if created)")
    print("3. Add repository topics")
    print("4. Share with collaborators")
    
    # Save setup info
    summary = f"""GitHub Setup Summary
Repository: https://github.com/chawas/{repo_name}
Created: {subprocess.run('date', capture_output=True, text=True).stdout}

Files created:
- .gitignore
- README.md
- GitHub Actions workflow (if selected)

Local commands:
git add .
git commit -m "Message"
git push
git pull origin main
"""
    
    with open("GITHUB_SETUP_SUMMARY.txt", "w") as f:
        f.write(summary)
    
    print(f"\n✓ Summary saved to: {project_dir}/GITHUB_SETUP_SUMMARY.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)