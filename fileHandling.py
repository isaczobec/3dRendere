"""Modul med funktioner som laddar ordlistan samt får en pyton-lista av ord från den."""

import requests

import pathlib

MEMOURL = "https://www.csc.kth.se/~lk/P/memo.txt" # Url:et ordliste-filen hämtas från
WORDLIST_FILENAME = "DownloadedWordList.txt"

# ladda ned ordlistan från en specefierad url
def DownloadWordList(url: str = MEMOURL, # urlen filen laddas ned från
                fileDestination: str = "", # Destinationen filen ska laddas ned till
                fileName: str = WORDLIST_FILENAME): # default - namnet på ordlistan
    """Laddar ned ordlista från sagda url."""
    
    try:
        r = requests.get(url,allow_redirects=True) # ladda ned filen

        if fileDestination == "": # om användaren inte har specefierat en directory, använd parent directoryn
            fileDestination = "\\".join(pathlib.Path(__file__).parts[:-1]) # lärde mig hur man delade på en file path från följande stack overflow-thread: https://stackoverflow.com/questions/26724275/removing-the-first-folder-in-a-path

        # öppna och skriv ut nedladdningen till en vald fil
        with open("\\".join([fileDestination,fileName]),"wb") as file: 
            file.write(r.content)
    except Exception: # om det inte går att ladda ned ordlistan
        print("The wordlist file could not be downloaded!")
        return None


def GetWordList(
                fileName: str = WORDLIST_FILENAME,
                fileDestination: str = "",
                tryToDownloadFile:bool = True):
    """Returnar en lista med alla ord från ordliste-filen."""
    
    if fileDestination == "": # om användaren inte har specefierat en directory, använd parent directoryn
        fileDestination = "\\".join(pathlib.Path(__file__).parts[:-1]) # lärde mig hur man delade på en file path från följande stack overflow-thread: https://stackoverflow.com/questions/26724275/removing-the-first-folder-in-a-path

    try:
        with open("\\".join([fileDestination,fileName]),"r") as file: # öppna och läs sagda fil
            return file.read().split("\n") # returnera en lista med alla ord
    except FileNotFoundError: # om filen inte kunde hittas, medela användaren och returna none
        print("The file",fileName,"could not be found!")

        # try to download the word list again
        if tryToDownloadFile:
            print("Trying to download the wordlist again from",MEMOURL)
            try:
                DownloadWordList()
                return GetWordList(tryToDownloadFile=False)
            except Exception:
                print("could not download the file.")
                return None
        else:
            return None
