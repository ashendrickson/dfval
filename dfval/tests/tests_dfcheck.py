import unittest

from dfval import dups_check
from dfval import column_names_check
import pandas as pd

class TestCheck(unittest.TestCase):
    def setUp(self):
        self.d_dups = [[3, '2019-12-15'], [3, '2019-12-15'], [3, '2019-12-15'], [3, '2019-12-08']]
        self.df_dups = pd.DataFrame(self.d_dups, columns = ['co_loc_ref_i', 'wk_beg_d'])

        self.d_no_dups = [[3, '2019-12-15'], [3, '2019-12-22'], [3, '2019-12-29'], [3, '2019-12-08']]
        self.df_no_dups = pd.DataFrame(self.d_no_dups, columns = ['co_loc_ref_i', 'wk_beg_d'])

        self.k = ['co_loc_ref_i', 'wk_beg_d']

        self.d_column_names = [[3, '2019-12-15'], [3, '2019-12-15'], [3, '2019-12-15'], [3, '2019-12-08']]
        self.df_column_names = pd.DataFrame(self.d_dups, columns = ['co_loc_ref_i', 'wk_beg_d'])

        self.expected_column_names_match = ['co_loc_ref_i', 'wk_beg_d']
        self.expected_column_names_diff = ['co_loc_i', 'wk_beg_d']

    def test_dups(self):
        dups = dups_check(self.df_dups, self.k)
        self.assertEqual(len(dups.index), 2)

    def test_no_dups(self):
        dups = dups_check(self.df_no_dups, self.k)
        self.assertEqual(len(dups.index), 0)

    def test_column_names_match(self):
        column_names_result = column_names_check(self.df_column_names, self.expected_column_names_match)
        self.assertEqual(len(column_names_result[column_names_result['column_check_pass'] == 'True'].index), 2)
        self.assertEqual(len(column_names_result[column_names_result['column_check_pass'] == 'False'].index), 0)

    def test_column_names_diff(self):
        column_names_result = column_names_check(self.df_column_names, self.expected_column_names_diff)
        self.assertEqual(len(column_names_result[column_names_result['column_check_pass'] == 'True'].index), 1)
        self.assertEqual(len(column_names_result[column_names_result['column_check_pass'] == 'False'].index), 1)

if __name__ == '__main__':
    unittest.main()
