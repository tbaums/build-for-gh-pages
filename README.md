
# Build for GH Pages

**Author:** Michael Tanenbaum  
**GitHub:** [https://github.com/tbaums](https://github.com/tbaums)  
**GitHub Project Repository:** [https://github.com/tbaums/build-for-gh-pages](https://github.com/tbaums/build-for-gh-pages)  
**License:** Apache License 2.0  

## Purpose

The purpose of this script is to promote the contents of a source directory (SOURCE_DIRECTORY) to a target directory (TARGET_DIRECTORY) on a user-specified Git branch (TARGET_BRANCH).

After the script executes, the contents of the TARGET_DIRECTORY will be only the git files that were in the TARGET_DIRECTORY before execution along with the contents of the SOURCE_DIRECTORY. No other files will be present in the TARGET_DIRECTORY.

Serving a static site on GitHub Pages requires that the static files be in the `/root` or `/docs` directory in a specific branch of a repo. The strategy presented here allows for continued development as normal, with a specific release branch for GitHub Pages.

## Script Arguments

The script accepts and requires three arguments:

1. **SOURCE_DIRECTORY** - The directory that contains the files to be promoted.
2. **TARGET_DIRECTORY** - The directory to which the files will be promoted. Must be a git repository.
3. **TARGET_BRANCH** - The branch to which the files will be promoted, committed, and pushed.

**Note:** SOURCE_DIRECTORY and TARGET_DIRECTORY must be absolute paths.

## Example

Run the script from the command line with the following command:

```sh
$ python3 build.py SOURCE_DIRECTORY TARGET_DIRECTORY TARGET_BRANCH
```

### Source Directory before execution:

- **Path:** `/usr/home/project/subdir/`
- **Contents:** `[file1.txt, file2.html, file3.css]`

### Target Directory before execution:

- **Path:** `/usr/home/project/`
- **Contents:** `[file4.js, file5.jpg, file6.png, ./.git/]`

### Execution:

```sh
$ python3 build.py /usr/home/project/subdir/ /usr/home/project/ gh-pages
```

### Target Directory after execution:

- **Path:** `/usr/home/project/`
- **Contents:** `[file1.txt, file2.html, file3.css, ./.git/]`

## How it Works

1. The script checks to see if there is a directory at the TARGET_DIRECTORY path.
2. The script checks to see if the TARGET_DIRECTORY is a git repository.
3. The script checks to see if the SOURCE_DIRECTORY is a directory.
4. The script checks to see if `/tmp/tmp_content` exists. If it does, it is removed.
5. The script copies the contents of the SOURCE_DIRECTORY to `/tmp/tmp_content`.
6. The script checks out the TARGET_BRANCH in the TARGET_DIRECTORY. The script creates the TARGET_BRANCH if it does not exist.
7. The script deletes all files in the TARGET_DIRECTORY except for the `.git` directory.
8. The script copies the contents of `/tmp/tmp_content` to the TARGET_DIRECTORY.
9. The script adds all files in the TARGET_DIRECTORY to the git index.
10. The script commits the changes to the git repository.
11. The script pushes the changes to the TARGET_BRANCH.
