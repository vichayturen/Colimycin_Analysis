import pandas as pd
from scipy import stats

# 创建一个示例 DataFrame
data = {
    'condition1': [20, 21, 19, 20, 22],
    'condition2': [21, 20, 20, 21, 22]
}
df = pd.DataFrame(data)

# 选择两列进行配对样本t检验
column1 = 'condition1'
column2 = 'condition2'

# 进行t检验
t_stat, p_value = stats.ttest_rel(df[column1], df[column2])

# 打印结果
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")
