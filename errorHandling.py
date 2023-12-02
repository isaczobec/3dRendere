"""Code with a function that can handle any exception."""

def HandleExceptions(function,
                         arguments: list = [],
                         exception = Exception, # the exception that is anticipated
                         errorMessage = "an error occurred while handling this file!"):
    """Function for handling errors. Prints errorMessage and returns the exception if there is an exception."""

    try:
        return function(*arguments)
    except exception:
        print(errorMessage)
        return exception