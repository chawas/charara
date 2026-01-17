#!/usr/bin/env python3
"""
Setup script for existing GitHub user (chawas)
Configures repository and pushes to GitHub
"""

import os
import sys
import json
import subprocess
import getpass
from pathlib import Path
from datetime import datetime

class ExistingGitHubSetup:
    """Setup for existing GitHub user"""
    
    def __init__(self):
        self.project_root = Path("/home/chawas/deployed/charara")
        self.github_username = "chawas"
        
        # Try to detect repository name from config
        self.repo_name = self.detect_repository_name()
        
        # Load existing config
        config_file = self.project_root / "scripts" / "config.json"
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        print(f"\n{'='*80}")
        print(f"GITHUB SETUP FOR USER: {self.github_username}")
        print(f"{'='*80}")
    
    def detect_repository_name(self):
        """Detect or ask for repository name"""
        # Check if .git exists and has remote
        git_dir = self.project_root / ".git"
        
        if git_dir.exists():
            try:
                # Check remote URL
                result = subprocess.run(
                    ['git', 'remote', 'get-url', 'origin'],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root
                )
                
                if result.returncode == 0 and result.stdout:
                    remote_url = result.stdout.strip()
                    # Extract repo name from URL
                    if 'github.com' in remote_url:
                        if '/' in remote_url:
                            repo_part = remote_url.rstrip('.git').split('/')[-1]
                            print(f"✓ Detected repository from remote: {repo_part}")
                            return repo_part
            
            except:
                pass
        
        # Ask user for repository name
        print("\nChoose a repository name for GitHub:")
        print("(This will create: https://github.com/chawas/YOUR_REPO_NAME)")
        
        suggestions = [
            "lake-kariba-wind-analysis",
            "kariba-floating-solar-wind",
            "charara-wind-analysis",
            "wind-analysis-toolkit"
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        
        print(f"\nOr enter your own name.")
        
        while True:
            choice = input(f"\nEnter choice (1-{len(suggestions)}) or custom name: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                repo_name = suggestions[int(choice) - 1]
                break
            elif choice:
                # Custom name
                repo_name = choice.lower().replace(' ', '-')
                # Validate name
                if all(c.isalnum() or c in ['-', '_', '.'] for c in repo_name):
                    break
                else:
                    print("Invalid repository name. Use only letters, numbers, hyphens, underscores, and dots.")
            else:
                print("Please enter a repository name.")
        
        return repo_name
    
    def check_and_configure_git(self):
        """Check and configure Git settings"""
        print("\n" + "="*80)
        print("CONFIGURING GIT")
        print("="*80)
        
        # Check if git is installed
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
            print("✓ Git is installed")
        except:
            print("✗ Git is not installed")
            print("\nInstall Git with:")
            print("  Ubuntu/Debian: sudo apt install git")
            print("  macOS: brew install git")
            print("  Windows: Download from https://git-scm.com/")
            return False
        
        # Configure git user if not set
        current_name = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        current_email = subprocess.run(
            ['git', 'config', 'user.email'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        if not current_name or current_name != self.github_username:
            print(f"\nSetting Git user name to: {self.github_username}")
            subprocess.run(['git', 'config', 'user.name', self.github_username], check=True)
        
        if not current_email:
            # Suggest email based on GitHub username
            suggested_email = f"{self.github_username}@users.noreply.github.com"
            print(f"\nGit email is not set.")
            print(f"GitHub suggests using: {suggested_email}")
            print("Or use your actual email if you want commits linked to your GitHub account.")
            
            set_email = input(f"Set email to '{suggested_email}'? (y/n): ").lower()
            if set_email == 'y':
                subprocess.run(['git', 'config', 'user.email', suggested_email], check=True)
                print(f"✓ Email set to: {suggested_email}")
            else:
                email = input("Enter your email: ").strip()
                if email:
                    subprocess.run(['git', 'config', 'user.email', email], check=True)
                    print(f"✓ Email set to: {email}")
        
        return True
    
    def initialize_git_repository(self):
        """Initialize Git repository if not already"""
        print("\n" + "="*80)
        print("INITIALIZING GIT REPOSITORY")
        print("="*80)
        
        git_dir = self.project_root / ".git"
        
        if git_dir.exists():
            print("✓ Git repository already exists")
            return True
        
        try:
            # Initialize git
            subprocess.run(['git', 'init'], cwd=self.project_root, check=True)
            print("✓ Git repository initialized")
            
            # Create .gitignore if not exists
            self.create_gitignore()
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error initializing Git: {e}")
            return False
    
    def create_gitignore(self):
        """Create .gitignore file"""
        gitignore_path = self.project_root / ".gitignore"
        
        if gitignore_path.exists():
            print("✓ .gitignore already exists")
            return True
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
env/
venv/
ENV/
env.bak/
venv.bak/

# Project data (large files)
data/era5_downloads/*.nc
data/era5_downloads/*.nc4
output/**/*
!output/README.md

# Logs
logs/*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
temp/
tmp/
*.tmp
*.temp

# Documentation build
docs/_build/

# Large files
*.hdf5
*.h5
*.mat
*.dat
*.bin
"""
        
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        
        print("✓ Created .gitignore file")
        
        # Create README files in output directories
        self.create_output_readmes()
        
        return True
    
    def create_output_readmes(self):
        """Create README files in output directories"""
        readme_content = """# Generated Output Directory

This directory contains automatically generated analysis outputs.

## Contents
- Wind maps and visualizations
- Time series plots
- Statistical analysis results
- Reports and documentation

## Notes
- Files are generated by the analysis scripts
- Do not edit these files directly
- Regenerate to update outputs

## Git Ignored
This directory is ignored by Git to avoid committing large files.
"""
        
        output_dirs = [
            self.project_root / "output",
            self.project_root / "output" / "wind_maps",
            self.project_root / "output" / "timeseries",
            self.project_root / "output" / "statistics",
            self.project_root / "output" / "reports",
            self.project_root / "logs"
        ]
        
        for dir_path in output_dirs:
            if dir_path.exists():
                readme_path = dir_path / "README.md"
                if not readme_path.exists():
                    with open(readme_path, 'w') as f:
                        f.write(readme_content)
        
        print("✓ Created README files in output directories")
    
    def setup_github_remote(self):
        """Setup GitHub remote repository"""
        print("\n" + "="*80)
        print("SETTING UP GITHUB REMOTE")
        print("="*80)
        
        repo_url_ssh = f"git@github.com:{self.github_username}/{self.repo_name}.git"
        repo_url_https = f"https://github.com/{self.github_username}/{self.repo_name}.git"
        
        print(f"Repository: {self.repo_name}")
        print(f"SSH URL: {repo_url_ssh}")
        print(f"HTTPS URL: {repo_url_https}")
        
        # Check if remote already exists
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                current_remote = result.stdout.strip()
                print(f"\n✓ Remote 'origin' already exists: {current_remote}")
                
                if current_remote != repo_url_ssh and current_remote != repo_url_https:
                    change = input(f"\nRemote points to different URL. Change to new repository? (y/n): ").lower()
                    if change == 'y':
                        subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url_ssh], 
                                     cwd=self.project_root, check=True)
                        print(f"✓ Updated remote to: {repo_url_ssh}")
                return True
        
        except subprocess.CalledProcessError:
            pass  # Remote doesn't exist
        
        # Ask which URL to use
        print("\nChoose remote URL type:")
        print("1. SSH (requires SSH keys setup - recommended)")
        print("2. HTTPS (requires username/password or token)")
        
        while True:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                remote_url = repo_url_ssh
                print("Using SSH URL")
                break
            elif choice == '2':
                remote_url = repo_url_https
                print("Using HTTPS URL")
                break
            else:
                print("Invalid choice")
        
        # Add remote
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], 
                         cwd=self.project_root, check=True)
            print(f"✓ Added remote 'origin': {remote_url}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error adding remote: {e}")
            return False
    
    def create_initial_commit(self):
        """Create initial commit if needed"""
        print("\n" + "="*80)
        print("CREATING INITIAL COMMIT")
        print("="*80)
        
        # Check if there are any commits
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '-1'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0 and result.stdout.strip():
                print("✓ Repository already has commits")
                return True
        
        except:
            pass
        
        # Check for uncommitted changes
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if not status_result.stdout.strip():
            print("No changes to commit")
            
            # Add README and other files
            self.add_initial_files()
            
            # Check again
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
        
        if status_result.stdout.strip():
            print("Staging files...")
            subprocess.run(['git', 'add', '.'], cwd=self.project_root, check=True)
            
            start_year = self.config.get('analysis_period', {}).get('start_year', 'N/A')
            end_year = self.config.get('analysis_period', {}).get('end_year', 'N/A')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            commit_message = f"""Initial commit: Lake Kariba Wind Analysis

Project: Wind analysis for floating solar panels at Lake Kariba
Location: Charara area (16.53°S, 28.83°E)
Analysis Period: {start_year}-{end_year}
Repository: https://github.com/{self.github_username}/{self.repo_name}

Features:
- Seasonal wind pattern analysis
- Time series and statistical analysis
- Automated documentation generation
- Configuration management
- GitHub integration

Generated: {timestamp}
"""
            
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         cwd=self.project_root, check=True)
            print("✓ Created initial commit")
            return True
        else:
            print("No files to commit")
            return False
    
    def add_initial_files(self):
        """Add initial project files if needed"""
        print("Adding initial project files...")
        
        # Ensure key files exist
        files_to_check = [
            'README.md',
            'scripts/config.json',
            'scripts/requirements.txt'
        ]
        
        for file_path in files_to_check:
            full_path = self.project_root / file_path
            if not full_path.exists():
                print(f"⚠ Warning: {file_path} does not exist")
    
    def push_to_github(self):
        """Push to GitHub"""
        print("\n" + "="*80)
        print("PUSHING TO GITHUB")
        print("="*80)
        
        # Check if repository exists on GitHub
        print(f"Checking if repository exists: {self.repo_name}")
        print(f"Visit: https://github.com/{self.github_username}/{self.repo_name}")
        
        exists = input(f"\nDoes the repository exist on GitHub? (y/n): ").lower()
        
        if exists != 'y':
            print(f"\nCreate the repository first:")
            print(f"1. Go to: https://github.com/new")
            print(f"2. Repository name: {self.repo_name}")
            print(f"3. Description: Wind analysis for floating solar at Lake Kariba")
            print(f"4. Choose 'Public' or 'Private'")
            print(f"5. DO NOT initialize with README, .gitignore, or license")
            print(f"6. Click 'Create repository'")
            
            input("\nPress Enter after creating the repository...")
        
        # Push to GitHub
        try:
            print("\nPushing to GitHub...")
            
            # Rename branch to main if needed
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            current_branch = branch_result.stdout.strip()
            if current_branch != 'main':
                subprocess.run(['git', 'branch', '-M', 'main'], 
                             cwd=self.project_root, check=True)
                print("✓ Renamed branch to 'main'")
            
            # Push with set-upstream
            print("Running: git push -u origin main")
            result = subprocess.run(
                ['git', 'push', '-u', 'origin', 'main'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print("✅ Successfully pushed to GitHub!")
                print(f"Repository URL: https://github.com/{self.github_username}/{self.repo_name}")
                return True
            else:
                print(f"✗ Push failed: {result.stderr}")
                
                # Try to diagnose
                if "Permission denied" in result.stderr:
                    print("\nSSH Permission denied. Try:")
                    print("1. Use HTTPS URL instead: git remote set-url origin https://github.com/...")
                    print("2. Setup SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh")
                
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Error pushing to GitHub: {e}")
            return False
    
    def generate_github_files(self):
        """Generate GitHub-specific files"""
        print("\n" + "="*80)
        print("GENERATING GITHUB FILES")
        print("="*80)
        
        # Create .github directory
        github_dir = self.project_root / ".github"
        workflows_dir = github_dir / "workflows"
        issue_template_dir = github_dir / "ISSUE_TEMPLATE"
        
        github_dir.mkdir(exist_ok=True)
        workflows_dir.mkdir(parents=True, exist_ok=True)
        issue_template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create GitHub Actions workflow
        workflow_content = """name: Python Analysis CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r scripts/requirements.txt
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 scripts/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 scripts/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test configuration
      run: |
        python -c "import sys; sys.path.append('scripts'); from config_manager import ConfigManager; c = ConfigManager(); print('Config loaded successfully')"
    
    - name: Test documentation generation
      run: |
        cd scripts
        python auto_documentation.py
        echo "Documentation generated in docs/"
"""
        
        workflow_file = workflows_dir / "python-ci.yml"
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)
        print("✓ Created GitHub Actions workflow")
        
        # Create simple issue templates
        bug_template = """---
name: Bug Report
about: Report a bug in the wind analysis
title: '[BUG] '
labels: bug
---

**Describe the bug**

**To Reproduce**

**Expected behavior**

**Screenshots**

**Environment:**
"""
        
        with open(issue_template_dir / "bug_report.md", 'w') as f:
            f.write(bug_template)
        
        print("✓ Created issue templates")
        
        # Create README.md if not exists
        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            repo_url = f"https://github.com/{self.github_username}/{self.repo_name}"
            
            readme_content = f"""# Lake Kariba Wind Analysis

Wind analysis for floating solar panels at Charara area, Lake Kariba.

## Features
- Seasonal wind pattern analysis
- Time series visualization
- Statistical analysis and reporting
- Automated documentation
- GitHub Actions CI/CD

## Quick Start
```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run analysis
python scripts/run_analysis.py

# Generate documentation
python scripts/auto_documentation.py