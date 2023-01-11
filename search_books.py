# This program determines if a manga or a novel (on the web) has already been read by the user
#   NOTE: this program is run through AutoHotkey first (must be activated by it to work as intended)
from database_functions import create_server_connection
from helpers import *
import webbrowser

# 15 newlines
newlines = "\n" * 15
########################################################################################################################
## Determine if book is recorded and get details
connection = create_server_connection()  # connect to MySQL server
book_url = get_url()
title = extract_title(book_url)  # web scrape title
new_book, book_details = get_book(connection, title)

## Display Information
print(newlines)
if new_book:
    print(spaces + "There is NO RECORD of you having read this manga/novel")

else:
    manga_link = book_details[COL_MANGA_CHAPTER_LINK]
    novel_link = book_details[COL_NOVEL_CHAPTER_LINK]
    if (manga_link != ""):
        webbrowser.open(manga_link)
    if (novel_link != ""):
        webbrowser.open(novel_link)

    display_book(book_details)
print(newlines)

## Delete the contents of clip_URL.txt for a future request
clip = open("clip_URL.txt", "w")
clip.close()
