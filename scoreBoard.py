import errorHandling
import fileHandling
import os
import datetime

SCOREBOARD_FILEPATH = "ScoreBoard.txt"
SCOREBOARD_KEYVALUESEPARATOR = ":"
SCOREBOARD_ATTRIBUTESEPARATOR = ";"
"""The separator used in the scoreboard file to separate attributes"""


def GetScoreBoardEntries(sort: bool = True,
                         sortKey: str = "score") -> list[dict[str:str]]:
    
    entries: list[str] = errorHandling.HandleExceptions(fileHandling.ReadFile,[SCOREBOARD_FILEPATH],exception=FileNotFoundError,errorMessage="the file could not be found!")


    entryList = []

    if entries != FileNotFoundError:

        for entry in entries:

            entryDict = {}
            if entry != "":

                for attribute in entry.split(SCOREBOARD_ATTRIBUTESEPARATOR):
                    keyAndValue = attribute.split(SCOREBOARD_KEYVALUESEPARATOR)
                    entryDict[keyAndValue[0]] = keyAndValue[1]

            entryList.append(entryDict)



    if sort == True:
        entryList.sort(key=lambda entry : entry[sortKey],reverse=True)  # sort the list

    return entryList

def AddScoreBoardEntry(name = os.getlogin(),
                       date = datetime.date.today(),
                       score = 1, 
                       time = 1, 
                       moves = 1) -> None:
    """Adds an entry and writes it to the scoreboard file"""
    entryString = f"name{SCOREBOARD_KEYVALUESEPARATOR}{name}{SCOREBOARD_ATTRIBUTESEPARATOR}date{SCOREBOARD_KEYVALUESEPARATOR}{date}{SCOREBOARD_ATTRIBUTESEPARATOR}score{SCOREBOARD_KEYVALUESEPARATOR}{score}{SCOREBOARD_ATTRIBUTESEPARATOR}time{SCOREBOARD_KEYVALUESEPARATOR}{time}{SCOREBOARD_ATTRIBUTESEPARATOR}moves{SCOREBOARD_KEYVALUESEPARATOR}{moves}"
    errorHandling.HandleExceptions(fileHandling.AppendToFile,[SCOREBOARD_FILEPATH,entryString],errorMessage="could not write to the scoreboard file.")









AddScoreBoardEntry()
print(GetScoreBoardEntries())
                
                
                



        

    
