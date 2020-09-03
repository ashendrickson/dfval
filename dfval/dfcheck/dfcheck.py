import pandas as pd

def column_names_check(df, expected_fields):
    """checks to see if a pandas dataframe has the columns contained in a passed in list
    Parameters:
      df (pandas dataframe): a pandas dataframe
      excepcted_fields (list): list of columns expected to be in the passed in dataframe
    Returns:
      columns_contain_result (pandas dataframe): a pandas dataframe with a record for each expected
        column and True/False indicating if it is in the dataframe
    """
    columns_contain_result = pd.DataFrame(columns = ['expected_column_name', 'column_check_pass'])
    for f in expected_fields:
        columnCheck = f in df.columns
        data = [[f, str(columnCheck)]]
        result = pd.DataFrame(data, columns = ['expected_column_name', 'column_check_pass'])
        columns_contain_result = columns_contain_result.append(result)
    return columns_contain_result

def dups_check(df, k):
    """checks for duplicate records in a passed in pandas dataframe based on a passed in key
    Parameters:
      df (pandas dataframe): a pandas dataframe
      k (list): columns in the dataframe that should be used to check for duplicates
    Returns:
      dups (pandas dataframe): a pandas dataframe of duplicate records based on the passed in key
        (the dups dataframe will have n - 1 records for each duplicate in the input dataframe
          where n = the number of times that duplicate occurs in the passed in dataframe)
    """
    dups = df[df.duplicated(subset = k)]
    dups = dups[k]
    return dups
