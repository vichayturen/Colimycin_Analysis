import pandas as pd


files = [
    r"V:\huihui\data\icu数据提取-李一鸣\2020-2023脓毒症.xlsx",
    r"V:\huihui\data\icu数据提取-李一鸣\表2.xlsx",
    r"V:\huihui\data\icu数据提取-李一鸣\表56.xlsx",
    r"V:\huihui\data\icu数据提取-李一鸣\表7.xlsx",
]

result = r"V:\huihui\data\icu数据提取-李一鸣\表1_2_56_7.xlsx"
tables = []


for file in files:
    df = pd.read_excel(file)
    print(df.shape)
    # print(df["患者编号"].value_counts().to_dict())
    tables.append(df)
print("=" * 50)
# tables[1] = tables[1].drop(columns=['患者编号'])
# tables[2] = tables[2].drop(columns=['患者编号'])
# tables[3] = tables[3].drop(columns=['患者编号'])
cols = []
for t in tables:
    for c in t.columns.tolist():
        if c not in cols:
            cols.append(c)
final = pd.DataFrame(columns=cols)
for i, row in tables[0].iterrows():
    properties = row.to_dict()
    loop = 1
    for j, r2 in tables[1].iterrows():
        if r2['住院号'] == properties['住院号']:
            tmp_properties = r2.to_dict()
            for k, v in tmp_properties.items():
                if k not in properties:
                    properties[k] = v
                    loop = 0
                    break
        if loop == 0:
            break
    loop = 1
    for j, r2 in tables[2].iterrows():
        if r2['住院号'] == properties['住院号']:
            tmp_properties = r2.to_dict()
            for k, v in tmp_properties.items():
                if k not in properties:
                    properties[k] = v
                    loop = 0
                    break
        if loop == 0:
            break
    loop = 1
    for j, r2 in tables[3].iterrows():
        if r2['住院号'] == properties['住院号']:
            tmp_properties = r2.to_dict()
            for k, v in tmp_properties.items():
                if k not in properties:
                    properties[k] = v
                    loop = 0
                    break
        if loop == 0:
            break
    final = final._append(properties, ignore_index=True)
print(final.shape)
print(final["患者编号"].value_counts().tolist())
final.to_excel(result, index=False)
