import pandas as pd

def na_clean(df, qty_n):
    """converts NaN values to 0
      Parameters:
        df (pandas dataframe): a pandas dataframe
        qty_n (list): list of field names in the dataframe that should have NaN values replaced with 0
      Returns:
        df (pandas dataframe): a pandas dataframe that is the input dataframe with NaN in the qty_n list replaced with 0
    """
    for i in qty_n:
        if len(df[df[i].isnull()].index) > 0:
            df[i] = df[i].fillna(0)
            print("NaN values in the " + i + " column have been replaced with zeros")
    return df
