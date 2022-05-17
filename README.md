# Bookmarks

## Motivation
As a webnovel and manga reader, when I finish the released chapters, I like to wait a few months to let new chapters
accumulate. However, I always forget where I was after so long and end up rereading several chapters which is 
incredibly frustrating. Therefore, I solved this issue with this project

## Description
This is an automated tool that lets users determine whether the book on the active webpage has been read before by 
pressing a hotkey[^1].
If the book has been read, the last read chapter of the book is automatically opened online for the user to read.
Furthermore, since information about read books is stored, data must be updated. Users can press another hotkey[^2]
to update stored data when they want to. [^note]

### Features I am working on:
* Making this tool cross-platform and centralizing so that it can be used across several devices.
* A listing functionality: The display of the list of all unfinished books with relevant information.
* Other information: The rating of books (would involve sorting of the books from highest rating to lowest for the listing functionality).
* Other information: The option to add a summary.

[^1]: Currently defined to be ctrl+s. It runs search_books.py.
[^2]: Currently defined to be ctrl+u. It runs update.py.
[^note]: Both hotkeys can be customized

## How to Install and Use
1. Download AutoHotkey if not installed.
2. Download Python if not installed.
3. Download the files in this repository in a single folder.
4. The Python libraries needed are urrlib.request, beautifulsoup4, re and webbrowser.
5. Start using by double clicking on the Copy_URL.ahk file. You can now press the two hotkeys whenever you want on online books.

