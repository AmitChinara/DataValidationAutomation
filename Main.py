import sys
import ExceptionClass as exp
from ConstantsModule import Constants
from FileHandleClass import FileHandling
from HelperClass import Helper


class Main:

    def __init__(self):
        self.dataframe = None
        self.script_path = None
        self.filename = None
        self.primary_column = None

    def main(self):
        self.fetchArgumentInfo()
        file_obj = FileHandling(self.filename)
        self.dataframe = file_obj.loadData()
        primary_column_df = self.dataframe[self.primary_column]
        helper = Helper()
        if helper.isPrimaryColumn(primary_column_df):
            pass
        else:
            file_obj.writeData(f'"{self.primary_column}" is not a primary column in "{self.filename}"')

        column_name_list = helper.fetchColumnName(self.dataframe)
        total_column_number = len(column_name_list)
        file_obj.writeData(f'{self.filename} has total {total_column_number} column{"s" if total_column_number > 1 else ""}.')

        file_obj.writeData(f'---------------------------------------------------------', False)
        for column_name in column_name_list:
            column_type = helper.classifyColumnType(self.dataframe[column_name])
            file_obj.writeData(f'The type of column {column_name} is: {column_type}')
        file_obj.writeData(f'---------------------------------------------------------', False)

        file_obj.writeData(f'---------------------------------------------------------', False)
        for column_name in column_name_list:
            manual, inconsistent_rows = helper.checkPatternConsistency(self.dataframe[column_name])
            if manual is not None:
                if manual:
                    file_obj.writeData(f'For the column({column_name}), manual checking is required.')
                else:
                    file_obj.writeData(f'For the column({column_name}), row number\n\t\t{inconsistent_rows}\n\t{"is" if len(inconsistent_rows) == 1 else "are"} not having consistent data.')
            else:
                file_obj.writeData(f'The column({column_name}) looks fine.')
        file_obj.writeData(f'---------------------------------------------------------', False)

        file_obj.writeData(f'---------------------------------------------------------', False)
        cardinality = helper.calculateCardinality(self.dataframe)
        granularity = helper.calculateGranularity(self.dataframe)

        file_obj.writeData(f'Cardinality:', False)
        for column, value in cardinality.items():
            file_obj.writeData(f'   {column}: {value} number of unique values')

        file_obj.writeData(f'The granularity of the dataset is determined by the total number of rows, indicating the level of detail present. Granularity: {granularity}')
        file_obj.writeData(f'---------------------------------------------------------', False)

    def fetchArgumentInfo(self):
        self.script_path = sys.argv[0]
        total_arg = len(sys.argv)
        if total_arg < 2:
            raise exp.DataNotSentException('You need to send the your file name along with primary column name.')
        elif total_arg < 3:
            value = sys.argv[1]
            if Constants.CSV in value or Constants.XLSX in value:
                raise exp.DataNotSentException('You need to send primary column name.')
            else:
                raise exp.DataNotSentException('You need to send file name.')

        self.filename = sys.argv[1]
        self.primary_column = sys.argv[2]


if __name__ == '__main__':
    file_obj = FileHandling()
    helper = Helper()
    time_zone = Constants.TIME_ZONE

    file_obj.writeData(f'=============||Script started ({helper.prepareCurrentTime()} {time_zone})||=============', False)
    main_obj = Main()
    try:
        main_obj.main()
        file_obj.writeData(f'=============||Script finished ({helper.prepareCurrentTime()} {time_zone})||=============\n', False)
    except Exception as e:
        file_obj.writeData(f'ERROR: {e}\n=============||Script terminated with an ERROR ({helper.prepareCurrentTime()} {time_zone})||=============\n', False)
