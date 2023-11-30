import math
errorCode = "ERROR"
"""String that is returned by the handleExceptions method to signal that an error occured while trying to handle the exception."""

def HandleExceptions(function,
                         arguments: list = [],
                         exception = Exception,
                         errorMessage = "an error occurred while handling this file!"):
    """Function for handling errors. Prints errorMessage and returns the exception if there is an exception."""

    try:
        return function(*arguments)
    except exception:
        print(errorMessage)
        return exception
    

