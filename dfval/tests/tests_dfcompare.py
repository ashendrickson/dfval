import unittest

from dfval import compare
import pandas as pd

class TestCompare(unittest.TestCase):
    def setUp(self):
        self.dx_qty = [[3, '2019-12-15', 100, 2], [3, '2019-12-22', 200, 3], [3, '2019-12-29', 500, 4], [3, '2019-12-08', 75, 3]]
        self.dfx_qty = pd.DataFrame(self.dx_qty, columns = ['co_loc_ref_i', 'wk_beg_d', 'qty_sum', 'qty_ct'])

        self.dy_qty_match = [[3, '2019-12-15', 100, 2], [3, '2019-12-22', 200, 3], [3, '2019-12-29', 500, 4], [3, '2019-12-08', 75, 3]]
        self.dfy_qty_match = pd.DataFrame(self.dy_qty_match, columns = ['co_loc_ref_i', 'wk_beg_d', 'qty_sum', 'qty_ct'])

        self.dy_qty_diff = [[3, '2019-12-15', 100, 2], [3, '2019-12-22', 190, 3], [3, '2019-12-29', 500, 4], [3, '2019-12-08', 75, 4]]
        self.dfy_qty_diff = pd.DataFrame(self.dy_qty_diff, columns = ['co_loc_ref_i', 'wk_beg_d', 'qty_sum', 'qty_ct'])

        self.dx_dim = [[3, '2019-12-15'], [3, '2019-12-22'], [3, '2019-12-29'], [3, '2019-12-01']]
        self.dfx_dim = pd.DataFrame(self.dx_dim, columns = ['co_loc_ref_i', 'wk_beg_d'])

        self.dy_dim_match = [[3, '2019-12-15'], [3, '2019-12-22'], [3, '2019-12-29'], [3, '2019-12-01']]
        self.dfy_dim_match = pd.DataFrame(self.dy_dim_match, columns = ['co_loc_ref_i', 'wk_beg_d'])

        self.dy_dim_diff = [[3, '2019-12-15'], [3, '2019-12-22'], [3, '2019-12-29'], [3, '2019-12-08']]
        self.dfy_dim_diff = pd.DataFrame(self.dy_dim_diff, columns = ['co_loc_ref_i', 'wk_beg_d'])

        self.k = ['co_loc_ref_i', 'wk_beg_d']
        self.qty_f = ['qty_sum', 'qty_ct']

    def test_compare_dim_qty_match(self):
        # call compare passing the x dataframe, y dataframe, key, quantity field name, and optionally decimal rounding and threshold for quantity comparison
        c = compare(self.dfx_qty, self.dfy_qty_match, self.k, self.qty_f, dec_rnd = 6, thrshld = 0.01)
        self.assertEqual(len(c.exceptions.index), 0)

    def test_compare_dim_qty_diff(self):
        # call compare passing the x dataframe, y dataframe, key, quantity field name, and optionally decimal rounding and threshold for quantity comparison
        c = compare(self.dfx_qty, self.dfy_qty_diff, self.k, self.qty_f, dec_rnd = 6, thrshld = 0.01)
        self.assertEqual(len(c.exceptions.index), 2)

    def test_compare_dim_match(self):
        # call compare passing the x dataframe, y dataframe, key, quantity field name, and optionally decimal rounding and threshold for quantity comparison
        c = compare(self.dfx_dim, self.dfy_dim_match, self.k)
        self.assertEqual(len(c.exceptions.index), 0)

    def test_compare_dim_diff(self):
        # call compare passing the x dataframe, y dataframe, key, quantity field name, and optionally decimal rounding and threshold for quantity comparison
        c = compare(self.dfx_dim, self.dfy_dim_diff, self.k)
        self.assertEqual(len(c.exceptions.index), 2)

    def test_compare_qty_keep(self):
        # call compare passing the x dataframe, y dataframe, key, quantity field name, and optionally decimal rounding and threshold for quantity comparison
        c = compare(self.dfx_qty, self.dfy_qty_diff, self.k, self.qty_f, keep_comparison = True, dec_rnd = 6, thrshld = 0.01)
        self.assertEqual(len(c.comparison.index), 4)

    def test_compare_dim_keep(self):
        # call compare passing the x dataframe, y dataframe, key, quantity field name, and optionally decimal rounding and threshold for quantity comparison
        c = compare(self.dfx_dim, self.dfy_dim_diff, self.k, keep_comparison = True, dec_rnd = 6, thrshld = 0.01)
        self.assertEqual(len(c.comparison.index), 5)

if __name__ == '__main__':
    unittest.main()
