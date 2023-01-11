sql_initial_setup = """
    create database books;
    use books;
    create table web_book (
        BookID int UNIQUE,
        ExistManga varchar(40),
        ExistNovel varchar(40),
        MangaRegEx varchar(255),
        MangaName varchar(255),
        MangaChapter int,
        MangaChapterLink varchar(255),
        MangaFinished bool,
        MangaRating float,
        NovelRegEx varchar(255),
        NovelName varchar(255),
        NovelChapter int,
        NovelChapterLink varchar(255),
        NovelFinished bool,
        NovelRating float
    );
    """

sql_insert_book = (
    "INSERT INTO web_book\r\n" 
    "VALUES ({BookID}, '{ExistManga}', '{ExistNovel}', "
    "       '{MangaRegEx}', '{MangaName}', {MangaChapter}, '{MangaChapterLink}', {MangaFinished}, {MangaRating}, "
    "       '{NovelRegEx}', '{NovelName}', {NovelChapter}, '{NovelChapterLink}', {NovelFinished}, {NovelRating}"
    ")"
)

sql_update_book = (
    "UPDATE web_book\r\n"
    "SET ExistManga='{ExistManga}', ExistNovel='{ExistNovel}', "
    "    {book_type}Chapter={Chapter}, {book_type}ChapterLink='{ChapterLink}', "
    "    {book_type}Finished={Finished}, {book_type}Rating={Rating}\r\n"
    "WHERE BookID={book_id}"
)

sql_update_alt_title = (
    "UPDATE web_book\r\n"
    "SET {book_type}RegEx='{RegEx}', {book_type}Name='{Name}'\r\n"
    "WHERE BookID={book_id}"
)

sql_find_book = \
    "SELECT * FROM web_book WHERE IF(ExistManga='Yes' , '{title}' REGEXP MangaRegEx, FALSE) OR " \
    "IF(ExistNovel='Yes', '{title}' REGEXP NovelRegEx, False)"

sql_num_of_books = \
    "SELECT COUNT(BookID)" \
    "FROM web_book"

