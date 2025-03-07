import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.model_selection import RepeatedKFold
from tqdm import tqdm


data = pd.read_excel('data/可利霉素分析.xlsx', sheet_name='检验1', index_col="姓名")

def map_object_to_na(value):
    if isinstance(value, str):
        return float('nan')
    if isinstance(value, int):
        return float(value)
    # print(type(value))
    return value

props = ['WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', 'IL6']
for prop in props:
    sub_props = [prop]
    for i in range(1, 7):
        sub_props.append(f'{prop}.{i}')
    sub_data = data[sub_props]
    sub_data = sub_data.applymap(map_object_to_na)
    sub_data = sub_data.dropna(axis=0, how='all')
    sub_data.transpose().to_csv(f'splits/{prop}.csv', index=False)
