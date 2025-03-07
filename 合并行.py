import pandas as pd
import numpy as np


data = pd.read_excel(r"V:\huihui\data\icu数据提取-李一鸣\表1.xlsx")
# print(data.head())
# print(data.columns.tolist())
# print(data.shape)

groups = data.groupby("患者编号", as_index=False)
# print(data.head())
# print(data.columns.tolist())
# print(data.shape)
new_data = pd.DataFrame(columns=data.columns.tolist())
ids = groups.all()['患者编号']
for id in ids:
    group = groups.get_group(id).sort_values(by="入院时间")
    # print(group)
    new_data = new_data._append(group.iloc[0, :])
new_data.to_excel(r"V:\huihui\data\icu数据提取-李一鸣\表1_v2.xlsx", index=False)
