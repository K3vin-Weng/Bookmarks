# This program updates the books_list.txt file with the latest
#   Note: This process is activated by a customized hotkey using AutoHotkey (must go through AHK for intended use)
from database_functions import create_server_connection
from helpers import *


# 15 newlines
newlines = "\n" * 15
# prompts (q stands for question mark - ?)
title_q = "\nWhat is the title of the book?\n"
manga_or_novel = "\nDid you just read a manga or a novel?\nPlease input M or N respectively.\n"
chapter_q = "\nWhich chapter have you reached?\nType -1 if you have not read any chapter.\n"
alt_version_q = "\nIs there a {} version?\nPlease input Y, U, or N.\n"
alt_title_q = "\nAre the manga and novel title different?\nPlease input No or the {} title if different.\n"
# alternative medium message
alt_medium_yes = "Y"
alt_medium_unknown = "U"
alt_medium_none = "N"
alt_medium_dict = {
    alt_medium_yes: "Yes",
    alt_medium_unknown: "Unknown - Not Searched",
    alt_medium_none: "None"
}
########################################################################################################################
## Determine if book is recorded and get details
connection = create_server_connection()  # connect to MySQL server
book_url = get_url()
book_title = extract_title(book_url)  # web scrape title
new_book, book = get_book(connection, book_title)


## Updating MySQL db

print(newlines)
# Case 1: New book. Record the new book
if new_book:
    print("\nAccording to records, you have never read this book before.")
    book_type = input(manga_or_novel)
    # In case of error
    book_type = check_cmd(book_type, ["M", "N"], manga_or_novel)
    book_title = input(title_q)
    book_chapter = input(chapter_q)
    book[COL_BOOK_ID] = number_of_books(connection) + 1

    if "M" == book_type:
        book[COL_EXIST_MANGA] = "Yes"
        book[COL_MANGA_REGEX] = title_to_regex(book_title)
        book[COL_MANGA_NAME] = book_title
        book[COL_MANGA_CHAPTER] = book_chapter
        book[COL_MANGA_CHAPTER_LINK] = book_url

        exist_novel = input(alt_version_q.format("novel"))
        # In case of error
        exist_novel = check_cmd(exist_novel, [alt_medium_yes, alt_medium_unknown, alt_medium_none],
                                alt_version_q.format("novel"))
        book[COL_EXIST_NOVEL] = alt_medium_dict[exist_novel]

        if "Y" == exist_novel:
            novel_title = input(alt_title_q.format("novel"))
            novel_chapter = input(chapter_q)
            
            book[COL_NOVEL_REGEX] = book_title if book_title == "No" else title_to_regex(novel_title)
            book[COL_NOVEL_NAME] = novel_title
            book[COL_NOVEL_CHAPTER] = novel_chapter

    elif "N" == book_type:
        book[COL_EXIST_NOVEL] = "Yes"
        book[COL_NOVEL_REGEX] = title_to_regex(book_title)
        book[COL_NOVEL_NAME] = book_title
        book[COL_NOVEL_CHAPTER] = book_chapter
        book[COL_NOVEL_CHAPTER_LINK] = book_url

        exist_manga = input(alt_version_q.format("manga"))
        # In case of error
        exist_manga = check_cmd(exist_manga, [alt_medium_yes, alt_medium_unknown, alt_medium_none],
                                 alt_version_q.format("manga"))
        book[COL_EXIST_MANGA] = alt_medium_dict[exist_manga]

        if ("Y" == exist_manga):
            manga_title = input(alt_title_q.format("manga"))
            manga_chapter = input(chapter_q)
            book[COL_MANGA_REGEX] = book_title if book_title == "No" else title_to_regex(manga_title)
            book[COL_MANGA_NAME] = manga_title
            book[COL_MANGA_CHAPTER] = manga_chapter

    add_book(connection, book)


# Case 2: Updating an already recorded book.
else:
    print("According to record, you have read this book previously.\n")
    display_book(book)

    book_type = input(manga_or_novel)
    # In case there is a mistake
    book_type = check_cmd(book_type, ["M", "N"], manga_or_novel)
    book_chapter = input(chapter_q)

    # updating previous data
    if "M" == book_type:
        if book[COL_EXIST_MANGA] != alt_medium_dict[alt_medium_yes]:
            book[COL_EXIST_MANGA] = alt_medium_dict[alt_medium_yes]
            manga_title = input(alt_title_q.format("manga"))
            book[COL_MANGA_REGEX] = title_to_regex(manga_title)
            book[COL_MANGA_NAME] = manga_title

        book[COL_MANGA_CHAPTER] = book_chapter
        book[COL_MANGA_CHAPTER_LINK] = book_url

    elif "N" == book_type:
        if book[COL_EXIST_NOVEL] != alt_medium_yes:
            book[COL_EXIST_NOVEL] = alt_medium_yes
            novel_title = input(alt_title_q.format("novel"))
            book[COL_NOVEL_REGEX] = title_to_regex(novel_title)
            book[COL_NOVEL_NAME] = novel_title

        book[COL_NOVEL_CHAPTER] = book_chapter
        book[COL_NOVEL_CHAPTER_LINK] = book_url

    update_book(connection, book_type, book)
