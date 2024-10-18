# Description

A collection of miscellaneous scripts and other useful tools.

# Files

## initProject.py - Inits project of any type, add to GitHub.
[initProject.py](initProject.py) - Place this script in your desired folder and run it using `py initProject.py`. The script will:

1. Initialize a Git repository.
2. Create a `.gitignore` file.
3. Commit the initial changes.
4. Prompt you for your GitHub account (be sure to create a token first at [GitHub Token Settings](https://github.com/settings/tokens?type=beta)) to create a private repository using `curl`.
5. Push the repository to your GitHub account.

## obsidian/templater/insertFileLink.js - Obsidian Templater Script.
This script facilitates the creation of new notes with intelligent parsing in Obsidian.

File: [insertFileLink.js](obsidian/templater/insertFileLink.js)


### Instructions:

1. **Add the Script**  
   Place the `insertFileLink.js` script in the Templater's script folder.

2. **Create a Template Note**  
   Set up a template note (e.g., `Template todo.md`) with the following content:
```markdown
<%* 
let note = await tp.user.createNote(tp, "TODO");
if (note === null) return;
%><% "---" %>
type: todo
tags:
  - <% tp.date.now() %>
date: <% tp.date.now() %>
done: false
priority:
parent:
<% "---" %>
<% note?.text %>
```
3. **Configure a Hotkey**  
   Assign a hotkey in Templater's settings for easy access to this script.

4. **(Optional) Set Up a Global Hotkey with AutoHotKey**  
   Use AutoHotKey to create a global hotkey that allows you to create a note from anywhere:
```ahk
; Global hotkey for creating a new note in Obsidian
#n:: ; Ctrl + Alt + N as the global hotkey
    ; Attempt to find the Obsidian window using its class
    IfWinExist ahk_exe Obsidian.exe
    {
        WinActivate  ; Bring Obsidian to the front
	Send ^n
    }
    else
    {
        MsgBox Obsidian is not running.
    }
return
```
