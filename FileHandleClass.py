import pandas as pd
import ExceptionClass as exp
from ConstantsModule import Constants
from HelperClass import Helper


class FileHandling:

    count_log = 0

    def __init__(self, filename=''):
        self.year_month_day = None
        self.filename = filename

    def loadData(self):
        filename = self.filename

        if Constants.CSV in filename.lower():
            df = pd.read_csv(filename)
        elif Constants.XLSX in filename.lower():
            df = pd.read_excel(filename)
        else:
            raise exp.UnknownFileException(f'Unknown file type for file: {filename}')

        return df

    def writeData(self, info, count=True):
        if count:
            FileHandling.count_log += 1
        helper = Helper()
        self.year_month_day = helper.prepareCurrentDate()

        filename = Constants.LOG_FOLDER+Constants.LOG_FILE + self.year_month_day + Constants.TXT
        with open(filename, 'a+') as file:
            if count:
                file.write(f'{FileHandling.count_log}. {info}\n')
            else:
                file.write(f'{info}\n')
