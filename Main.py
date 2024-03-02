# Importing necessary modules and classes
import sys
import ExceptionClass as exp  # Custom exception class
from ConstantsModule import Constants  # Constants module containing predefined constants
from FileHandleClass import FileHandling  # FileHandling class for handling file operations
from HelperClass import Helper  # Helper class for various data analysis operations


# Main class for the script
class Main:
    filename = None

    def __init__(self):
        # Initializing instance variables
        self.dataframe = None  # Placeholder for the dataset
        self.script_path = None  # Path of the script file
        self.filename = None  # Name of the input file
        self.primary_column = None  # Name of the primary column in the dataset

    # Main method to execute the script
    def main(self):
        # Fetching command line arguments
        self.fetchArgumentInfo()

        # Creating FileHandling object to load data from the file
        file_obj = FileHandling(self.filename)
        self.dataframe = file_obj.loadData()  # Loading data into a pandas DataFrame

        # Extracting the primary column from the DataFrame
        primary_column_df = self.dataframe[self.primary_column]

        # Creating Helper object for data analysis operations
        helper = Helper()

        # Checking if the primary column is valid
        if helper.isPrimaryColumn(primary_column_df):
            file_obj.writeData(f'"{self.primary_column}" has all the unique data, so it can be a primary column.')
        else:
            # Writing error message if primary column is not valid
            file_obj.writeData(f'"{self.primary_column}" is not a primary column in "{self.filename}"')

        # Extracting column names from the DataFrame
        column_name_list = helper.fetchColumnName(self.dataframe)
        total_column_number = len(column_name_list)

        # Writing total number of columns in the file
        file_obj.writeData(
            f'{self.filename} has total {total_column_number} column{"s" if total_column_number > 1 else ""}.')

        # Writing separator line
        file_obj.writeData(f'---------------------------------------------------------', False)

        # Iterating over each column to analyze its type
        for column_name in column_name_list:
            column_type = helper.classifyColumnType(self.dataframe[column_name])
            file_obj.writeData(f'The type of column {column_name} is: {column_type}')

        # Writing separator line
        file_obj.writeData(f'---------------------------------------------------------', False)

        # Writing separator line
        file_obj.writeData(f'---------------------------------------------------------', False)

        # Iterating over each column to check pattern consistency
        for column_name in column_name_list:
            manual, inconsistent_rows = helper.checkPatternConsistency(self.dataframe[column_name])
            if manual is not None:
                if manual:
                    file_obj.writeData(f'For the column({column_name}), manual checking is required.')
                else:
                    file_obj.writeData(
                        f'For the column({column_name}), row number\n\t\t{inconsistent_rows}\n\t{"is" if len(inconsistent_rows) == 1 else "are"} not having consistent data.')
            else:
                file_obj.writeData(f'The column({column_name}) looks fine.')

        # Writing separator line
        file_obj.writeData(f'---------------------------------------------------------', False)

        # Writing separator line
        file_obj.writeData(f'---------------------------------------------------------', False)

        # Calculating cardinality and granularity of the dataset
        cardinality = helper.calculateCardinality(self.dataframe)
        granularity = helper.calculateGranularity(self.dataframe)

        # Writing cardinality information for each column
        file_obj.writeData(f'Cardinality:', False)
        for column, value in cardinality.items():
            file_obj.writeData(f'   {column}: {value} number of unique values')

        # Writing granularity information
        file_obj.writeData(f'The granularity of the dataset is determined by the total number of rows, indicating the '
                           f'level of detail present. Granularity: {granularity}')
        file_obj.writeData(f'---------------------------------------------------------', False)

    # Method to fetch command line arguments
    def fetchArgumentInfo(self):
        self.script_path = sys.argv[0]  # Fetching script path
        total_arg = len(sys.argv)  # Total number of command line arguments
        if total_arg < 2:
            # Error handling for insufficient arguments
            raise exp.DataNotSentException('You need to send the your file name along with primary column name.')
        elif total_arg < 3:
            value = sys.argv[1]
            if Constants.CSV in value or Constants.XLSX in value:
                raise exp.DataNotSentException(f'You need to send primary column name for {value}')
            else:
                raise exp.DataNotSentException('You need to send file name.')

        # Setting filename and primary_column from command line arguments
        self.filename = sys.argv[1]
        self.primary_column = sys.argv[2]
        Main.filename = self.filename


if __name__ == '__main__':
    # Initializing FileHandling and Helper objects
    file_obj = FileHandling()
    helper = Helper()
    time_zone = Constants.TIME_ZONE

    # Writing script start message
    file_obj.writeData(f'=============||Script started ({helper.prepareCurrentTime()} {time_zone})||=============',
                       False)
    # Creating Main object and executing the main method
    main_obj = Main()
    try:
        main_obj.main()  # Executing main method
        # Writing script finish message
        file_obj.writeData(
            f'=============||Script finished ({helper.prepareCurrentTime()} {time_zone})||=============\n', False)
        print('Script is over.')
    except Exception as e:
        # Handling and logging any exceptions that occur during execution
        file_obj.writeData(
            f'ERROR: {e}\n=============||Script terminated with an ERROR ({helper.prepareCurrentTime()} {time_zone})||=============\n',
            False)
        print('Script is terminated with error.')

    finally:
        file_obj.finalLogFile(Main.filename)
