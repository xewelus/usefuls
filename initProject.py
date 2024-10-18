import os
import subprocess

folder_path = os.getcwd()  # Use the current working directory directly
# Check if the .git directory already exists
git_dir = os.path.join(folder_path, '.git')
print(f"Checking for existing Git repository at: {git_dir}")  # Debugging line
if os.path.isdir(git_dir):
    print("Git repository already exists.")
else:
    # Initialize a new git repository
    subprocess.run(["git", "init"], check=True)

# create .gitignore file if not exists
if not os.path.exists(os.path.join(folder_path, '.gitignore')):
    with open(os.path.join(folder_path, '.gitignore'), 'w') as f:
        f.write("*.pyc\n__pycache__\n") 

# commit all changes
subprocess.run(["git", "add", "."], check=True)

# Check if there are changes to commit
try:
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
except subprocess.CalledProcessError:
    print("No changes to commit.")

# check if remote origin already exists
try:
    subprocess.run(["git", "remote", "get-url", "origin"], check=True)
    print("Remote 'origin' already exists. No need to prompt for GitHub login.")
    login = None  # Set login to None to skip the prompt
except subprocess.CalledProcessError:
    login = input("Enter your GitHub login to add the repository, or leave empty to not add: ").strip()

if login:
    print(f"Adding repository to GitHub for user: {login}")
    repo_name = os.path.basename(folder_path)  # Extract the repository name from the folder path
    repo_url = f"https://github.com/{login}/{repo_name}.git"  # Use the repository name instead of the full path
    print(f"Repository URL: {repo_url}")

    # Check if the repository exists
    response = subprocess.run(["curl", "-s", f"https://api.github.com/repos/{login}/{repo_name}"], capture_output=True)
    if response.returncode == 0 and b'"message": "Not Found"' not in response.stdout:
        print("Repository already exists on GitHub.")
    else:
        create_repo = input("Repository does not exist. Would you like to create it? (y/n): ").strip().lower()
        if create_repo == 'y':
            subprocess.run(["curl", "-u", f"{login}", "-X", "POST", "https://api.github.com/user/repos", "-d", f'{{"name": "{repo_name}", "private": true}}'], check=True)
            print("Private repository created successfully.")

    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

    # push to remote origin
    print("Pushing to remote origin...")
    subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
    print("Done.")
