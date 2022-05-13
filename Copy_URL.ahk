; This is an AutoHotkey script that automates copying the url of the current tab to clip_URL.txt
;   and running either search_books.py or update.py



#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#WinActivateForce


^s::
FileDelete C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt
clipboard := ""
Send !d^c
ClipWait
FileAppend, %Clipboard%, C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt, UTF-8-RAW
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
Send {Text}cd C:\\Users\\kevfi\\PycharmProjects\\web_mangas_novels`n
Sleep, 500
Send py search_books.py`n
WinActivate, ahk_exe cmd.exe
return




^u::
FileDelete C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt
clipboard := ""
Send !d^c
ClipWait
FileAppend, %Clipboard%, C:\Users\kevfi\PycharmProjects\web_mangas_novels\clip_URL.txt, UTF-8-RAW
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
Send {Text}cd C:\\Users\\kevfi\\PycharmProjects\\web_mangas_novels`n
Sleep, 500
Send py update.py`n
WinActivate, ahk_exe cmd.exe
return

