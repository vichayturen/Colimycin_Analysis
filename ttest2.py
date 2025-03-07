import pandas as pd
from scipy import stats

# 创建一个示例 DataFrame
# data = {
#     'condition1': [20, 21, 19, 20, 22],
#     'condition2': [21, 20, 20, 21, 22]
# }
# df = pd.DataFrame(data)

df = pd.read_excel("data/可利霉素分析.xls", sheet_name="检验1")

print(df.columns.tolist())

# columns = ['WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', '血沉', 'IL6']
columns = ['PCT', 'CRP']

for post in ['.2', '.3', '.4', '.5','.6']:
    print(f"## time: {post}")
    for col in columns:
        print(f"### Column: {col}")
        # 选择两列进行配对样本t检验
        column1 = col
        column2 = col+post
        def strip_dayuxiaoyu(x):
            if isinstance(x, str):
                x = x.strip('<').strip('>')
            return x

        s1 = df[column1].map(strip_dayuxiaoyu).astype(float)
        s2 = df[column2].map(strip_dayuxiaoyu).astype(float)
        try:
            # 进行t检验
            t_stat, p_value = stats.ttest_rel(s1, s2, nan_policy='omit')

            # 打印结果
            print(f"T-statistic: {t_stat}")
            print(f"P-value: {p_value}")
            print(f"post-mean - pre-mean: {s2.mean() -s1.mean()}")
        except Exception as e:
            print(f"Error occurred for column {col}: {e}")
