#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

def main():
    # Check if at least two arguments are provided
    if len(sys.argv) < 3:
        print("Usage: {} <source-directory-path> <destination-directory-path> [branch-name]".format(sys.argv[0]))
        sys.exit(1)

    # Assign arguments to variables
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]
    branch_name = sys.argv[3] if len(sys.argv) > 3 else 'gh-pages'

    # Check if the source directory exists
    if not os.path.isdir(source_directory):
        print(f"Error: Source directory {source_directory} does not exist.")
        sys.exit(1)

    # Check if the destination directory exists
    if not os.path.isdir(destination_directory):
        print(f"Error: Destination directory {destination_directory} does not exist.")
        sys.exit(1)

    # Save the current branch name
    try:
        current_branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=destination_directory).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        print("Error: Failed to get the current branch name.")
        sys.exit(1)

    print(f"Current branch: {current_branch}")

    # Create a temporary directory inside the destination directory
    tmp_content = os.path.join(destination_directory, 'tmp_content')
    os.makedirs(tmp_content, exist_ok=True)

    # Copy contents of source directory to the temporary directory
    print(f"Copying contents of {source_directory} to {tmp_content}")
    for item in os.listdir(source_directory):
        s = os.path.join(source_directory, item)
        d = os.path.join(tmp_content, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # # Clean the destination directory except git files and the temporary directory
    # print(f"Cleaning the destination directory {destination_directory} except git files and {tmp_content}")
    # for root, dirs, files in os.walk(destination_directory):
    #     for name in dirs + files:
    #         path = os.path.join(root, name)
    #         if path == tmp_content:
    #             continue
    #         if path.startswith(os.path.join(destination_directory, '.git')):
    #             print(f"Preserving (git file): {path}")
    #             continue
    #         if os.path.isdir(path):
    #             print(f"Deleting directory: {path}")
    #             shutil.rmtree(path)
    #         else:
    #             print(f"Deleting file: {path}")
    #             os.remove(path)

    # # Copy contents of the temporary directory to the destination directory
    # print(f"Copying contents of {tmp_content} to {destination_directory}")
    # for item in os.listdir(tmp_content):
    #     s = os.path.join(tmp_content, item)
    #     d = os.path.join(destination_directory, item)
    #     if os.path.isdir(s):
    #         shutil.copytree(s, d, dirs_exist_ok=True)
    #     else:
    #         shutil.copy2(s, d)

    # # Delete the temporary directory
    # print(f"Deleting temporary directory {tmp_content}")
    # shutil.rmtree(tmp_content)
    

    # # Create a new orphan branch or switch to the existing one
    # print(f"Switching to branch {branch_name}")
    # try:
    #     subprocess.check_call(['git', 'checkout', '--orphan', branch_name], cwd=destination_directory)
    # except subprocess.CalledProcessError:
    #     print(f"Error: Failed to switch to branch {branch_name}.")
    #     sys.exit(1)

    # # Commit the changes
    # print("Committing changes")
    # try:
    #     subprocess.check_call(['git', 'add', '.'], cwd=destination_directory)
    #     subprocess.check_call(['git', 'commit', '-m', f"Deploy to {branch_name}"], cwd=destination_directory)
    # except subprocess.CalledProcessError:
    #     print("Error: Failed to commit changes.")
    #     sys.exit(1)

    # # Push the branch to the remote repository
    # print(f"Pushing branch {branch_name} to remote repository")
    # try:
    #     subprocess.check_call(['git', 'push', 'origin', branch_name, '--force'], cwd=destination_directory)
    # except subprocess.CalledProcessError:
    #     print(f"Error: Failed to push branch {branch_name} to remote repository.")
    #     sys.exit(1)

    # # Switch back to the original branch
    # print(f"Switching back to branch {current_branch}")
    # try:
    #     subprocess.check_call(['git', 'checkout', current_branch], cwd=destination_directory)
    # except subprocess.CalledProcessError:
    #     print(f"Error: Failed to switch back to branch {current_branch}.")
    #     sys.exit(1)

    # print(f"Deployment to {branch_name} completed successfully.")

if __name__ == "__main__":
    main()
