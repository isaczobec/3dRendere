"""Modul med funktioner som laddar ordlistan samt får en pyton-lista av ord från den."""

import requests
import pathlib
import errorHandling

import errorHandling as EH

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
    
    wordList = EH.HandleExceptions(ReadFile,[fileName,fileDestination],errorMessage="The file could not be read!",exception=FileNotFoundError)

    if wordList != FileNotFoundError:
        return wordList
    else:

        # try to download the word list again
        if tryToDownloadFile:
            print("Trying to download the wordlist again from",MEMOURL)

            dL = EH.HandleExceptions(DownloadWordList,errorMessage="Could not download the wordlist!")
            if dL != Exception:
                return GetWordList(tryToDownloadFile=False) # do not try to download the file more than once
            else:
                return None
        else:
            return None


def ReadFile(fileName: str,
                fileDestination: str = "",
                splitString: str = "\n") -> list[str]:
    """Reads a file and returns a list of its contents."""
    if fileDestination == "": # om användaren inte har specefierat en directory, använd parent directoryn
        fileDestination = "\\".join(pathlib.Path(__file__).parts[:-1]) # lärde mig hur man delade på en file path från följande stack overflow-thread: https://stackoverflow.com/questions/26724275/removing-the-first-folder-in-a-path


    with open("\\".join([fileDestination,fileName]),"r") as file: # öppna och läs sagda fil
        return file.read().split(splitString) # returnera en lista med alla ord
    


def AppendToFile(fileName: str,
                 text: str = "",
                fileDestination: str = "",
                newLine: bool = True 
                ) -> None:

    if fileDestination == "": # om användaren inte har specefierat en directory, använd parent directoryn
        fileDestination = "\\".join(pathlib.Path(__file__).parts[:-1]) # lärde mig hur man delade på en file path från följande stack overflow-thread: https://stackoverflow.com/questions/26724275/removing-the-first-folder-in-a-path
    
    with open("\\".join([fileDestination,fileName]),"a") as file:
        if newLine:
            file.write("\n")
        file.write(text)




    
