import os
import shutil
import subprocess
import json
import uuid
import platform
import sys
from datetime import datetime
from time import sleep

directories = []
name = ""
osname = os.name
defaultpath = ""

def folderSetup():
    print("Source Organiser Version 1.0.0.9. Copyright (c) 2025-2026 Nicholas Lim.")
    global defaultpath
    if osname == "nt":
        defaultpath = rf"{os.path.expandvars("%USERPROFILE%")}\Documents\source-organiser"
    elif osname == "posix":
        defaultpath = rf"{os.path.expandvars("$HOME")}/Documents/source-organiser"
    try:
        os.chdir(defaultpath)
        folderCreate()
    except FileNotFoundError:
        while True:
            setupcheck = input(f"The required directory '{defaultpath}' is not found.\nWould you like to create it now? (Type Y or N): ").lower()
            if setupcheck == "y":
                os.makedirs(defaultpath)
                os.chdir(defaultpath)
                if osname == "nt":
                    defaultpath = rf"{os.path.expandvars("%USERPROFILE%")}\Documents\source-organiser"
                elif osname == "posix":
                    defaultpath = rf"{os.path.expandvars("$HOME")}/Documents/source-organiser"
                folderCreate()
            elif setupcheck == "n":
                sys.exit(2)

def folderCreate():
    print("Your folders:")
    for dir in os.scandir("."):
        if dir.is_dir():
            print(dir.name)
            directories.append(dir.name)
    print("")
    while True:
        command = input("Would you like to create another folder? (Type Y or N): ").lower()
        if command == "y":
            while True:
                name = input("Enter folder name: ")
                if name not in directories:
                    os.mkdir(name)
                    directories.append(name)
                    print("")
                    with open(f"{name}/folder.log", "a+") as log:
                        load(10, "Creating 'folder.log'...  ")
                        load(20, "Loading 'folder.log'...  ")
                        log.write(f"{datetime.now()}: Log for '{name}' created.")
                        load(20, "Editing 'folder.log'...  ")
                        with open(f"{name}/metadata.json", "a+") as metadata:
                            metadata.write('{"id": "", "name": ""}')
                            metadata.seek(0)
                            load(40, "Copying 'metadata.json'...")
                            log.write(f"\n{datetime.now()}: 'metadata.json' copied.")
                            contents = json.load(metadata)
                            load(50, "Loading 'metadata.json'...")
                            contents["name"] = name
                            load(60, "Editing 'metadata.json'...")
                            id = str(uuid.uuid4())
                            load(70, "Editing 'metadata.json'...")
                            contents["id"] = id
                            load(80, "Editing 'metadata.json'...")
                            metadata.seek(0)
                            metadata.truncate()
                            json.dump(contents, metadata)
                            load(90, "Editing 'metadata.json'...")
                            log.write(f"\n{datetime.now()}: 'metadata.json' edited.")
                        load(100, "Folder creation completed.")
                        log.write(f"\n{datetime.now()}: Folder creation completed.")
                        print("\n")
                    mainInterface(name)
                    sys.exit()
                else:
                    print(f"The folder name '{name}' is already used.")
                break
        elif command == "n":
            if directories == []:
                print("There are no available folders.")
            else:
                break
    mainInterface(0)

def mainInterface(name):
    if directories != []:
        while True:
            if name == 0:
                folder = input("Enter folder name to use: ")
            else:
                folder = name
            if folder in directories:
                print("")
                if osname == "nt":
                    folderdir = defaultpath + "\\" + folder
                else:
                    folderdir = defaultpath + "/" + folder
                os.chdir(folderdir)
                log = open(f"{folderdir}/folder.log", "a")
                print(f"Folder: {folder}\nPath: {os.getcwd()}")
                log.write(f"\n{datetime.now()}: Session started.")
                checkexit = False
                try:
                    contents = json.load(open(f"metadata.json", "r"))
                    print(f"ID: {contents["id"]}")
                except:
                    print("Warning: Unable to retrive ID from 'metadata.json'. Run 'generate-metadata' to fix this issue.")
                    checkexit = True
                    exitcode = 2
                print("Enter 'help' to get started!")
                while True:
                    os.chdir(folderdir)
                    command = input(">> ")

                    # Help command.
                    if command.lower() == "help":
                        print("""about:  Display information about Source Organiser.
change: Change folder.
clear:  Clears the screen.
create: Creates a new file or folder within the folder.
        Add '--file' or '-i' to create a file.
        Add '--folder' or '-o' to create a folder.
remove: Removes the current folder.
        Add '--noprompt' or '-n' to remove confirmation prompts.
exit:   Quits this interface.
help:   Display this message.
info:   Display information about the selected folder.
log:    Load the folder's log file.
rename: Rename a folder.""")
                        checkexit = False
                    
                    # About command.
                    elif command.lower() == "about":
                        print("Source Organiser Version 1.0.0.9.\nA user-friendly CLI file organiser for developers with more human-readable commands.\nCopyright (c) 2025-2026 Nicholas Lim.\nView source at https://github.com/Nicholas1023/source-organiser.")

                    # Exit command.
                    elif command.lower() == "exit":
                        if checkexit == True:
                            log.write(f"\n{datetime.now()}: Session ended. (Exit code {exitcode})")
                            log.close()
                            sys.exit(exitcode)
                        else:
                            log.write(f"\n{datetime.now()}: Session ended. (Exit code 0)")
                            log.close()
                            sys.exit(0)

                    elif command.lower() == "generate-metadata":
                        with open(f"{folderdir}/folder.log", "a+") as log:
                            with open(f"{folderdir}/metadata.json", "w+") as metadata:
                                metadata.write('{"id": "", "name": ""}')
                                metadata.seek(0)
                                load(0, "Copying 'metadata.json'...")
                                log.write(f"\n{datetime.now()}: 'metadata.json' copied.")
                                contents = json.load(metadata)
                                load(20, "Loading 'metadata.json'...")
                                contents["name"] = folder
                                load(40, "Editing 'metadata.json'...")
                                id = str(uuid.uuid4())
                                load(60, "Editing 'metadata.json'...")
                                contents["id"] = id
                                load(80, "Editing 'metadata.json'...")
                                metadata.seek(0)
                                metadata.truncate()
                                json.dump(contents, metadata)
                                load(100, "'metadata.json' created.\n")
                                log.write(f"\n{datetime.now()}: 'metadata.json' created.")
                                checkexit = False
                    
                    # Clear screen command.
                    elif command.lower() == "clear":
                        if osname == "nt":
                            subprocess.run("cls", shell=True)
                            checkexit = False
                        elif osname == "posix":
                            subprocess.run("clear", shell=True)
                            checkexit = False
                        else:
                            print("This command is not compatible with your OS.")
                            checkexit = True
                            exitcode = 3

                    # Folder information command.
                    elif command.lower() == "info":
                        print(f"Folder Name: {folder}\nFolder Path: {os.getcwd()}\nFolder ID: {contents["id"]}\nOperating System: {platform.system() + " " + platform.version()}")
                        checkexit = False

                    # Folder removal command: confirmation prompts.
                    elif command.lower() == "remove":
                        while True:
                            check = input(f"Are you sure about removing '{folder}'? This action is irreversible. (Type Y or N): ").lower()
                            if check == "y":
                                log.close()
                                os.chdir(defaultpath)
                                shutil.rmtree(folderdir)
                                print(f"Folder '{folder}' removed successfully.")
                                print("Exiting Source Organiser...")
                                sys.exit(0)
                            elif check == "n":
                                break

                    # Folder removal command: no confirmation prompts.
                    elif command.lower() == "remove --noprompt" or command.lower() == "remove -n":
                        log.close()
                        os.chdir(defaultpath)
                        shutil.rmtree(folderdir)
                        print(f"Folder '{folder}' removed successfully.")
                        print("Exiting Source Organiser...")
                        sys.exit(0)

                    # Create file command.
                    elif command.lower() == "create --file" or command.lower() == "create -i":
                        os.chdir(folderdir)
                        while True:
                            filename = input("Enter filename: ")
                            if filename == "metadata.json":
                                print("Error: Creating a file named 'metadata.json' removes the folder's metadata. Try another filename.")
                                checkexit = True
                                exitcode = 2
                            else:
                                create = open(filename, "w")
                                create.close()
                                print(f"'{filename}' created successfully.")
                                checkexit = False
                                break

                    # Create folder command.
                    elif command.lower() == "create --folder" or command.lower() == "create -o":
                        os.chdir(folderdir)
                        foldername = input("Enter folder name: ")
                        os.makedirs(foldername, exist_ok=True)
                        print(f"'{foldername}' created successfully.")
                        checkexit = False

                    # Display log command.
                    elif command.lower() == "log":
                        print(f"Log for '{folder}':")
                        os.chdir(folderdir)
                        log.close()
                        display = open(f"{folderdir}/folder.log", "r")
                        print(display.read())
                        display.close()
                        log = open(f"{folderdir}/folder.log", "a")
                    
                    # Change folder command.
                    elif command.lower() == "change":
                        if directories != [f"{folder}"]:
                            while True:
                                change = input("Enter folder name to change to: ")
                                if change in directories:
                                    if osname == "nt":
                                        folderdir = defaultpath + "\\" + folder
                                    else:
                                        folderdir = defaultpath + "/" + folder
                                    os.chdir(folderdir)
                                    if osname == "nt":
                                        subprocess.run("cls", shell=True)
                                    elif osname == "posix":
                                        subprocess.run("clear", shell=True)
                                    checkexit = False
                                    log.write(f"\n{datetime.now()}: Session ended. (Exit code 0)")
                                    log.close()
                                    mainInterface(change)
                                else:
                                    print(f"Folder '{change}' does not exist.")
                                    checkexit = True
                                    exitcode = 2
                        else:
                            print("There are no other available folders.")
                            checkexit = True
                            exitcode = 2

                    # Rename folder command.
                    elif command.lower() == "rename":
                        while True:
                            newname = input("Enter folder's new name: ")
                            if newname.lower() not in directories:
                                log.close()
                                os.chdir(defaultpath)
                                if osname == "nt":
                                    folderdirnew = defaultpath + "\\" + newname
                                else:
                                    folderdirnew = defaultpath + "/" + newname
                                os.rename(folderdir, folderdirnew)
                                folderdir = folderdirnew
                                log = open(f"{folderdir}/folder.log", "a")
                                log.write(f"\n{datetime.now()}: '{name}' renamed to '{newname}'.")
                                log.close()
                                if osname == "nt":
                                    subprocess.run("cls", shell=True)
                                elif osname == "posix":
                                    subprocess.run("clear", shell=True)
                                checkexit = False
                                directories.append(newname)
                                directories.remove(folder)
                                contents = json.load(open(f"{defaultpath}/{newname}/metadata.json", "r"))
                                contents["name"] = newname
                                json.dump(contents, open(f"{defaultpath}/{newname}/metadata.json", "w"))
                                mainInterface(newname)
                            else:
                                print(f"The folder name '{newname}' is already used.")

                    # Command does not exist or options not provided.
                    else:
                        command = command.lower()
                        if (command.startswith("create") and
                        command != "create -i" and
                        command != "create -o" and
                        command != "create --file" and
                        command != "create --folder"):
                            print("The command 'create' requires '--file', '--folder', '-i' or '-o'.")
                            checkexit = True
                            exitcode = 4
                        elif (command.startswith("cli ") and command != "cli -d" and command != "cli --default"):
                            print("The command 'cli' accepts only '--default', '-d' or without options.")
                            checkexit = True
                            exitcode = 4
                        elif (command.startswith("remove ") and command != "remove -n" and command != "remove --noprompt"):
                            print("The command 'remove' accepts only '--noprompt', '-n' or without options.")
                            checkexit = True
                            exitcode = 4
                        elif command != "":
                            print(f"The command '{command}' does not exist. Enter 'help' to get started!")
                            checkexit = True
                            exitcode = 1

            else:
                print("Invalid folder name.")
    else:
        print("There are no available folders.")
        sys.exit(2)

def load(percentage: int, status: str):
    percentagebar = int(percentage / 2)
    bar = "\u2588" * percentagebar + "\u2591" * (50 - percentagebar)
    if percentage != 100:
        print(f"\r{str(percentage)}%  {bar} {status}", end="", flush=True)
    else:
        print(f"\r{str(percentage)}% {bar} {status}", end="", flush=True)
    sleep(0.1)

if __name__ == "__main__":
    folderSetup()