import pandas as pd


df = pd.read_excel(r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\基线情况11.18.xls", sheet_name="Sheet1")
print(df.dtypes.to_dict())
# exit(0)


for i, row in df.iterrows():
    if row["0死亡；1放弃；2康复；3出院"] in (0, 1):
        df.loc[i, "生存时间"] = row["出院或死亡时间"] - row["入院时间"]
        df.loc[i, "生存时间2"] = row["出院或死亡时间"] - row["入院或入ICU时间"]

df.to_excel(r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\基线情况11.18_v2.xlsx", index=False)
