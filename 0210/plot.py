
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False # 显示负号



data = pd.read_excel(r"c:\Users\Vichayturen\Desktop\projects\huihui\keli_data\可利霉素病原学_检验1_去除初用.xlsx", sheet_name="检验1")
print(data.columns.tolist())

props = [
    "WBC",
    "L",
    "N",
    "MONO",
    "PCT",
    "IL6",
]

fig, ax = plt.subplots(2, 3, figsize=(10, 6))

for i, prop in enumerate(props):
    new_data = {
        "时间标签": [],
        prop: []
    }

    for postfix, label in zip([".1", ".2", ".3", ".4", ".5"], ["使用前", "1-2天", "3-4天", "5-6天", "7-8天"]):
        column = pd.to_numeric(data[f"{prop}{postfix}"], errors="coerce")
        new_data[prop].extend(column)
        new_data["时间标签"].extend([label] * len(data[f"{prop}{postfix}"]))
    new_data = pd.DataFrame(new_data)

    if prop in ("PCT", "IL6"):
        new_prop = f"log({prop})"
        new_data[new_prop] = np.log(new_data[prop])
        prop = new_prop

    # plt.figure()
    sns.boxplot(x='时间标签', y=prop, data=new_data, width=0.8, whis=100, ax=ax[i//3][i%3])
    # plt.savefig(f"0210/可利霉素_{prop}_boxplot.png")
    # plt.close()
plt.savefig(f"0210/可利霉素_boxplot.png")
