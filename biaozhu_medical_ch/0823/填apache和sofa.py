from config import pd


df1 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/Apache2合并.xlsx')
df2 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/baseline可利霉素.xls', sheet_name='基线情况')

print(df2.columns.tolist())
for row_index, row in df2.iterrows():
    print(f"开始处理第{row_index}行")
    if not pd.isna(row['APACHEII']):
        continue
    name = row['姓名']
    time1 = row['入院时间']
    df3 = df1[df1['姓名'] == name]
    df3 = df3.reset_index()
    if df3.shape[0] == 1:
        df2.loc[row_index, 'APACHEII'] = df3.loc[0, 'APACHE II评分']
        df2.loc[row_index, 'SOFA'] = df3.loc[0, 'SOFA评分']
    elif df3.shape[0] > 1:
        print(f"### {name}对应的入院时间是{time1}，有多个入院时间")
        print(df3[['姓名', '开始时间', 'APACHE II评分', 'SOFA评分']])
        input_row = int(input(f'请输入第几行：（从0开始）'))
        if input_row not in df3.index:
            input_row = int(input(f'输入错误，请输入第几行：（从0开始）'))
        df2.loc[row_index, 'APACHEII'] = df3.loc[input_row, 'APACHE II评分']
        df2.loc[row_index, 'SOFA'] = df3.loc[input_row, 'SOFA评分']


df2.to_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/baseline可利霉素_基线情况.xlsx', sheet_name='基线情况', index=False)
