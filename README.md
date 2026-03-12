# Source Organiser
Source Organiser is a user-friendly CLI file organiser for developers with more human-readable commands.

## Installation
You can install Source Organiser using the command: `pip install source-organiser`

## Features
1. A setup wizard that creates folders with metadata and ensures the necessary directories are available.
2. A CLI interface for entering more human-readable commands:
- `about`:  Displays information about Source Organiser.
- `change`: Change folder.
- `clear`:  Clears the screen.
- `create`: Creates a new file or folder within the folder.
    - Add '--file' or '-i' to create a file.
    - Add '--folder' or '-o' to create a folder.
- `remove`: Removes the current folder.
    - Add '--noprompt' or '-n' to remove confirmation prompts.
- `exit`:   Quits the CLI interface.
- `help`:   Display the help message.
- `info`:   Display information about the selected folder.
- `log`:    Load the folder's log file.
- `rename`: Rename a folder.

## Using as a Module
- `folderSetup()`: Ensure the necessary directories are available.
- `folderCreate()`: Create folders.
- `mainInterface(name)`: Starts the interface. Set `name` to name of folder or `0` to ignore this parameter.

## Using as an Application
Run `source-organiser` in your terminal to use Source Organiser as an application.