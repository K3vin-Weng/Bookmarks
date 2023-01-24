# Bookmarks

## Motivation
As a webnovel and manga reader, when I finish the released chapters, I like to wait a few months to let new chapters
accumulate and then continue reading. However, I always forget where I was after so long and end up rereading several chapters which is 
incredibly frustrating. To solve this issue, I completed this project.

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
[^note]: Both hotkeys can be customized in Copy_URL.ahk.

