import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.model_selection import RepeatedKFold
from tqdm import tqdm

# 假设df是你的数据表，其中包含红细胞指标
# 这里创建一个示例数据表
data = pd.read_excel('data/可利霉素分析.xlsx', sheet_name='检验1')
print(data.columns.tolist())
props = ['WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', 'IL6']
def map_object_to_na(value):
    if isinstance(value, str):
        return float('nan')
    if isinstance(value, int):
        return float(value)
    # print(type(value))
    return value

all_props = []
for prop in tqdm(props):
    all_props.extend([prop, prop+'.1', prop+'.2', prop+'.3', prop+'.4', prop+'.5', prop+'.6'])
    # print(prop)
df = data[all_props]

df = df.applymap(map_object_to_na)

# 初始化多重插补器
imputer = IterativeImputer(max_iter=10)

# 选择需要插补的列
columns_to_impute = [col for col in df.columns if df[col].isnull().any()]

# 进行多重插补
df_imputed = pd.DataFrame(imputer.fit_transform(df[columns_to_impute]), columns=columns_to_impute)

# 将插补后的数据合并回原始数据表
df_complete = df.copy()
df_complete[columns_to_impute] = df_imputed

for col in df_complete.columns:
    data[col] = df_complete[col]

# exit(0)
data.to_excel('data/可利霉素分析_检验1_imputed2.xlsx', index=False)
