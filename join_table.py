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
tables[1] = tables[1].drop(columns=['患者编号'])
tables[2] = tables[2].drop(columns=['患者编号'])
tables[3] = tables[3].drop(columns=['患者编号'])

final = tables[0]
for i in range(1, len(tables)):
    final = pd.merge(final, tables[i], on="住院号", how="left")
    print(final.shape)
print(final.shape)
print(final["患者编号"].value_counts().tolist())
final.to_excel(result, index=False)
