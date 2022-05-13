# This program updates the books_list.txt file with the latest
#   Note: This process is activated by a customized hotkey using AutoHotkey (must go through AHK for intended use)

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import helpers


# title-chapter separation
tc_sep = "   -   ch "
# 15 newlines
newlines = "\n" * 15
# prompts (q stands for question mark - ?)
title_q = "\nWhat is the title of the book?\n"
manga_or_novel = "\nDid you just read a manga or a novel?\nPlease input M or N respectively.\n"
chapter_q = "\nWhich chapter have you reached?\nType -1 if you have not read any chapter.\n"
alt_version_q = "\nIs there a {} version?\nPlease input Y, NNS, or NS.\n"
alt_title_q = "\nAre the manga and novel title different?\nPlease input No or the {} title if different.\n"
########################################################################################################################

# get URL of the webpage requested from clip_URL.txt, where the url selected through AHK is stored
clip = open("clip_URL.txt", "r")
url = clip.read()
clip.close()

# web scraping to get title
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(req).read(), features="html.parser")
title = soup.title.get_text().casefold()[:-1]


# Search if the manga/novel has been read
books = open("books_list.txt", "r")
result = helpers.go_to_book(title, books) # "Sucess" or "None"


## Updating "the books_list.txt" file

# Lines of information for book to update (refer to "info_books_list_format.txt" for more details)
line1 = ""
line2 = ""
line3 = ""
line4 = ""
line5 = ""
line6 = "\n"

print(newlines)

# Case 1: New book. Recording a new book
if ("None" == result):
    books.close()
    print("\nAccording to records, you have never read this book before.")
    title = input(title_q)
    formatted_title = helpers.format(title)
    type = input(manga_or_novel)
    # In case of error
    type = helpers.check_cmd(type, ["M", "N"], manga_or_novel)
    type_chapter = input(chapter_q)

    if ("M" == type):
        novel_option = input(alt_version_q.format("novel"))
        # In case of error
        novel_option = helpers.check_cmd(novel_option, ["Y", "NNS", "NS"], alt_version_q.format("novel"))

        if ("Y" == novel_option):
            novel_title = input(alt_title_q.format("novel"))
            novel_chapter = input(chapter_q)

            line1 = formatted_title + "\n"
            line2 = url + "\n"
            line3 = "None\n"
            line4 = title.strip() + tc_sep + type_chapter.strip() + "\n"
            line5 = novel_title.strip() + tc_sep + novel_chapter.strip() + "\n"

        else:
            line1 = formatted_title + "\n"
            line2 = url + "\n"
            line3 = "None\n"
            line4 = title.strip() + tc_sep + type_chapter.strip() + "\n"
            if ("NNS" == novel_option):
                line5 = "None - not searched" + "\n"
            else:
                line5 = "None - searched" + "\n"

    else:
        manga_option = input(alt_version_q.format("manga"))
        # In case of error
        manga_option = helpers.check_cmd(manga_option, ["Y", "NNS", "NS"], alt_version_q.format("manga"))

        if ("Y" == manga_option):
            manga_title = input(alt_title_q.format("manga"))
            manga_chapter = input(chapter_q)

            line1 = formatted_title + "\n"
            line2 = "None\n"
            line3 = url + "\n"
            if ("No" == manga_title):
                line4 = title.strip() + tc_sep + manga_chapter.strip() + "\n"
            else:
                line4 = manga_title.strip() + tc_sep + manga_chapter.strip() + "\n"
            line5 = title.strip() + tc_sep + type_chapter.strip() + "\n"

        else:
            line1 = formatted_title + "\n"
            line2 = "None\n"
            line3 = url + "\n"
            if ("NNS" == manga_option):
                line4 = "None - not searched" + "\n"
            else:
                line4 = "None - searched" + "\n"
            line5 = title.strip() + tc_sep + type_chapter.strip() + "\n"

    books = open("books_list.txt", "a")
    books.write(line1 + line2 + line3 + line4 + line5 + line6)
    books.close()

# Case 2: Updating an already recorded book.
else:
    print("According to record, you have read this book previously.\n")
    size = books.tell() # used later to truncate

    # previous data (to update)
    line2 = books.readline()
    line3 = books.readline()
    line4 = books.readline()
    line5 = books.readline()
    line6 = books.readline()
    print("Manga: " + line4.strip())
    print("Novel: " + line5.strip())

    type = input(manga_or_novel)
    # In case there is a mistake
    type = helpers.check_cmd(type, ["M", "N"], manga_or_novel)
    type_chapter = input(chapter_q)

    # updating previous data
    if ("M" == type):
        line2 = url + "\n"

        if ("None - not searched\n" == line4 or "None - searched\n" == line4):
            title = input(alt_title_q.format("manga"))

            if ("No" == title):
                index = line5.find(tc_sep)
                line4 = line5[:index] + tc_sep + type_chapter.strip() + "\n"
            else:
                line4 = title.strip() + tc_sep + type_chapter.strip() + "\n"

        else:
            index = line4.find(tc_sep)
            line4 = line4[:index] + tc_sep + type_chapter.strip() + "\n"


    else:
        line3 = url + "\n"

        if ("None - not searched\n" == line5 or "None - searched\n" == line5):
            title = input(alt_title_q.format("novel"))

            if ("No" == title):
                index = line4.find(tc_sep)
                line5 = line4[:index] + tc_sep + type_chapter.strip() + "\n"
            else:
                line5 = title.strip() + tc_sep + type_chapter.strip() + "\n"

        else:
            index = line5.find(tc_sep)
            line5 = line5[:index] + tc_sep + type_chapter.strip() + "\n"

    # Transfering the updated lines below the first entry of the current book to a temporary file
    temp = open("temp.txt", "w")
    temp.write(line2 + line3 + line4 + line5 + line6)  #done writing updated data about current book
    line = books.readline()
    while ("" != line):
        temp.write(line)
        line = books.readline()
    books.close()
    temp.close()

    # Updating the book_list file using the temporary file
    books = open("books_list.txt", "a")
    books.truncate(size)
    temp = open("temp.txt", "r")
    line = temp.readline()
    while ("" != line):
        books.write(line)
        line = temp.readline()









