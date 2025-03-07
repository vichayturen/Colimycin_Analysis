import pandas as pd

files = [
    r"V:\huihui\data\icu数据提取-李一鸣\表1.xlsx",
    r"V:\huihui\data\icu数据提取-李一鸣\表56.xlsx",
    r"V:\huihui\data\icu数据提取-李一鸣\表7.xlsx",
]

result = r"V:\huihui\data\icu数据提取-李一鸣\表1_56_7.xlsx"
tables = []

for file in files:
    df = pd.read_excel(file)
    print(df.shape)
    tables.append(df)
final = pd.concat(tables, axis=0)
print(final.shape)
final.to_excel(result, index=False)
