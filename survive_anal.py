import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter

# 假设df是你的DataFrame
# 'time'列是观察时间，'event'列是事件发生的指示（1表示事件发生，0表示被审查（censored））

import numpy as np

# 创建一个示例DataFrame
data = {
    'patient_id': [1, 2, 3, 4, 5],
    'time': [1, 2, 3, 4, 5],
    '用药前': [10, 15, 20, 25, 30],  # 用药前的生存时间
    '用药中': [5, 10, 15, 20, 25],   # 用药中的生存时间
    '用药后1天': [3, 5, 7, pd.NA, 10],  # 用药后1天的生存时间
    '用药后2天': [2, 4, pd.NA, pd.NA, 8],   # 用药后2天的生存时间
    '用药后3天': [1, pd.NA, pd.NA, pd.NA, 6],   # 用药后3天的生存时间
    'event': [0, 1, 1, 1, 0]  # 事件发生情况，1表示发生，0表示未发生（例如死亡或存活）
}

df = pd.DataFrame(data)

# 显示DataFrame
print(df)

# 处理缺失数据，这里假设'用药后1天'到'用药后3天'的数据如果缺失，则认为是提前退出
for col in ['用药后1天', '用药后2天', '用药后3天']:
    df[col + '_censored'] = df[col].isnull()  # 标记为censored
    df['time'] = df[col].fillna(df['time'])  # 更新时间

# 标记事件，这里假设如果'用药前'列有值，则事件未发生，否则事件发生
df['event'] = (~df['用药前'].notnull()).astype(int)

# 创建生存分析模型
kmf = KaplanMeierFitter()
kmf.fit(df)

# 绘制生存曲线
kmf.plot_survival_function()

# 使用Cox比例风险模型
cph = CoxPHFitter()
cph.fit(df)

# 打印模型摘要
print(cph.summary)
