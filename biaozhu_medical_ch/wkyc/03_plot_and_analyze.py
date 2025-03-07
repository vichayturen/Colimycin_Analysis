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

special_col = "IL6"

data[special_col] = pd.to_numeric(data[special_col], errors='coerce')
# data[special_col] = np.log(pd.to_numeric(data[special_col], errors='coerce'))
# d = {
#     "可利霉素前": 0,
#     "可利霉素后第3天": 1,
#     "可利霉素后第5天": 2,
#     "可利霉素后第7天": 3,
#     "结束可利霉素": 4,
#     "出院": 5
# }
# data["时间标签"] = data["时间标签"].map(lambda x: d[x])
# # 描述性统计
# print(data['淋巴细胞'].describe())


# 使用卡方检验选择前两个最佳特征
# print("## 卡方检验")
# data = data.dropna(axis=0, subset=["淋巴细胞"])
# KB_chi2 = SelectKBest(chi2, k=1)
# X_new = KB_chi2.fit_transform(data[["淋巴细胞"]], data["时间标签"])  # 输入特征减少到仅包含通过卡方检验选择出的前2个特征。
# print(KB_chi2.pvalues_)
#
#
# # print(data.head())
#
#
# # 重塑数据为宽格式
# data_wide = data.pivot(index='住院号', columns='时间标签', values='淋巴细胞')

#
# print(data_wide.head())
# print(data_wide.shape)

# # 方差齐性检验（Levene检验）
# levene_result = pg.homoscedasticity(data_wide, method='levene')
# print("\n## Levene's test for equality of variances:")
# print(tabulate(levene_result, headers='keys', tablefmt='grid'))
#
# # 重复测量方差分析
# rm_anova_result = pg.rm_anova(data_wide, detailed=True)
# print("\n## Repeated measures ANOVA:")
# print(tabulate(rm_anova_result, headers='keys', tablefmt='grid'))
#
# # 事后检验（配对t检验，使用Bonferroni校正）
# # posthoc_result = pg.pairwise_tests(data_wide, dv="", padjust='bonferroni')
# # print("\n## Post-hoc tests (paired t-tests with Bonferroni correction):")
# # print(tabulate(posthoc_result, headers='keys', tablefmt='grid'))
#
# import pingouin as pg
#
# # 重复测量方差分析
# rm_anova_result = pg.rm_anova(data_wide, detailed=True)
# print("Repeated measures ANOVA:")
# print(tabulate(rm_anova_result, headers='keys', tablefmt='grid'))
#
# # 计算partial η²
# partial_eta_squared = rm_anova_result['SS'][0] / (rm_anova_result['SS'][0] + rm_anova_result['SS'][1])
# print(f"Partial η² (Partial Eta-squared): {partial_eta_squared:.3f}")
#
# # 计算Generalized η²
# generalized_eta_squared = rm_anova_result['SS'][0] / rm_anova_result['SS'].sum()
# print(f"Generalized η² (Generalized Eta-squared): {generalized_eta_squared:.3f}")

# exit(0)

# 使用 seaborn 绘制箱形图
sns.boxplot(x='时间标签', y=special_col, data=data, width=0.8, whis=100)

plt.xlabel('时间', fontsize=8)
# plt.ylabel(special_col, fontsize=8)
plt.ylabel(f"log {special_col}", fontsize=8)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# 显示图形
plt.show()
