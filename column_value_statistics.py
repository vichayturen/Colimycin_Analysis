import pandas as pd

pd.set_option("display.max_row", None)


data = pd.read_excel("data/可利霉素分析(1).xlsx")


columns = data.columns.tolist()

for col in columns:
    data_col = data[col]
    print("=" * 50)
    # print(col)
    print(data_col.value_counts(dropna=False))
    print("sum is", data_col.value_counts(dropna=False).sum())

