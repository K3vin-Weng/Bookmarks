# helpers is a module that provides helper functions to search_books and update
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from sql_statements import *
from database_functions import read_query, execute_query
import pandas as pd


# punctuation marks
punctuation = [" ", "!", "?", ".", ",", "'", '"', ":", ";", "-", "–", "(", ")", "[", "]", "{", "}", "$", "#", "%",
               "&", "<", ">", "=", "_", "*", "\n"]
# web_book table columns
COL_BOOK_ID = "BookID"
COL_EXIST_MANGA = "ExistManga"
COL_EXIST_NOVEL = "ExistNovel"
COL_MANGA_REGEX = "MangaRegEx"
COL_MANGA_NAME = "MangaName"
COL_MANGA_CHAPTER = "MangaChapter"
COL_MANGA_CHAPTER_LINK = "MangaChapterLink"
COL_MANGA_FINISHED = "MangaFinished"
COL_MANGA_RATING = "MangaRating"
COL_NOVEL_REGEX = "novelRegEx"
COL_NOVEL_NAME = "novelName"
COL_NOVEL_CHAPTER = "novelChapter"
COL_NOVEL_CHAPTER_LINK = "novelChapterLink"
COL_NOVEL_FINISHED = "novelFinished"
COL_NOVEL_RATING = "novelRating"
web_book_columns = [COL_BOOK_ID, COL_EXIST_MANGA, COL_EXIST_NOVEL,
                    COL_MANGA_REGEX, COL_MANGA_NAME, COL_MANGA_CHAPTER, COL_MANGA_CHAPTER_LINK, COL_MANGA_FINISHED, COL_MANGA_RATING,
                    COL_NOVEL_REGEX, COL_NOVEL_NAME, COL_NOVEL_CHAPTER, COL_NOVEL_CHAPTER_LINK, COL_NOVEL_FINISHED, COL_NOVEL_RATING]
########################################################################################################################

def get_url():
    # get URL of the webpage requested from clip_URL.txt, where the url selected through AHK is stored
    clip = open("clip_URL.txt", "r")
    url = clip.read()
    clip.close()
    return url

def extract_title(url):

    # web scraping to get title
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(urlopen(req).read(), features="html.parser")
    title = soup.title.get_text().casefold()[:-1]
    return title


# format(title) returns the title with all sequences of punctuation replaced by ".*"
#   to make it a regex that can be used for matching
# Ex: "MookHyang - Dark Lady" => "mookhyang.*dark.*lady"
def title_to_regex(title):
    formated_title = title.casefold()
    prev_is_punc = False
    length = len(formated_title)
    i = 0
    while (i < length):
        if formated_title[i] in punctuation:
            if not(prev_is_punc):
                temp = i + 1
                formated_title = formated_title[:i] + ".*" + formated_title[temp:]
                length += 1
                i += 2
            else:
                temp = i + 1
                formated_title = formated_title[:i] + formated_title[temp:]

                # The length has been reduced by one because we have deleted one character
                # also everything after the deleted character has been moved forward by one
                # i.e. the next character to check has now been moved to the index of the deleted character
                #      => don't change i
                length -= 1
                i = i

            prev_is_punc = True

        else:
            prev_is_punc = False
            i += 1

    return formated_title


def find_book(connection, title):
    title = title.casefold()
    book = read_query(connection, sql_find_book.format(title=title))
    if not book:
        return None

    book = pd.DataFrame(book, columns=web_book_columns)
    return book


def number_of_books(connection):
    num = read_query(connection, sql_num_of_books)
    return num[0][0]


def get_book(connection, title):
    book = find_book(connection, title)
    new_book = True if book is None else False

    #  Book Details
    web_book = {
        COL_BOOK_ID: 0 if new_book else book.loc[0][COL_BOOK_ID],
        COL_EXIST_MANGA: False if new_book else book.loc[0][COL_EXIST_MANGA],
        COL_EXIST_NOVEL: False if new_book else book.loc[0][COL_EXIST_NOVEL],
        COL_MANGA_REGEX: "" if new_book else book.loc[0][COL_MANGA_REGEX],
        COL_MANGA_NAME: "" if new_book else book.loc[0][COL_MANGA_NAME],
        COL_MANGA_CHAPTER: 0 if new_book else book.loc[0][COL_MANGA_CHAPTER],
        COL_MANGA_CHAPTER_LINK: "" if new_book else book.loc[0][COL_MANGA_CHAPTER_LINK],
        COL_MANGA_FINISHED: False if new_book else book.loc[0][COL_MANGA_FINISHED],
        COL_MANGA_RATING: 0 if new_book else book.loc[0][COL_MANGA_RATING],
        COL_NOVEL_REGEX: "" if new_book else book.loc[0][COL_NOVEL_REGEX],
        COL_NOVEL_NAME: "" if new_book else book.loc[0][COL_NOVEL_NAME],
        COL_NOVEL_CHAPTER: 0 if new_book else book.loc[0][COL_NOVEL_CHAPTER],
        COL_NOVEL_CHAPTER_LINK: "" if new_book else book.loc[0][COL_NOVEL_CHAPTER_LINK],
        COL_NOVEL_FINISHED: False if new_book else book.loc[0][COL_NOVEL_FINISHED],
        COL_NOVEL_RATING: 0 if new_book else book.loc[0][COL_NOVEL_RATING]
    }
    return new_book, web_book


def add_book(connection, web_book):
    sql_add_book = sql_insert_book.format(BookID=web_book[COL_BOOK_ID],
                                          ExistManga=web_book[COL_EXIST_MANGA],
                                          ExistNovel=web_book[COL_EXIST_NOVEL],
                                          MangaRegEx=web_book[COL_MANGA_REGEX],
                                          MangaName=web_book[COL_MANGA_NAME],
                                          MangaChapter=web_book[COL_MANGA_CHAPTER],
                                          MangaChapterLink=web_book[COL_MANGA_CHAPTER_LINK],
                                          MangaFinished=web_book[COL_MANGA_FINISHED],
                                          MangaRating=web_book[COL_MANGA_RATING],
                                          NovelRegEx=web_book[COL_NOVEL_REGEX],
                                          NovelName=web_book[COL_NOVEL_NAME],
                                          NovelChapter=web_book[COL_NOVEL_CHAPTER],
                                          NovelChapterLink=web_book[COL_NOVEL_CHAPTER_LINK],
                                          NovelFinished=web_book[COL_NOVEL_FINISHED],
                                          NovelRating=web_book[COL_NOVEL_RATING],
                                          )
    execute_query(connection, sql_add_book)


def update_book(connection,book_type, web_book):
    manga = "Manga"
    novel = "Novel"
    if book_type == "M":
        book_type = manga
    elif book_type == "N":
        book_type = novel
    else:
        raise Exception("Non Valid Book Type.")

    sql_update = sql_update_book.format(book_type=book_type,
                                        book_id=web_book[COL_BOOK_ID],
                                        ExistManga=web_book[COL_EXIST_MANGA],
                                        ExistNovel=web_book[COL_EXIST_NOVEL],
                                        Chapter=web_book[COL_MANGA_CHAPTER],
                                        ChapterLink=web_book[COL_MANGA_CHAPTER_LINK],
                                        Finished=web_book[COL_MANGA_FINISHED],
                                        Rating=web_book[COL_MANGA_RATING]
                                        )
    execute_query(connection, sql_update)

    if web_book[COL_MANGA_NAME] != web_book[COL_NOVEL_NAME]:
        sql_update_title = ""
        if book_type == manga:
            sql_update_title = sql_update_alt_title.format(book_type=novel,
                                                           book_id=web_book[COL_BOOK_ID],
                                                           RegEx=web_book[COL_NOVEL_REGEX],
                                                           Name=web_book[COL_NOVEL_NAME]
                                                           )
        elif book_type == novel:
            sql_update_title = sql_update_alt_title.format(book_type=manga,
                                                           book_id=web_book[COL_BOOK_ID],
                                                           RegEx=web_book[COL_MANGA_REGEX],
                                                           Name=web_book[COL_MANGA_NAME]
                                                           )
        execute_query(connection, sql_update_title)


def display_book(book):
    # title-chapter separation
    sep = "   -   ch "
    print("Manga:\r\n\t", end="")
    if book[COL_EXIST_MANGA] == "Yes":
        print(book[COL_MANGA_NAME] + sep + str(book[COL_MANGA_CHAPTER]))
    else:
        print(book[COL_EXIST_MANGA])
    print("\n" * 2)
    print("Novel:\r\n\t", end="")
    if book[COL_EXIST_NOVEL] == "Yes":
        print(book[COL_NOVEL_NAME] + sep + str(book[COL_NOVEL_NAME]))
    else:
        print(book[COL_EXIST_NOVEL])


# check_cmd(cmd, valid_list, prompt) checks if cmd is in valid_list. Asks for appropriate with the providing prompt until
#   a valid command is received. Returns a valid received command (will simply return cmd if it is in valid_list)
def check_cmd(cmd, valid_list, prompt):
    while (cmd not in valid_list):
        print("Sorry, your command is invalid. Please try again.")
        cmd = input(prompt)
    return cmd