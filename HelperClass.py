import re
from datetime import datetime
from ConstantsModule import Constants


class Helper:

    def __init__(self):
        pass

    def isPrimaryColumn(self, primary_column_df):
        return primary_column_df.count() == primary_column_df.nunique()

    def prepareCurrentDate(self):
        current_datetime = datetime.now()

        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day

        year_str = str(year)
        month_str = str(month).zfill(2)
        day_str = str(day).zfill(2)

        return year_str + month_str + day_str

    def prepareCurrentTime(self, format_str=Constants.DATE_FORMAT):
        current_time = datetime.now()
        return current_time.strftime(format_str)

    def fetchColumnName(self, dataframe):
        return dataframe.columns.tolist()

    import re

    def classifyColumnType(self, column_df):
        column_values = column_df.dropna().astype(str)
        total_count = len(column_values)

        numeric_count = alpha_count = date_count = 0
        date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')

        for value in column_values:
            value_no_spaces = ''.join(value.split())  # Remove spaces from the value
            if re.match(r'^[0-9.]+$', value_no_spaces):  # Check if value is numeric
                numeric_count += 1
            elif value_no_spaces.isalpha():  # Check if value is alphabetic
                alpha_count += 1
            elif date_pattern.match(value_no_spaces):  # Check if value matches date pattern
                date_count += 1

        numeric_percent = numeric_count / total_count
        alpha_percent = alpha_count / total_count
        date_percent = date_count / total_count

        if date_percent > 0.85:
            return 'date'
        elif numeric_percent > 0.85:
            return 'numeric'
        elif alpha_percent > 0.85:
            return 'string'
        else:
            return 'alphanumeric'

    def checkPatternConsistency(self, column_df):
        def checkLengthConsistency():
            column = column_df.dropna()
            lengths = [len(str(x)) for x in column]
            most_common_length = max(set(lengths), key=lengths.count)

            consistent_count = sum(1 for length in lengths if length == most_common_length)
            percentage_consistent = consistent_count / len(column)

            if percentage_consistent < Constants.VALID_PERCENTAGE:
                most_common_length = None

            inconsistent_rows = [index + 1 for index, length in enumerate(lengths) if length != most_common_length]
            return inconsistent_rows

        def checkSerialConsistency():
            values = column_df.dropna().astype(str)
            pattern = None
            inconsistent_values = []
            if self.classifyColumnType(column_df) == 'numeric':
                gap = column_df.diff().value_counts().idxmax()

            for value in values:
                if pattern is None:
                    pattern = value
                elif value.isdigit() and (str(int(value)) == str(int(pattern) + gap) or str(int(value)) == str(int(pattern) - gap)):
                    pattern = value
                else:
                    inconsistent_values.append(value)

            return inconsistent_values

        def checkForOutliers():
            values = column_df.dropna()
            value_counts = values.value_counts(normalize=True)
            outlier_indices = [index for index, (value, percent) in enumerate(value_counts.items()) if percent < 0.05 or percent > 0.95]
            outlier_values = value_counts.index[outlier_indices]
            outlier_indexes_df = [index + 1 for index, value in values.reset_index(drop=True).items() if value in outlier_values]
            return outlier_indexes_df if outlier_indexes_df else None

        def isTotallyRandom():
            unique_count = column_df.nunique()
            total_count = len(column_df.dropna())
            unique_percent = unique_count / total_count
            return unique_percent > Constants.UNIQUE_PERCENT

        inconsistent_rows = checkLengthConsistency()
        inconsistent_rows = checkSerialConsistency() if inconsistent_rows else None
        inconsistent_rows = checkForOutliers() if inconsistent_rows else None
        manual = isTotallyRandom() if inconsistent_rows else None

        return manual, inconsistent_rows

    def calculateCardinality(self, dataframe):
        cardinality = {}
        for column in dataframe.columns:
            cardinality[column] = dataframe[column].nunique()
        return cardinality

    def calculateGranularity(self, dataframe):
        return len(dataframe)
