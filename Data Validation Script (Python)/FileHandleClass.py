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
            try:
                df = pd.read_csv(filename)
            except UnicodeDecodeError:
                df = pd.read_csv(filename, encoding='latin1')
        elif Constants.XLSX in filename.lower():
            try:
                df = pd.read_excel(filename)
            except UnicodeDecodeError:
                df = pd.read_excel(filename, encoding='latin1')
        else:
            # Raising UnknownFileException for unsupported file types
            raise exp.UnknownFileException(f'Unknown file type for file: {filename}')

        return df

    # Method to write data to a log file
    def writeData(self, info, count=True):
        if count:
            FileHandling.count_log += 1  # Incrementing log count if count is enabled
        helper = Helper()
        self.year_month_day = helper.prepareCurrentDate()
        # Constructing log file name based on current date
        filename = f'{Constants.LOG_FOLDER}{Constants.LOG_FILE}{Constants.TXT}'

        # Writing information to log file
        with open(filename, 'a+') as file:
            if count:
                file.write(f'{FileHandling.count_log}. {info}\n')  # Writing log entry with count
            else:
                file.write(f'{info}\n')  # Writing log entry without count

    # Method to delete the log file

    def finalLogFile(self, main_file):
        filename = f'{Constants.LOG_FOLDER}{Constants.LOG_FILE}{Constants.TXT}'
        date = self.year_month_day

        def deleteFile(filepath = ''):
            # Check if the file exists before attempting to delete
            if os.path.exists(filepath):
                with open(filepath, 'w') as obj:
                    obj.write('')
                    obj.close()
                print("Log file deleted successfully.")
            else:
                print("Log file does not exist.")


        def deleteLogFile():
            # Check if the file exists before attempting to delete
            if os.path.exists(filename):
                os.remove(filename)
                print("Log file deleted successfully.")
            else:
                print("Log file does not exist.")

        def writeLogToFinalLog():
            if main_file is not None:
                filename_value = ''
                tokens = main_file.split('/')
                for token in tokens:
                    if token.endswith('.csv') or token.endswith('.xlsx'):
                        # Determine the length of the extension
                        extension_length = len(token.split('.')[-1]) + 1
                        # Remove the extension and print the rest
                        filename_value = token[:-extension_length]
                final_log_filename = f'{Constants.LOG_FOLDER}{filename_value.upper()}_{Constants.LOG_FILE}.{date}{Constants.TXT}'
                write_mode = 'w'
            else:
                final_log_filename = f'{Constants.LOG_FOLDER}{Constants.ERROR_LOG_FILE}.{date}{Constants.TXT}'
                write_mode = 'a+'

            if os.path.exists(filename):
                with open(filename, 'r') as log_file:
                    log_data = log_file.read()
                    log_file.close()
                    with open(final_log_filename, write_mode) as final_log_file:
                        if write_mode == 'w':
                            final_log_file.write(log_data)
                        else:
                            with open(final_log_filename, 'r') as read_final_file:
                                old_content = read_final_file.read()
                                deleteFile(final_log_filename)
                                final_log_file.write(log_data)
                                final_log_file.write(old_content)
                                final_log_file.close()
                                read_final_file.close()

            else:
                print("Log file does not exist.")

        writeLogToFinalLog()
        deleteLogFile()