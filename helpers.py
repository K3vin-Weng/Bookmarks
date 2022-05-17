# helpers is a module that provides helper functions to search_books and update

import re


# number of lines occupied by each book
lines_per_book = 5
# punctuation marks
punctuation = [" ", "!", "?", ".", ",", "'",'"', ":", ";", "-", "–", "(", ")", "[", "]", "{", "}", "$", "#", "%",
               "&", "<", ">", "=", "_", "*", "\n"]
##################################################################################################################

# next(file) skips to the first entry of the next book in provided file
# requires: the cursor is at the beginning of the second entry/line of the previous book
def next(file):
    for i in range(lines_per_book):
        file.readline()



# go_to_book(title) goes to the second entry of the book entitled title and returns "Success" or
#   returns "None" if there is no match (the book has not been read) in the provided file
def go_to_book(title, file):
    current = file.readline()[:-1]
    if (current == ""):
        return "None"
    while (None == re.search(current, title)):
        next(file)
        current = file.readline()
        if "" == current:
            return "None"
        else:
            current = current[:-1]
    return "Success"



# format(title) returns the title with all sequences of punctuation replaced by ".*"
#   to make it a regex that can be used for matching
# Ex: "MookHyang - Dark Lady" => "mookhyang.*dark.*lady"
def format(title):
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

# check_cmd(cmd, valid_list, prompt) checks if cmd is in valid_list. Asks for appropriate with the providing prompt until
#   a valid command is received. Returns a valid received command (will simply return cmd if it is in valid_list)
def check_cmd(cmd, valid_list, prompt):
    while (cmd not in valid_list):
        print("Sorry, your command is invalid. Please try again.")
        cmd = input(prompt)
    return cmd
