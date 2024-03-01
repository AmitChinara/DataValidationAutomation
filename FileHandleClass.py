import os  # Importing the os module for operating system-related functions
import pandas as pd  # Importing pandas for data manipulation
import ExceptionClass as exp  # Importing custom exception classes
from ConstantsModule import Constants  # Importing constants
from HelperClass import Helper  # Importing Helper class for date formatting


class FileHandling:
    count_log = 0  # Class variable to count log entries

    def __init__(self, filename=''):
        self.year_month_day = None  # Placeholder for current date
        self.filename = filename  # Initializing filename

    # Method to load data from file into a DataFrame
    def loadData(self):
        filename = self.filename

        # Checking file extension to determine file type and reading accordingly
        if Constants.CSV in filename.lower():
            df = pd.read_csv(filename)
        elif Constants.XLSX in filename.lower():
            df = pd.read_excel(filename)
        else:
            # Raising UnknownFileException for unsupported file types
            raise exp.UnknownFileException(f'Unknown file type for file: {filename}')

        return df

    # Method to write data to a log file
    def writeData(self, info, count=True):
        if count:
            FileHandling.count_log += 1  # Incrementing log count if count is enabled
        helper = Helper()  # Creating Helper object for date formatting
        self.year_month_day = helper.prepareCurrentDate()  # Formatting current date

        # Constructing log file name based on current date
        filename = Constants.LOG_FOLDER + Constants.LOG_FILE + self.year_month_day + Constants.TXT

        # Writing information to log file
        with open(filename, 'a+') as file:
            if count:
                file.write(f'{FileHandling.count_log}. {info}\n')  # Writing log entry with count
            else:
                file.write(f'{info}\n')  # Writing log entry without count

    def deleteOldestLogFile(self):
        # Delete the oldest log file if the total number of log files exceeds 10
        log_files = [f for f in os.listdir(Constants.LOG_FOLDER) if f.startswith(Constants.LOG_FILE)]
        if len(log_files) > 10:
            # Sort log files based on creation time
            log_files.sort(key=lambda x: os.path.getctime(os.path.join(Constants.LOG_FOLDER, x)))

            # Delete the oldest log file
            oldest_log_file = os.path.join(Constants.LOG_FOLDER, log_files[0])
            os.remove(oldest_log_file)
            print(f"Deleted oldest log file: {oldest_log_file}")
