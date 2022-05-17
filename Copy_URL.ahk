; This is an AutoHotkey script that automates copying the url of the current tab to clip_URL.txt
;   and running either search_books.py or update.py
; Note: If you want to use this script, you will need to change file paths at 6 different places. 
;       The file path "C:\Users\kevfi\PycharmProjects\web_mangas_novels" and only needs to
;       be changed to the file path indicating the folder where you store the entire program.
;       Only modify this specified part of any file path you see.
;       The locations where this change needs to be made is indicated by "HERE".

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#WinActivateForce




; The hotkey ^s (ctrl+s) is defined to copy the URL of active tab  the clip_URL.txt file
;   and run search_books.py

^s::
FileDelete C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt ; HERE
clipboard := ""
Send !d^c
ClipWait
FileAppend, %Clipboard%, C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt, UTF-8-RAW ; HERE
if WinExist("ahk_exe cmd.exe")
{
   WinActivate, ahk_exe cmd.exe 
   WinWaitActive, ahk_exe cmd.exe
}
else
{
   Run, %ComSpec% /k
   WinWaitActive, ahk_exe cmd.exe
}
Send {Text}cd C:\\Users\\kevfi\\PycharmProjects\\web_mangas_novels`n ; HERE (keep double slashes)
Sleep, 500
Send py search_books.py`n
WinActivate, ahk_exe cmd.exe
return




; The hotkey ^u (ctrl+u) is defined to copy the URL of the active tab to the clip_URL.txt file and
;   run update.py

^u::
FileDelete C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt ; HERE
clipboard := ""
Send !d^c
ClipWait
FileAppend, %Clipboard%, C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt, UTF-8-RAW ; HERE
if WinExist("ahk_exe cmd.exe")
{
   WinActivate, ahk_exe cmd.exe 
   WinWaitActive, ahk_exe cmd.exe
}
else
{
   Run, %ComSpec% /k
   WinWaitActive, ahk_exe cmd.exe
}
Send {Text}cd C:\\Users\\kevfi\\PycharmProjects\\web_mangas_novels`n ; HERE (Keep double slashes)
Sleep, 500
Send py update.py`n
WinActivate, ahk_exe cmd.exe
return

