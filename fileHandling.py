"""Module with funcitons for downloading, opening and writing
to files relevant to this game."""

import requests
import pathlib
import errorHandling as EH

MEMOURL = "https://www.csc.kth.se/~lk/P/memo.txt"
"""The url the worldlist file is downloaded from."""
WORDLIST_FILENAME = "DownloadedWordList.txt"
"""The filename that will be attempted to retrieve 
the wordlist from or download it to."""

def DownloadFile(url: str = MEMOURL,
                fileDestination: str = "",
                fileName: str = WORDLIST_FILENAME) -> None:
    """Downloads a file from a url, prints an errormessage 
    and returns none if it couldnt be downloaded."""
    
    r = requests.get(url,allow_redirects=True)


    # Write the downloaded content to the the specefied location
    with open(GetFullFilePath(fileName,fileDestination),"wb") as file: 
        file.write(r.content)


def GetWordList(
                fileName: str = WORDLIST_FILENAME,
                fileDestination: str = "",
                tryToDownloadFile:bool = True) -> list[str]:
    """Returns a list with all the words from the wordlist file."""
    
    # attempt to open the wordlist file
    wordList = EH.HandleExceptions(ReadFile,[fileName,fileDestination],errorMessage="The file could not be read!",exception=FileNotFoundError)

    if wordList != FileNotFoundError: # if there wasnt an error
        return wordList
    else:

        # try to download the word list again
        if tryToDownloadFile:
            print("Trying to download the wordlist again from",MEMOURL)

            dL = EH.HandleExceptions(DownloadFile,errorMessage="Could not download the wordlist!")
            if dL != Exception:
                return GetWordList(tryToDownloadFile=False) # do not try to download the file again
            else:
                return None
        else:
            return None


def ReadFile(fileName: str,
                fileDestination: str = "",
                splitString: str = "\n") -> list[str]:
    """Reads a file and returns a list of its contents."""


    with open(GetFullFilePath(fileName,fileDestination),"r") as file: # öppna och läs sagda fil
        return file.read().split(splitString) # returnera en lista med alla ord
    


def AppendToFile(fileName: str,
                 text: str = "",
                fileDestination: str = "",
                newLine: bool = True 
                ) -> None:
    """appends text to a specefied file."""

    with open(GetFullFilePath(fileName,fileDestination),"a") as file:
        if newLine:
            file.write("\n")
        file.write(text)


def GetFullFilePath(fileName: str, fileDestination: str,) -> str:
    """Gets and returns the full file path 
    from a file name and a folder/filedestination."""

    if fileDestination == "": # om användaren inte har specefierat en directory, använd parent directoryn
        fileDestination = "\\".join(pathlib.Path(__file__).parts[:-1]) # lärde mig hur man delade på en file path från följande stack overflow-thread: https://stackoverflow.com/questions/26724275/removing-the-first-folder-in-a-path

    return "\\".join([fileDestination,fileName])





    
