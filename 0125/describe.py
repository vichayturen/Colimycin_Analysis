
import pandas as pd
from scipy.stats import ttest_ind, normaltest
pd.options.display.max_rows = None
pd.options.display.max_columns = None


data = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学_检验1_去除初用.xlsx", sheet_name="检验1")
print(data.columns.tolist())

cols = [
    'WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', '血沉', 'IL6'
]
postfixes = ["", ".1", ".2", ".3", ".4", ".5"]

confidence = 0.05

table = []
for col in cols:
    row = {}
    row["变量"] = col
    concat_cols = []
    for postfix in postfixes:
        concat_cols.append(pd.to_numeric(data[col + postfix], errors="coerce"))
    all_items = pd.concat(concat_cols, axis=0).dropna()
    test_result = normaltest(all_items)
    row["正态检验p值"] = test_result.pvalue
    description = all_items.describe()
    for key, value in description.items():
        row[key] = value
    if test_result.pvalue > confidence:
        row["是否正态"] = True
        row["特征"] = f"{description['mean']}(±{description['std']})"
    else:
        row["是否正态"] = False
        row["特征"] = f"{description['50%']}({description['25%']}~{description['75%']})"
    table.append(row)
dist_test_df = pd.DataFrame(table)
print(dist_test_df)
dist_test_df.to_excel(r"C:\Users\Vichayturen\Desktop\projects\huihui\keli\0125\test_result2.xlsx", index=False)
