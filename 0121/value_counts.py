import re

import pandas as pd
from scipy.stats import normaltest
pd.options.display.max_rows = None
pd.options.display.max_columns = None


# data = pd.read_excel(r"C:\Users\Vichayturen\Desktop\projects\huihui\可利霉素分析结果\可利霉素病原学.xls", sheet_name="二次感染")
data = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学原表_基线情况_去除初用.xlsx", sheet_name="基线情况")
# data = pd.read_excel(r"C:\Users\Vichayturen\Desktop\projects\huihui\可利霉素分析结果\可利霉素病原学.xls", sheet_name="二次感染")
# data = pd.read_excel(r"C:\Users\Vichayturen\Desktop\projects\huihui\可利霉素分析结果\可利霉素病原学.xls", sheet_name="二次感染")
# data = pd.read_excel(r"C:\Users\Vichayturen\Desktop\projects\huihui\可利霉素分析结果\可利霉素病原学.xls", sheet_name="二次感染")
print(data.columns.tolist())

# 离散值占比
column = "肝脏疾病"
result = data[column].value_counts(dropna=False)
print(result)
print(result / result.sum())
pd.DataFrame({
    "值": result.index,
    "例数": result.to_list(),
    "百分比": (result / result.sum()).to_list()
}).to_excel(rf"C:\Users\Vichayturen\Desktop\projects\huihui\可利霉素分析结果\value_counts_result\{column}value_counts.xlsx", na_rep="NA", index=False)

# # 连续值描述
# column = "nian"
# print(normaltest(data[column], nan_policy="omit"))
# result = data[column].describe()
# print(result)

# # 多离散占比
# column = "停用原因"
# result = data[column].tolist()
# value_counts = {}  # 选项：出现行数
# for res in result:  # res是每行的整体字符串
#     if pd.isna(res) or res in ("无", "不详"):  # 是否满足“不详”这个条件
#         value_counts["不详"] = value_counts.get("不详", 0) + 1
#         continue
#     if isinstance(res, int):
#         value_counts[str(res)] = value_counts.get(str(res), 0) + 1
#         continue
#     options = re.split(r"[、，+]", res)  # 用逗号或者顿号来分割成不同字符串
#     print(options)
#     s = set()
#     for option in options:
#         option = option.strip()  # 把字符串两端的空格去掉
#         if option not in s:
#             value_counts[option] = value_counts.get(option, 0) + 1
#             s.add(option)
# value_counts = pd.Series(value_counts).sort_values(ascending=False)
# print(value_counts)
# value_counts.to_excel(rf"C:\Users\Vichayturen\Desktop\projects\huihui\可利霉素分析结果\value_counts_result\{column}value_counts.xlsx")
