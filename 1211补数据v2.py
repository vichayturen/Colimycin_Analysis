import json
from datetime import datetime
from copy import deepcopy
from typing import Optional

import pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine
pd.set_option('display.width', 180)  # 150，设置打印宽度
pd.set_option("display.max_columns", 10)
pd.set_option('display.max_colwidth', 40)

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/medical?charset=utf8mb4")


# 常量
input_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\1210检验结果_v1.0.csv"
output_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\1210检验结果_v1.0_step2.csv"
df1 = pd.read_csv(input_file)
print(df1.columns.tolist())
columns = set(df1.columns.tolist())
# exit(0)

for col in columns:
    if col.startswith("PCT") or col == "IL6":
        for i in range(df1.shape[0]):
            val = df1.loc[i, col]
            if isinstance(val, str):
                val = val.replace(">", "").replace("<", "")
                df1.loc[i, col] = val

df1.to_csv(output_file, index=False)
