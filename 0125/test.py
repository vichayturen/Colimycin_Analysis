
import pandas as pd
from scipy.stats import ttest_ind, normaltest, ks_2samp, chi2_contingency, spearmanr
pd.options.display.max_rows = None
pd.options.display.max_columns = None


data = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学_检验1_去除初用.xlsx", sheet_name="检验1")
print(data.columns.tolist())

cols = [
    'WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', '血沉', 'IL6'
]

postfix_couples = [
    (".1", ".2", "可前 vs 可D1-D2"),
    (".1", ".3", "可前 vs 可D3-D4"),
    (".1", ".4", "可前 vs 可D5-D6"),
    (".1", ".5", "可前 vs 可D7-D8"),
]

confidence = 0.05

table = []
for col in cols:
    for postfix1, postfix2, time_feat in postfix_couples:
        row = {}
        row["变量"] = col
        row["时间特征"] = time_feat
        col1 = col + postfix1
        col2 = col + postfix2
        data_col1 = pd.to_numeric(data[col1], errors="coerce")
        data_col2 = pd.to_numeric(data[col2], errors="coerce")
        row["左非空数量"] = pd.notna(data_col1).sum()
        row["右非空数量"] = pd.notna(data_col2).sum()
        description = data_col1.describe()
        for k, v in description.items():
            row["左_" + k] = v
        description = data_col2.describe()
        for k, v in description.items():
            row["右_" + k] = v
        all_items = data_col1 + data_col2
        test_result = normaltest(all_items, nan_policy="omit")
        row["正态检验p值"] = test_result.pvalue
        if test_result.pvalue > confidence:
            row["是否正态"] = True
            row["检验类型"] = "两独立样本t检验"
            test_result = ttest_ind(data_col1, data_col2, nan_policy="omit")
            row["p值"] = test_result.pvalue
        else:
            row["是否正态"] = False
            row["检验类型"] = "两样本Kolmogorov-Smirnov检验"
            test_result = ks_2samp(data_col1.dropna(), data_col2.dropna())
            row["p值"] = test_result.pvalue
        if row["p值"] < confidence:
            row["是否有差异"] = "是"
        else:
            row["是否有差异"] = "否"
        table.append(row)
dist_test_df = pd.DataFrame(table)
print(dist_test_df)
dist_test_df.to_excel(r"C:\Users\Vichayturen\Desktop\projects\huihui\keli\0125\test_result.xlsx", index=False)
