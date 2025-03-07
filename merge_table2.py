import os
import pandas as pd


root = r"V:\huihui\data\ICU"
middle1 = ["一区", "二区", "三区"]
middle2 = r"常规查询"
# middle2 = r"基线情况"
output_dir = r"V:\huihui\data\监护系统"
df_list = []

count = 0
for m1 in middle1:
    dir_path = os.path.join(root, m1, middle2)
    file_list = os.listdir(dir_path)
    # print(dir_path, len(file_list))
    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        df = pd.read_excel(file_path, skiprows=[0, 1])
        # print(file_path)
        print(file_path)
        print(df.columns.tolist())
        count += 1
        # print(df.head())
        df_list.append(df)
print(count)
print(len(df_list))
final = pd.concat(df_list)
print(final.shape)

final.to_excel(os.path.join(output_dir, f"{middle2}.xlsx"), index=False)
