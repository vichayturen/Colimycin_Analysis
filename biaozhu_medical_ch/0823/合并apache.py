import pandas as pd


df1 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/apache2 一区.xlsx')
df2 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/APACHE2 2020-2022.xlsx')
df3 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/Apache2 2022-2024.xlsx')
df4 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/二区APACHE.xlsx')
print(df1.shape)
print(df2.shape)
print(df3.shape)
print(df4.shape)


df = pd.concat([df1, df2, df3, df4], axis=0, ignore_index=True)
print(df.shape)
df.to_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/Apache2合并.xlsx', index=False)
