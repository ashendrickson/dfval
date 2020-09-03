from .dfcompare import dfcompare
from .dfclean import dfclean
from .dfcheck import dfcheck

def compare(x, y, k, qty_n = [], keep_comparison = False, dec_rnd = 8, thrshld = 0):
    """compares data of the two dataframes based on a common key by creating a Comarison object from dfcompare
    Parameters:
      x (pandas dataframe): a pandas dataframe
      y (pandas dataframe): a pandas dataframe
      k (list): list of names in the key
      qty_n (list): list of quantities field names for comparison (optional)
      keep_comparison (bool): indicates if the entire comparison should be retained (the "full outer join" vs just exceptions)
      dec_rnd (int): the number of decimal places to round the quantity fields before comparison
      thrshld (float): a threshold for determining if a quantity difference should be considered an exception
    Returns:
      c (Comarpison object): an instance of the Comarison object with the following parameters:
        Sets the object instance's exceptions parameter to a dataframe of exceptions found during the comparison
        Sets the object instance's results parameter to a dataframe with records counts for the result of the comparison
        If keep_comparison = True, sets the object instances' comparison parameter to the dataframe with result of the "full outer join"
        Note: The compare() does a column name check to make sure both x and y have the fields in the key.
          If that fails, a message is printed and the parameters are not set/reset.
    """
    c = dfcompare.Comparison()
    c.compare(x, y, k, qty_n, keep_comparison, dec_rnd, thrshld)
    return c

def na_clean(df, qty_n):
    """calls na_clean() to convert NaN values to 0
      Parameters:
        df (pandas dataframe): a pandas dataframe
        qty_n (list): list of field names in the dataframe that should have NaN values replaced with 0
      Returns:
        df (pandas dataframe): a pandas dataframe that is the input dataframe with NaN in the qty_n list replaced with 0
    """
    return dfclean.na_clean(df, qty_n)

def dups_check(df, k):
    """calls dups_check() to check for duplicate records in a passed in pandas dataframe based on a passed in key
    Parameters:
      df (pandas dataframe): a pandas dataframe
      k (list): columns in the dataframe that should be used to check for duplicates
    Returns:
      dups (pandas dataframe): a pandas dataframe of duplicate records based on the passed in key
        (the dups dataframe will have n - 1 records for each duplicate in the input dataframe
          where n = the number of times that duplicate occurs in the passed in dataframe)
    """
    return dfcheck.dups_check(df, k)

def column_names_check(df, expected_fields):
    """calls colunm_names_check() to see if a pandas dataframe has the columns contained in a passed in list
    Parameters:
      df (pandas dataframe): a pandas dataframe
      excepcted_fields (list): list of columns expected to be in the passed in dataframe
    Returns:
      columns_contain_result (pandas dataframe): a pandas dataframe with a record for each expected
        column and True/False indicating if it is in the dataframe
    """
    return dfcheck.column_names_check(df, expected_fields)
