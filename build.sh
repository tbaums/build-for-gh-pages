#!/bin/bash

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory-path> [branch-name]"
    exit 1
fi

# Assign arguments to variables
DIRECTORY_PATH=$1
BRANCH_NAME=${2:-gh-pages}

# Check if the directory exists
if [ ! -d "$DIRECTORY_PATH" ]; then
    echo "Directory $DIRECTORY_PATH does not exist."
    exit 1
fi

# Get the current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Create a new orphan branch or switch to the existing one
git checkout --orphan $BRANCH_NAME

# Remove all files from the branch except for the specified directory
shopt -s extglob
rm -rf !("$DIRECTORY_PATH")
shopt -u extglob

# Copy the specified directory to the root of the branch
cp -r $DIRECTORY_PATH/* .

# Check that the specified directory is now empty
if [ "$(ls -A $DIRECTORY_PATH)" ]; then
    echo "Failed to clear the directory $DIRECTORY_PATH."
    exit 1
fi

# Remove the empty specified directory
rm -r $DIRECTORY_PATH

# Add all files to the branch
git add .

# Commit the changes
git commit -m "Deploying $DIRECTORY_PATH to $BRANCH_NAME"

# Push the branch to the remote repository
git push -f origin $BRANCH_NAME

# Switch back to the original branch
git checkout $CURRENT_BRANCH