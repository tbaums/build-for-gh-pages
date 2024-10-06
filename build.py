
#!/usr/bin/env python3

# Build for GH Pages
# Author: Michael Tanenbaum
# GitHub: https://github.com/tbaums
# GitHub Project Repository: https://github.com/tbaums/build-for-gh-pages
# License: Apache License 2.0
# 
# The purpose of this script is to promote the contents of a source directory 
# (SOURCE_DIRECTORY) to a target directory (TARGET_DIRECTORY) on a user-specified 
# Git branch (TARGET_BRANCH). 
#
# After the script executes, the contents of the TARGET_DIRECTORY will be only the 
# git files that were in the TARGET_DIRECTORY before execution along with the 
# contents of the SOURCE_DIRECTORY. No other files will be present in the TARGET_DIRECTORY.
#
# Serving a static site on GitHub Pages requires that the static files be in the
# /root or /docs directory in a specific branch of a repo. The strategy presented
# here allows for continued development as normal, with a specific release branch 
# for GitHub Pages.
#
# The script accepts and requires three arguments:
# 1. SOURCE_DIRECTORY - The directory that contains the files to be promoted.
# 2. TARGET_DIRECTORY - The directory to which the files will be promoted. Must be a git repository.
# 3. TARGET_BRANCH - The branch to which the files will be promoted, committed, and pushed.
# ***NB: SOURCE_DIRECTORY and TARGET_DIRECTORY must be absolute paths.***
#
# Example:
# 
# Run the script from the command line with the following command:
# $ python3 build.py SOURCE_DIRECTORY TARGET_DIRECTORY TARGET_BRANCH
#
# Source Directory before execution:
# - path: /usr/home/project/subdir/
# - contents: [file1.txt, file2.html, file3.css]
#
# Target Directory before execution:
# - path: /usr/home/project/
# - contents: [file4.js, file5.jpg, file6.png, ./.git/]
#
# Execution:
# $ python3 build.py /usr/home/project/subdir/ /usr/home/project/ gh-pages
#
# Target Directory after execution:
# - path: /usr/home/project/
# - contents: [file1.txt, file2.html, file3.css, ./.git/]
#
#
# How it Works:
# 1. The script checks to see if there is a directory at the TARGET_DIRECTORY path.
# 2. The script checks to see if the TARGET_DIRECTORY is a git repository.
# 3. The script checks to see if the SOURCE_DIRECTORY is a directory.
# 4. The script checks to see if /tmp/tmp_content exists. If it does, it is removed.
# 5. The script copies the contents of the SOURCE_DIRECTORY to /tmp/tmp_content.
# 6. The script checks out the TARGET_BRANCH in the TARGET_DIRECTORY. The script creates the TARGET_BRANCH if it does not exist.
# 7. The script deletes all files in the TARGET_DIRECTORY except for the .git directory.
# 8. The script copies the contents of /tmp/tmp_content to the TARGET_DIRECTORY.
# 9. The script adds all files in the TARGET_DIRECTORY to the git index.
# 10. The script commits the changes to the git repository.
# 11. The script pushes the changes to the TARGET_BRANCH. 


import os
import shutil
import subprocess
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 build.py SOURCE_DIRECTORY TARGET_DIRECTORY TARGET_BRANCH")
        sys.exit(1)

    source_directory = sys.argv[1]
    target_directory = sys.argv[2]
    target_branch = sys.argv[3]

    # Check if TARGET_DIRECTORY exists
    if not os.path.isdir(target_directory):
        print(f"Error: TARGET_DIRECTORY '{target_directory}' does not exist.")
        sys.exit(1)
    print(f"TARGET_DIRECTORY '{target_directory}' exists.")

    # Check if TARGET_DIRECTORY is a git repository
    if not os.path.isdir(os.path.join(target_directory, '.git')):
        print(f"Error: TARGET_DIRECTORY '{target_directory}' is not a git repository.")
        sys.exit(1)
    print(f"TARGET_DIRECTORY '{target_directory}' is a git repository.")

    # Check if SOURCE_DIRECTORY exists
    if not os.path.isdir(source_directory):
        print(f"Error: SOURCE_DIRECTORY '{source_directory}' does not exist.")
        sys.exit(1)
    print(f"SOURCE_DIRECTORY '{source_directory}' exists.")

    tmp_content = '/tmp/tmp_content'

    # Remove /tmp/tmp_content if it exists
    if os.path.exists(tmp_content):
        shutil.rmtree(tmp_content)
        print(f"Removed existing '{tmp_content}' directory.")
    else:
        print(f"No existing '{tmp_content}' directory to remove.")

    # Copy contents of SOURCE_DIRECTORY to /tmp/tmp_content
    shutil.copytree(source_directory, tmp_content)
    print(f"Copied contents of '{source_directory}' to '{tmp_content}'.")
    # Checkout TARGET_BRANCH in TARGET_DIRECTORY. Create the TARGET_BRANCH if it does not exist.
    try:
        subprocess.run(['git', 'checkout', target_branch], cwd=target_directory, check=True)
        print(f"Checked out branch '{target_branch}' in '{target_directory}'.")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['git', 'checkout', '-b', target_branch], cwd=target_directory, check=True)
            print(f"Created and checked out new branch '{target_branch}' in '{target_directory}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to create and checkout branch '{target_branch}' in '{target_directory}'.")
            sys.exit(1)

    # Delete all files in TARGET_DIRECTORY except for the .git directory
    for item in os.listdir(target_directory):
        if item == '.git':
            continue
        item_path = os.path.join(target_directory, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted directory '{item_path}'.")
        else:
            os.remove(item_path)
            print(f"Deleted file '{item_path}'.")

    # Copy contents of /tmp/tmp_content to TARGET_DIRECTORY
    for item in os.listdir(tmp_content):
        s = os.path.join(tmp_content, item)
        d = os.path.join(target_directory, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
            print(f"Copied directory '{s}' to '{d}'.")
        else:
            shutil.copy2(s, d)
            print(f"Copied file '{s}' to '{d}'.")

    # Add all files in TARGET_DIRECTORY to the git index
    try:
        subprocess.run(['git', 'add', '.'], cwd=target_directory, check=True)
        print(f"Added all files in '{target_directory}' to the git index.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to add files to the git index in '{target_directory}'.")
        sys.exit(1)

    # Commit the changes to the git repository
    try:
        subprocess.run(['git', 'commit', '-m', 'Promote contents to target branch'], cwd=target_directory, check=True)
        print(f"Committed changes to the git repository in '{target_directory}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to commit changes in '{target_directory}'.")
        sys.exit(1)

    # Push the changes to the TARGET_BRANCH
    try:
        subprocess.run(['git', 'push', 'origin', target_branch], cwd=target_directory, check=True)
        print(f"Pushed changes to branch '{target_branch}' in remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to push changes to branch '{target_branch}' in remote repository.")
        sys.exit(1)

if __name__ == "__main__":
    main()