import pandas as pd
import numpy as np

from ..dfcheck.dfcheck import column_names_check
from ..dfcheck.dfcheck import dups_check
from ..dfclean.dfclean import na_clean

class Comparison():
    def __init__(self):
        self.exceptions = None
        self.results = None
        self.comparison = None

    def compare(self, x, y, k, qty_n = [], keep_comparison = False, dec_rnd = 8, thrshld = 0):
        """compares data of the two dataframes based on a common key
        Parameters:
          x (pandas dataframe): a pandas dataframe
          y (pandas dataframe): a pandas dataframe
          k (list): list of names in the key
          qty_n (list): list of quantities field names for comparison (optional)
          keep_comparison (bool): indicates if the entire comparison should be retained (the "full outer join" vs just exceptions)
          dec_rnd (int): the number of decimal places to round the quantity fields before comparison
          thrshld (float): a threshold for determining if a quantity difference should be considered an exception
        Returns (via _exceptions_identifier() decribed below):
          Sets the object instance's exceptions parameter to a dataframe of exceptions found during the comparison
          Sets the object instance's results parameter to a dataframe with records counts for the result of the comparison
          If keep_comparison = True, sets the object instances' comparison parameter to the dataframe with result of the "full outer join"
          Note: The compare() does a column name check to make sure both x and y have the fields in the key.
          If that fails, a message is printed and the parameters are not set/reset.
        """

        # column names check
        xc = column_names_check(x, k + qty_n)
        yc = column_names_check(y, k + qty_n)
        if (len(xc[xc['column_check_pass'] == 'False'].index) + len(yc[yc['column_check_pass'] == 'False'].index) != 0):
            print("column name check failed")
            xc['df_ref'] = 'x'
            yc['df_ref'] = 'y'
            print(pd.concat([xc, yc]))

        else:
            # dups check
            xd = dups_check(x, k)
            if(len(xd.index) != 0):
                print("There are dups in the x table:")
                print(xd)

            yd = dups_check(y, k)
            if(len(yd.index) != 0):
                print("There are dups in the y table:")
                print(yd)

            # clean up NA
            x = na_clean(x, qty_n)
            y = na_clean(y, qty_n)

            #create new dataframe for outer join of x and y
            z = x.merge(y, how = 'outer', on = k, indicator = True)

            #compare quantity
            if qty_n != []:
                z = self._qty_compare(z, qty_n, dec_rnd, thrshld)

            self._exceptions_identifier(x, y, z, qty_n, keep_comparison)

    def _qty_compare(self, df, qty_n, dec_rnd, thrshld):
        """compares the quantites in a dataframe
        Parameters:
          df (pandas dataframe): a pandas dataframe with quantity fields for comparison
          qtn_n (list): list of quantity field(s) for comparison
            (needs to be the name of the common quantity field between two dataframes that were merged)
          dec_rnd (int): the number of decimal places to round the quantity fields before comparison
          thrshld (float): a threshold for determining if a quantity difference should be considered an exception
        Returns:
          df (pandas dataframe): a pandas dataframe that includes a field for each quantity comparison
        """

        # initialize a counter that will be used to count quantity comparison that are above the threshold for each record
        df['diff_counter'] = 0
        for i in qty_n:
            # round the quantity fields by the passed in value
            # quantity field names are the value from the passed in quantity field list (i in qty_n) plus either underscore x or y
            df[i + '_x'] = df[i + '_x'].round(dec_rnd)
            df[i + '_y'] = df[i + '_y'].round(dec_rnd)

            # create a field to calculate the difference between the x and y quantities
            # field name is 'diff_' plus name of the quantity field
            df['diff_' + i] = (df[i + '_x'] - df[i + '_y'])

            # determine if the differences is greater than the threshold: 1 if Yes, 0 if No
            df['diff_test'] = np.where(abs(df['diff_' + i]) > abs(thrshld), 1, 0)

            # update the difference counter with the difference comparison to threshold result
            df['diff_counter'] = df['diff_counter'] + df['diff_test']

        return df

    def _exceptions_identifier(self, x, y, z, qty_n, keep_comparison):
        """classifies exceptions after two dataframes are compared
        Parameters:
          x (pandas dataframe): a pandas dataframe
          y (pandas dataframe): a pandas dataframe
          k (list): list of names in the key
          qty_n (list): list of quantities field names for comparison (optional)
          keep_comparison (bool): indicates if the entire comparison should be retained (the "full outer join" vs just exceptions)
        Returns:
          Sets the object instance's exceptions parameter to a dataframe of exceptions found during the comparison
          Sets the object instance's results parameter to a dataframe with records counts for the result of the comparison
          If keep_comparison = True, sets the object instances' comparison parameter to the dataframe with result of the "full outer join"
        """

        #determine 'expections': not in x, not in y, or diff quantity
        if qty_n == []:
            #label exceptions
            conditions = [
                (z['_merge'] == 'right_only'),
                (z['_merge'] == 'left_only'),
                (z['_merge'] == 'both')
            ]

            names = ['not_in_x', 'not_in_y', 'match']

            z.loc[:, ('exception_type')] = np.select(conditions, names)

            #record counts used to ensure all records are accounted for
            rc_z = len(z.index) #records from outer join of x and y
            rc_same = len(z[(z['_merge'] == 'both')].index) #records that match dim and quantity
            rc_notinx = len(z[z['_merge'] == 'right_only'].index) #records in y but not x
            rc_notiny = len(z[z['_merge'] == 'left_only'].index) #records in x but not y

            z = z.drop(['_merge'], axis = 1)

            exceptions = z[(z['exception_type'] == 'not_in_x') | (z['exception_type'] == 'not_in_y')]

            rc_ex = len(exceptions.index) #records considered an exception

            #record count check;
            #the record count from outer join (x and y) should eqaul:
            # - records that match, records only in x, records only in y
            rec_chk = rc_z - rc_same - rc_notinx - rc_notiny

            if rec_chk == 0:
                # print("All records accounted for")
                rec_chk_pass = True
            else:
                print("Record counts for same, diff, and in one but not other DO NOT match")
                rec_chk_pass = False

            #create one line line dataframe showing test check meta data
            data = [[rec_chk_pass, len(x.index), len(y.index), rc_z, rc_same, rc_notinx, rc_notiny, rc_ex]]
            self.results = pd.DataFrame(data, columns = ['rec_chk_pass', 'rec_count_x', 'rec_count_y', 'rec_count_z', 'rec_count_same', 'rec_count_notinx', 'rec_count_notiny', 'rec_count_ex'])

        else:
            #label exceptions
            conditions = [
                (z['_merge'] == 'right_only'),
                (z['_merge'] == 'left_only'),
                (z['diff_counter'] > 0),
                (z['diff_counter'] == 0)
            ]

            names = ['not_in_x', 'not_in_y', 'diff_qty', 'match']

            z.loc[:, ('exception_type')] = np.select(conditions, names)

            #record counts used to ensure all records are accounted for
            rc_z = len(z.index) #records from outer join of x and y
            rc_same = len(z[(z['_merge'] == 'both') & (z['diff_counter'] <= 0)].index) #records that match dim and quantity
            rc_diff = len(z[(z['_merge'] == 'both') & (z['diff_counter'] > 0)].index) #records that match dim but have diff quantity
            rc_notinx = len(z[z['_merge'] == 'right_only'].index) #records in y but not x
            rc_notiny = len(z[z['_merge'] == 'left_only'].index) #records in x but not y

            z = z.drop(['_merge', 'diff_test', 'diff_counter'], axis = 1)

            #isolate exceptions
            exceptions = z[(z['exception_type'] == 'not_in_x') | (z['exception_type'] == 'not_in_y') | (z['exception_type'] == 'diff_qty')]

            rc_ex = len(exceptions.index) #records considered an exception

            #record count check;
            #the record count from outer join (x and y) should eqaul:
            # - records that match, records that are different, records only in x, records only in y
            rec_chk = rc_z - rc_same - rc_diff - rc_notinx - rc_notiny

            if rec_chk == 0:
                # print("All records accounted for")
                rec_chk_pass = True
            else:
                print("Record counts for same, diff, and in one but not other DO NOT match")
                rec_chk_pass = False

            #create one line line dataframe showing test check meta data
            data = [[rec_chk_pass, len(x.index), len(y.index), rc_z, rc_same, rc_diff, rc_notinx, rc_notiny, rc_ex]]
            self.results = pd.DataFrame(data, columns = ['rec_chk_pass', 'rec_count_x', 'rec_count_y', 'rec_count_z', 'rec_count_same', 'rec_count_diff', 'rec_count_notinx', 'rec_count_notiny', 'rec_count_ex'])

        #assign expections to object instance
        self.exceptions = exceptions

        #assign the comparison to object instance is keep_comparison == True
        if keep_comparison == True:
            self.comparison = z
