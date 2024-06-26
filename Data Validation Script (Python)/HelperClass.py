import re  # Importing regular expression module
import numpy as np  # Import numpy for numerical operations
from datetime import datetime  # Importing datetime module for date and time operations
from ConstantsModule import Constants  # Importing constants


class Helper:

    def __init__(self):
        pass

    # Method to check if a column is a primary column (i.e., all values are unique)
    def isPrimaryColumn(self, primary_column_df):
        return primary_column_df.count() == primary_column_df.nunique()

    # Method to prepare current date in the format YYYYMMDD
    def prepareCurrentDate(self):
        current_datetime = datetime.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        year_str = str(year)
        month_str = str(month).zfill(2)  # Zero-padding for month
        day_str = str(day).zfill(2)  # Zero-padding for day
        return year_str + month_str + day_str

    # Method to prepare current time with optional format string
    def prepareCurrentTime(self, format_str=Constants.DATE_FORMAT):
        current_time = datetime.now()
        return current_time.strftime(format_str)

    # Method to fetch column names from a DataFrame
    def fetchColumnName(self, dataframe):
        return dataframe.columns.tolist()

    # Method to classify the type of column (numeric, string, date, alphanumeric)
    def classifyColumnType(self, column_df):
        # Implementation to classify column type based on data distribution
        column_values = column_df.dropna().astype(str)
        total_count = len(column_values)
        numeric_count = alpha_count = date_count = 0
        # Updated date patterns to include different formats
        date_patterns = [
            re.compile(r'\b\d{4}-\d{4}\b'),  # Matches '2019-2020'
            re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b')  # Matches '1/1/2000'
        ]

        for value in column_values:
            value_no_spaces = ''.join(value.split())  # Remove spaces from the value
            if re.match(r'^-?\d+(\.\d+)?$', value_no_spaces):  # Check if value is numeric
                numeric_count += 1
            elif value_no_spaces.isalpha():  # Check if value is alphabetic
                alpha_count += 1
            elif any(pattern.match(value_no_spaces) for pattern in date_patterns):  # Check if value matches any date pattern
                date_count += 1

        numeric_percent = numeric_count / total_count
        alpha_percent = alpha_count / total_count
        date_percent = date_count / total_count

        if date_percent > Constants.VALID_PERCENTAGE:
            return 'date'
        elif numeric_percent > Constants.VALID_PERCENTAGE:
            return 'numeric'
        elif alpha_percent > Constants.VALID_PERCENTAGE:
            return 'string'
        else:
            return 'alphanumeric'

    # Method to check pattern consistency of a column
    def checkPatternConsistency(self, column_df):
        # Checks pattern consistency of a column.
        def checkLengthConsistency():
            # Checks length consistency within the column.
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
            # Checks consistency of values in a serial pattern.
            values = column_df.dropna().astype(str)
            pattern = None
            inconsistent_values = []
            gap = 0
            if self.classifyColumnType(column_df) == 'numeric':
                gap = column_df.diff().value_counts().idxmax()

            for value in values:
                value = value.strip()
                if pattern is None:
                    pattern = value
                elif value.isdigit() and (
                        str(int(value)) == str(int(int(pattern) + gap)) or str(int(value)) == str(int(int(pattern) - gap))):
                    pattern = value
                else:
                    inconsistent_values.append(value)

            return inconsistent_values

        def checkForOutliers():
            # Checks for outlier values.
            values = column_df.dropna()
            value_counts = values.value_counts(normalize=True)
            outlier_indices = [index for index, (value, percent) in enumerate(value_counts.items()) if
                               percent < 0.05 or percent > 0.95]
            outlier_values = value_counts.index[outlier_indices]
            outlier_indexes_df = [index + 1 for index, value in values.reset_index(drop=True).items() if
                                  value in outlier_values]
            return outlier_indexes_df if outlier_indexes_df else None

        def isTotallyRandom():
            # Checks if the column is totally random.
            unique_count = column_df.nunique()
            total_count = len(column_df.dropna())
            unique_percent = unique_count / total_count
            return unique_percent > Constants.UNIQUE_PERCENT

        # Call internal functions to check different types of pattern consistency
        inconsistent_rows = checkLengthConsistency()
        inconsistent_rows = checkSerialConsistency() if inconsistent_rows else None
        inconsistent_rows = checkForOutliers() if inconsistent_rows else None
        manual = isTotallyRandom() if inconsistent_rows else None

        return manual, inconsistent_rows

    def calculateCardinality(self, dataframe):
        # Calculates cardinality for each column.

        # Initialize an empty dictionary to store cardinality values for each column
        cardinality = {}

        # Iterate over each column in the DataFrame
        for column in dataframe.columns:
            # Calculate the number of unique values in the column and store it in the dictionary
            cardinality[column] = dataframe[column].nunique()

        # Return the dictionary containing cardinality values for each column
        return cardinality

    def calculateGranularity(self, dataframe):
        # Calculates various aspects of granularity of a dataset.
        # Returns a dictionary containing:
        # - Number of records/rows
        # - Number of columns/variables
        # - Average non-null values per column
        # - Percentage of missing values per column
        # - Descriptive statistics for numerical columns (mean, median, min, max, std)
        # - Temporal granularity (if applicable)

        num_rows = len(dataframe)  # Number of rows
        num_columns = len(dataframe.columns)  # Number of columns

        # Calculate the average number of non-null values per column and percentage of missing values
        avg_non_null_values = {}
        missing_value_percentage = {}
        for column in dataframe.columns:
            non_null_count = dataframe[column].count()  # Count non-null values in the column
            avg_non_null_values[column] = non_null_count / num_rows if num_rows > 0 else 0  # Calculate average
            missing_value_percentage[column] = (1 - avg_non_null_values[column]) * 100  # Calculate percentage of missing values

        # Calculate descriptive statistics for numerical columns
        numerical_stats = {}
        numerical_columns = dataframe.select_dtypes(include=np.number).columns
        for column in numerical_columns:
            numerical_stats[column] = {
                "mean": dataframe[column].mean(),
                "median": dataframe[column].median(),
                "min": dataframe[column].min(),
                "max": dataframe[column].max(),
                "std": dataframe[column].std()
            }

        # Check if temporal data is present and determine temporal granularity
        temporal_granularity = None
        if 'timestamp' in dataframe.columns:
            min_timestamp = dataframe['timestamp'].min()
            max_timestamp = dataframe['timestamp'].max()
            time_difference = max_timestamp - min_timestamp
            if time_difference.days >= num_rows:  # Assuming each row represents a distinct time point
                temporal_granularity = "Fine (each row represents a distinct time point)"
            else:
                temporal_granularity = "Coarse (aggregated over time)"

        # Return the calculated granularity metrics as a dictionary
        return {
            "num_rows": num_rows,
            "num_columns": num_columns,
            "avg_non_null_values": avg_non_null_values,
            "missing_value_percentage": missing_value_percentage,
            "numerical_statistics": numerical_stats,
            "temporal_granularity": temporal_granularity
        }