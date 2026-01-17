#!/usr/bin/env python3
"""
Fixed GitHub setup script - no syntax errors
"""

import os
import sys
import subprocess
from pathlib import Path

def run_cmd(cmd, desc=None):
    """Run command and show status"""
    if desc:
        print(f"\n{desc}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if desc:
            print(f"✓ {desc}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        if desc:
            print(f"✗ {desc} failed")
        print(f"Error: {e.stderr}")
        return False, e.stderr

def main():
    print("=" * 80)
    print("GITHUB SETUP FOR chawas")
    print("=" * 80)
    
    project_dir = Path("/home/chawas/deployed/charara")
    os.chdir(project_dir)
    
    # Ask for repo name
    repo_name = input("GitHub repository name (default: lake-kariba-wind-analysis): ").strip()
    if not repo_name:
        repo_name = "lake-kariba-wind-analysis"
    
    print(f"\nWill create: https://github.com/chawas/{repo_name}")
    
    # Step 1: Check Git
    print("\n" + "="*80)
    print("STEP 1: CHECKING GIT")
    print("="*80)
    
    # Check if Git is installed
    run_cmd("git --version", "Checking Git installation")
    
    # Initialize Git if needed
    if not (project_dir / ".git").exists():
        run_cmd("git init", "Initializing Git repository")
    else:
        print("✓ Git already initialized")
    
    # Configure Git
    run_cmd('git config user.name "chawas"', "Setting Git username")
    
    # Check email
    success, email = run_cmd("git config user.email")
    if not success or not email.strip():
        run_cmd('git config user.email "chawas@users.noreply.github.com"', "Setting Git email")
    
    # Step 2: Create essential files
    print("\n" + "="*80)
    print("STEP 2: CREATING FILES")
    print("="*80)
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*.pyc

# Data files
data/era5_downloads/*.nc
data/era5_downloads/*.nc4
output/
logs/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
"""
    
    gitignore_path = project_dir / ".gitignore"
    if not gitignore_path.exists():
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print("✓ Created .gitignore")
    else:
        print("✓ .gitignore already exists")
    
    # Create README.md
    readme_content = f"""# Lake Kariba Wind Analysis

Wind analysis for floating solar panels at Charara area, Lake Kariba.

## Features
- Seasonal wind pattern analysis
- Time series visualization
- Statistical analysis
- Automated documentation

## Quick Start
```bash
pip install -r scripts/requirements.txt
python scripts/run_analysis.py