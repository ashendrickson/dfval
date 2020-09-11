# dfval

`dfval` can be used to compare two dataframes and identify differences between the dataframes. It also has methods to validate attributes or update dataframes.

Below is example creates two small dataframes and does a comparison using `dfval` as well as more detail on how to use `dfval`.

## Example of `compare()`
**1. Import dfval and pandas**
```
import dfval as dv
import pandas as pd
```

**2. Create two dataframes (x and y)**
```
dx = [[5000, '2019-12-15', 100, 2], [5000, '2019-12-22', 200, 3], [5000, '2019-12-29', 500, 4], [5000, '2019-12-08', 75, 3]]
dfx = pd.DataFrame(dx, columns = ['loc_id', 'greg_d', 'qty_sum', 'qty_ct'])

dy = [[5000, '2019-12-15', 100.000001, 2], [5000, '2019-12-22', 190, 3], [5000, '2019-12-29', 500, 4], [5000, '2019-12-01', 75, 3]]
dfy = pd.DataFrame(dy, columns = ['loc_id', 'greg_d', 'qty_sum', 'qty_ct'])
```

**3. Define the key and quantity fields for comparison**
```
k = ['loc_id', 'greg_d']

qty_f = ['qty_sum', 'qty_ct']
```

**4. Call `compare()`**
```
# call compare passing the x dataframe, y dataframe, key, the quantity field name, and optionally the keep_comparison (True or False), decimal rounding, and threshold for quantity comparison
c = dv.compare(dfx, dfy, k, qty_f, keep_comparison = True, decimal_round = 4, threshold = 0.01)
```

**5. Contents of `c.results`**

rec_chk_pass | rec_count_x | rec_count_y | rec_count_z | rec_count_same | rec_count_diff | rec_count_notinx | rec_count_notiny | rec_count_ex
-------------|-------------|-------------|-------------|----------------|----------------|------------------|------------------|-------------
True | 4 | 4 | 5 | 2 | 1 | 1 | 1 | 3

**6. Contents of `c.exceptions`**

loc_id | greg_d | qty_sum_x | qty_ct_x | qty_sum_y | qty_ct_y | diff_qty_sum | diff_qty_ct | exception_type
-------------|----------|-----------|----------|-----------|----------|--------------|-------------|----------------
5000 | 2019-12-22 | 200.0 | 3.0 | 190.0 | 3.0 | 10.0 | 0.0 | diff_qty
5000 | 2019-12-08 | 75.0 | 3.0 | NaN | NaN | NaN | NaN | not_in_y
5000 | 2019-12-01 | NaN | NaN | 75.0 | 3.0 | NaN | NaN | not_in_x

**7. Contents of `c.comparison`**

loc_id | greg_d | qty_sum_x | qty_ct_x | qty_sum_y | qty_ct_y | diff_qty_sum | diff_qty_ct | exception_type
-------------|----------|-----------|----------|-----------|----------|--------------|-------------|----------------
5000	| 2019-12-15	| 100.0 |	2.0 |	100.0 |	2.0 |	0.0 |	0.0	| match
5000 | 2019-12-22 | 200.0 | 3.0 | 190.0 | 3.0 | 10.0 | 0.0 | diff_qty
5000	| 2019-12-29	| 500.0	| 4.0	| 500.0	| 4.0	| 0.0	| 0.0	| match
5000 | 2019-12-08 | 75.0 | 3.0 | NaN | NaN | NaN | NaN | not_in_y
5000 | 2019-12-01 | NaN | NaN | 75.0 | 3.0 | | NaN | NaN | not_in_x


## `compare()` detail
`compare()` can be used to compare dimensions in two dataframes or dimensions and quantity values. To compare dimensions only, leave out the `qty_n`, `decimal_round`, and `threshold` parameters listed below.

### Input

`compare()` has three required parameters and four optional parameters:

* **Required parameters**
  * `x`: one of two dataframes used the comparison (order doesn't matter)
  * `y`: second of two dataframes used in comparison (order doesn't matter)
  * `k`: a list of the common key in the dataframes used for comparison
* **Optional parameters**
  * `qty_n`: a list of the quantity field(s) to compare
    * **Note:** if the `qty_n` is not passed, `compare()` will do a comparison of the dimensions (`k`) only
  * `keep_comparison`: retains all the records of the comparison in results comparison dataframe
  * `decimal_round`: number of digits to round the quantity fields in the comparison (fields listed in `qty_n`)
  * `threshold`: a threshold for what should be considered an exception in the quantity comparison

### Output

`compare()` returns an object with two dataframes describing the results of the comparison and the exceptions.

* `exceptions`: one record for each difference
  * exception types (`exception_type`):
    * not_in_x: key is present in y dataframe but not x
    * not_in_y: key is present in x dataframe but not y
    * diff_qty: key is present in both x and y dataframe but difference in one or more of the quantity columns is greater than threshold
* `result`: one record showing counts for comparison
  * rec_chk_pass:
    * Does the record count in the outer join of x and y equal the sum of the record counts of: records that match, records with quantity difference, records in x by not y, and records in y but not x
    * As long as there are not duplicates in the key in the x or y dataset, this should always be `True`
* `comparison`: all records from the result of the comparison (only retained if `keep_comparison = True`
  * exception types are the same as the `exceptions` dataframe, plus this has the records that `match`

**Notes:**
* `compare()` first checks the x and y DataFrames to make sure both have all columns defined in the passed in key and quantity field(s). If one or more columns is missing in either DataFrame, a message prints ("column name check failed") and the comparison is not run. `exceptions` and `results` will be `None`.
* `NaN` values in the quantity fields in the x and y datasets are converted to zero. If this happens, a message is printed
* `compare()` checks for duplicate keys and prints a message if duplicates are found. The comparison continues to run and creates results. However, the results may be be what is expected. It is better to handle duplicates in the key prior to using `compare()`.
* The result of the record count check prints if the result is `FALSE`:
  * "Record counts for same, diff, and in one but not other DO NOT match"
