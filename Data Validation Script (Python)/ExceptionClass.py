# Custom exception class for handling unknown file exceptions
class UnknownFileException(Exception):
    pass


# Custom exception class for handling cases where data is not sent along with the script
class DataNotSentException(Exception):
    pass