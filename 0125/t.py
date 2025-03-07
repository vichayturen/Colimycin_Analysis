
import pandas as pd

data1 = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学.xls", sheet_name="检验1")
data2 = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学.xls", sheet_name="二次感染")
data3 = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学原表.xls", sheet_name="基线情况")

ids1 = data1["编号"]
ids2 = data2[data2["初用or换用"] == "初用"]["编号"]
data = data3[data3["编号"].isin(ids1) & ~data3["编号"].isin(ids2)]

data.to_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学原表_基线情况_去除初用.xlsx", index=False, sheet_name="基线情况")
