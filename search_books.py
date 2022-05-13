# This program determines if a manga or a novel (on the web) has already been read by the user
#   NOTE: this program is run through AutoHotkey first (must be activated by it to work as intended)

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import helpers
import webbrowser


# 20 spaces
spaces = " " * 20
# 10 newlines
newlines = "\n" * 10
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
books = open("books_list.txt", "r+")
result = helpers.go_to_book(title, books) # "Sucess" or "None"


print(newlines)


if ("None" == result):
    print(spaces + "There is NO RECORD of you having read this manga/novel")

else:
    # Now that we have found the book the lines under contain specific information
    #   This will be reflected by the names of the subsequent lines for readability
    manga_link = books.readline()  # url + "\n" or "None\n"
    novel_link = books.readline()  # url + "\n" or "None\n"
    manga_info = books.readline()
    novel_info = books.readline()

    if ("None\n" != manga_link):
        webbrowser.open(manga_link)

    if ("None\n" != novel_link):
        webbrowser.open(novel_link)

    print(spaces + "Manga (last chapter read):")
    print(spaces + manga_info)

    print(spaces + "Novel (last chapter read):")
    print(spaces + novel_info)


print(newlines)


# Delete the contents of clip_URL.txt for a future request
clip = open("clip_URL.txt", "w")
clip.close()
