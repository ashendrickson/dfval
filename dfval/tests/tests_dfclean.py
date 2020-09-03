import unittest
from pandas.util.testing import assert_frame_equal

from dfval import na_clean
import pandas as pd

class TestClean(unittest.TestCase):
    def setUp(self):
        self.d_na_clean = [[3, '2019-12-15', None], [3, '2019-12-22', 200], [3, '2019-12-29', 500], [3, '2019-12-08', 75]]
        self.df_na_clean = pd.DataFrame(self.d_na_clean, columns = ['co_loc_ref_i', 'wk_beg_d', 'qty_sum'])

        self.d_no_na_clean = [[3, '2019-12-15', 100], [3, '2019-12-22', 200], [3, '2019-12-29', 500], [3, '2019-12-08', 75]]
        self.df_no_na_clean = pd.DataFrame(self.d_no_na_clean, columns = ['co_loc_ref_i', 'wk_beg_d', 'qty_sum'])

        self.qty_n = ['qty_sum']

    def test_na_clean(self):
        df_after = na_clean(self.df_na_clean, self.qty_n)
        self.assertEqual(sum(df_after['qty_sum']), 775)

    def test_no_na_clean(self):
        df_after = na_clean(self.df_no_na_clean, self.qty_n)
        assert_frame_equal(self.df_no_na_clean, df_after)

if __name__ == '__main__':
    unittest.main()
