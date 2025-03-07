# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import pingouin as pg
from tabulate import tabulate
from datetime import datetime
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

plt.rcParams['font.sans-serif'] = ['simhei']  # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
pd.set_option('display.width', 180)  # 150，设置打印宽度
pd.set_option('display.max_rows', None)
pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', 40)

# 创建一个 DataFrame
data = pd.read_excel('../data/可利霉素_wkyc_02_fillvalue.xlsx')


# 过滤掉所有结束时间-开始时间小于3天的行

# 定义一个函数，该函数返回持续时间大于等于3天的行的布尔序列
def filter_func(x):
    if pd.isna(x["可利霉素开始时间"]) or pd.isna(x["结束可利霉素时间"]):
        return False
    return (datetime.strptime(x['结束可利霉素时间'], "%Y/%m/%d") - datetime.strptime(x['可利霉素开始时间'],
                                                                                     "%Y/%m/%d")) >= pd.Timedelta(days=2)

print(len(data))
data = data[data.apply(filter_func, axis=1)]
print(len(data))

special_col = "WBC"

data[special_col] = pd.to_numeric(data[special_col], errors='coerce')
# data[special_col] = np.log(pd.to_numeric(data[special_col], errors='coerce'))
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []
for i, row in data.iterrows():
    if row["时间标签"] == "可利霉素前":
        if not pd.isna(row[special_col]):
            s1.append(row[special_col])
    elif row["时间标签"] == "可利霉素后第3天":
        if not pd.isna(row[special_col]):
            s2.append(row[special_col])
    elif row["时间标签"] == "可利霉素后第5天":
        if not pd.isna(row[special_col]):
            s3.append(row[special_col])
    elif row["时间标签"] == "可利霉素后第7天":
        if not pd.isna(row[special_col]):
            s4.append(row[special_col])
    elif row["时间标签"] == "结束可利霉素":
        if not pd.isna(row[special_col]):
            s5.append(row[special_col])
    elif row["时间标签"] == "出院":
        if not pd.isna(row[special_col]):
            s6.append(row[special_col])

print(len(s1), len(s2), len(s3), len(s4), len(s5), len(s6))
max_len = max(len(s1), len(s2), len(s3))
mean = sum(s1) / len(s1)
for i in range(max_len-len(s1)):
    s1.append(mean)
mean = sum(s2) / len(s2)
for i in range(max_len-len(s2)):
    s2.append(mean)
mean = sum(s3) / len(s3)
for i in range(max_len-len(s3)):
    s3.append(mean)
mean = sum(s4) / len(s4)
for i in range(max_len-len(s4)):
    s4.append(mean)
mean = sum(s5) / len(s5)
for i in range(max_len-len(s5)):
    s5.append(mean)
mean = sum(s6) / len(s6)
for i in range(max_len-len(s6)):
    s6.append(mean)
result = stats.friedmanchisquare(s1, s2, s3, s4, s5, s6)
print(result)
