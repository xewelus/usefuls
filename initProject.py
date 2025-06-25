import os
import subprocess
import json
import re

def get_github_username():
    """Get GitHub username from environment variable (required)"""
    username = os.getenv('GITHUB_USERNAME')
    if not username:
        print("❌ ERROR: GITHUB_USERNAME environment variable is not set!")
        print("🔧 Please set it with one of these methods:")
        print("   PowerShell: [Environment]::SetEnvironmentVariable('GITHUB_USERNAME', 'your-username', 'User')")
        print("   CMD: setx GITHUB_USERNAME your-username")
        print("   Or restart your terminal after setting it")
        exit(1)
    return username

def validate_repo_name(name):
    """Validate GitHub repository name"""
    if not name:
        return False, "Repository name cannot be empty"
    
    if len(name) > 100:
        return False, "Repository name cannot be longer than 100 characters"
    
    # GitHub repository name rules
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        return False, "Repository name can only contain letters, numbers, dots, hyphens, and underscores"
    
    if name.startswith('.') or name.startswith('-'):
        return False, "Repository name cannot start with a dot or hyphen"
    
    if name.endswith('.') or name.endswith('-'):
        return False, "Repository name cannot end with a dot or hyphen"
    
    return True, ""

def create_github_repo(repo_name, private=True):
    """Create GitHub repository using gh CLI"""
    try:
        visibility = "private" if private else "public"
        subprocess.run(["gh", "repo", "create", repo_name, f"--{visibility}", "--source=.", "--remote=origin", "--push"], check=True)
        print(f"✅ Repository '{repo_name}' created and pushed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create repository: {e}")
        return False

def main():
    folder_path = os.getcwd()
    default_repo_name = os.path.basename(folder_path)
    
    print(f"🚀 Initializing project in: {folder_path}")
    print(f"📂 Default repository name: {default_repo_name}")
    
    # Ask for repository name with validation
    while True:
        user_repo_name = input(f"📝 Repository name (press Enter for '{default_repo_name}'): ").strip()
        repo_name = user_repo_name if user_repo_name else default_repo_name
        
        is_valid, error_msg = validate_repo_name(repo_name)
        if is_valid:
            break
        else:
            print(f"❌ {error_msg}")
            print("💡 Please try again")
    
    print(f"✅ Using repository name: {repo_name}")
    
    # Show a note if repo name differs from folder name
    if repo_name != default_repo_name:
        print(f"📝 Note: Repository name '{repo_name}' differs from folder name '{default_repo_name}'")
    
    # Check if the .git directory already exists
    git_dir = os.path.join(folder_path, '.git')
    if os.path.isdir(git_dir):
        print("📁 Git repository already exists.")
    else:
        print("🔧 Initializing Git repository...")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)  # Use 'main' instead of 'master'

    # Create .gitignore file if not exists
    gitignore_path = os.path.join(folder_path, '.gitignore')
    if not os.path.exists(gitignore_path):
        print("📝 Creating .gitignore file...")
        with open(gitignore_path, 'w') as f:
            f.write("# Python\n*.pyc\n__pycache__/\n*.pyo\n*.pyd\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\n\n# Virtual Environment\nvenv/\nenv/\nENV/\n\n# IDE\n.vscode/\n.idea/\n*.swp\n*.swo\n*~\n\n# OS\n.DS_Store\nThumbs.db\n\n# Logs\n*.log\n")

    # Add and commit changes
    print("💾 Adding and committing changes...")
    subprocess.run(["git", "add", "."], check=True)
    
    # Check if there are changes to commit
    try:
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        print("✅ Initial commit created")
    except subprocess.CalledProcessError:
        print("ℹ️  No changes to commit")

    # Check if remote origin already exists
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, check=True)
        print("🔗 Remote 'origin' already exists")
        print("🚀 Pushing to existing remote...")
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✅ Pushed to remote successfully!")
        return
    except subprocess.CalledProcessError:
        pass  # Remote doesn't exist, continue

    # Get GitHub username (will exit if not set)
    username = get_github_username()
    print(f"👤 GitHub username: {username}")
    
    # Check if user wants to create repository
    create_repo = input(f"🤔 Create GitHub repository '{repo_name}'? (Y/n): ").strip().lower()
    if create_repo in ['', 'y', 'yes']:
        private_repo = input("🔒 Make repository private? (Y/n): ").strip().lower()
        is_private = private_repo in ['', 'y', 'yes']
        
        if create_github_repo(repo_name, is_private):
            print("🎉 Project initialization completed successfully!")
        else:
            print("❌ Failed to create GitHub repository")
    else:
        print("⏭️  Skipping GitHub repository creation")
        print("✅ Local Git repository initialized")

if __name__ == "__main__":
    main()
