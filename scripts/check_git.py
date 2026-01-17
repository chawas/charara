#!/usr/bin/env python3
"""
Check current GitHub setup and repository status
"""

import subprocess
import json
import os
from pathlib import Path

def check_git_status():
    """Check current git repository status"""
    print("="*80)
    print("CHECKING CURRENT GIT SETUP")
    print("="*80)
    
    project_root = Path("/home/chawas/deployed/charara")
    
    # Check if we're in a git repository
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        if result.returncode == 0 and result.stdout.strip() == 'true':
            print("✓ Already in a Git repository")
            
            # Get remote info
            remote_result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            if remote_result.stdout:
                print("\nCurrent remotes:")
                print(remote_result.stdout)
            else:
                print("✗ No remotes configured")
                
            # Get branch info
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            print(f"Current branch: {branch_result.stdout.strip()}")
            
            # Get status
            status_result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            print(f"\nGit status:\n{status_result.stdout}")
            
            return True
        else:
            print("✗ Not in a Git repository")
            return False
            
    except FileNotFoundError:
        print("✗ Git is not installed")
        return False

def check_github_username():
    """Check configured GitHub username"""
    try:
        # Check git config
        username_result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True
        )
        
        email_result = subprocess.run(
            ['git', 'config', 'user.email'],
            capture_output=True,
            text=True
        )
        
        print(f"\nGit Configuration:")
        print(f"  Name: {username_result.stdout.strip() or 'Not set'}")
        print(f"  Email: {email_result.stdout.strip() or 'Not set'}")
        
        # Check if connected to GitHub
        print(f"\nGitHub Username from config:")
        github_user = None
        
        # Try to get from remote URL
        try:
            remote_result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd="/home/chawas/deployed/charara"
            )
            
            if remote_result.returncode == 0:
                remote_url = remote_result.stdout.strip()
                print(f"  Remote URL: {remote_url}")
                
                # Extract username from URL
                if 'github.com' in remote_url:
                    if 'git@github.com:' in remote_url:
                        # SSH format: git@github.com:username/repo.git
                        github_user = remote_url.split(':')[1].split('/')[0]
                    elif 'https://github.com/' in remote_url:
                        # HTTPS format: https://github.com/username/repo.git
                        parts = remote_url.split('/')
                        if len(parts) >= 4:
                            github_user = parts[3]
                    
                    if github_user:
                        print(f"  GitHub Username: {github_user}")
                    else:
                        print(f"  Could not extract username from URL")
                else:
                    print(f"  Not a GitHub repository")
        
        except:
            pass
        
        return github_user or username_result.stdout.strip()
        
    except Exception as e:
        print(f"Error checking GitHub username: {e}")
        return None

def check_existing_repos():
    """Check for existing Lake Kariba repositories on GitHub"""
    print("\n" + "="*80)
    print("CHECKING EXISTING GITHUB REPOSITORIES")
    print("="*80)
    
    # Common repository names for this project
    possible_repo_names = [
        'lake-kariba-wind-analysis',
        'kariba-wind-analysis',
        'charara-wind-analysis',
        'floating-solar-wind',
        'wind-analysis',
        'charara',
        'lake-kariba'
    ]
    
    print("Checking for existing repositories with similar names...")
    print("(You can check manually at: https://github.com/chawas?tab=repositories)")
    
    for repo in possible_repo_names:
        print(f"  https://github.com/chawas/{repo}")
    
    return possible_repo_names

def suggest_repository_name():
    """Suggest a repository name based on existing repos"""
    print("\n" + "="*80)
    print("REPOSITORY NAME SUGGESTIONS")
    print("="*80)
    
    suggestions = [
        {
            'name': 'lake-kariba-wind-analysis',
            'description': 'Clear and descriptive',
            'recommended': True
        },
        {
            'name': 'kariba-floating-solar-wind',
            'description': 'Focus on floating solar application',
            'recommended': False
        },
        {
            'name': 'charara-wind-patterns',
            'description': 'Specific to Charara location',
            'recommended': False
        },
        {
            'name': 'wind-analysis-toolkit',
            'description': 'More general tool name',
            'recommended': False
        }
    ]
    
    for suggestion in suggestions:
        star = "⭐" if suggestion['recommended'] else "  "
        print(f"{star} {suggestion['name']:30} - {suggestion['description']}")
    
    return suggestions

def main():
    """Main function to check current setup"""
    print("\n" + "="*80)
    print("GITHUB SETUP ANALYSIS")
    print("="*80)
    print(f"Checking project at: /home/chawas/deployed/charara")
    print(f"GitHub username: chawas")
    print("="*80)
    
    # Check current git status
    git_status = check_git_status()
    
    # Check GitHub username
    username = check_github_username()
    if username and username.lower() != 'chawas':
        print(f"\n⚠ Warning: Git configured as '{username}', but GitHub username is 'chawas'")
        print("You might want to update your git config:")
        print(f"  git config user.name 'chawas'")
    
    # Check existing repositories
    existing_repos = check_existing_repos()
    
    # Suggest repository name
    suggestions = suggest_repository_name()
    
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    if git_status:
        print("\n✅ Your project is already a Git repository.")
        print("\nNext steps:")
        print("1. Check if you want to use an existing repository or create new")
        print("2. Add/update remote to GitHub")
        print("3. Commit any uncommitted changes")
        print("4. Push to GitHub")
    else:
        print("\n⚡ Your project is not a Git repository yet.")
        print("\nNext steps:")
        print("1. Initialize Git repository: git init")
        print("2. Add GitHub remote")
        print("3. Create .gitignore")
        print("4. Make initial commit")
    
    print("\nRun the setup script to automate these steps:")
    print("python scripts/setup_existing_github.py")

if __name__ == "__main__":
    main()