import json
from datetime import datetime
from copy import deepcopy
from typing import Optional

import pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine
pd.set_option('display.width', 180)  # 150，设置打印宽度
pd.set_option("display.max_columns", 10)
pd.set_option('display.max_colwidth', 40)

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/medical?charset=utf8mb4")


# 常量
input_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\1210检验结果.xls"
output_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\1210检验结果_v1.0.xlsx"
extracted_props = ["HR(bpm)", "Bp", "Resp", "SpO2"]
timing = ["入院或入ICU时间", "可利霉素前24小时", "可D1-2", "可后D3-D4", "可后D5-D6", "可后D7-D8"]
timing_postfix = ["", ".1", ".2", ".3", ".4", ".5"]
time_format = "%Y/%m/%d"
na = "NA"
df1 = pd.read_excel(input_file, sheet_name="Sheet1")
print(df1.columns.tolist())
exit(0)


sql_map = {
    "WBC": "select * from check_record where `检验项目名称` like '%%血常规分析%%' `检验子项结果` like '%%白细胞%%'",
}

# print(len(time_props))
# print(len(col_pattern_map))
# print(set(col_pattern_map.keys()).difference(set(time_props)))
# print(set(time_props).difference(set(col_pattern_map.keys())))
# exit(-1)

def get_result(
        id: str,
        prop: str,
        from_day: Optional[datetime] = None,
        to_day: Optional[datetime] = None,
        desc: bool = False) -> tuple:
    check_setting = col_pattern_map[prop]
    if from_day is not None:
        from_day = from_day.replace(hour=0, minute=0, second=0)
    if to_day is not None:
        to_day = to_day.replace(hour=23, minute=59, second=59)
    check_item_rule = " and (" + " or ".join(
        [f"`项目` = '{keyword}'" for keyword in check_setting]) + ")"
    sql = f"""\
select min(`结果`) as min, max(`结果`) as max from check_record_table3
where `住院号`='{id}'
  {check_item_rule}
  and (`记录时间` between '{from_day}' and '{to_day}')
order by `记录时间`"""
    if desc:
        sql += " desc"
    try:
        df = pd.read_sql(sql, con=engine)
    except Exception as e:
        print(sql)
        raise e
    if len(df) > 0:
        r1 = df.loc[0, 'min']
        r2 = df.loc[0, 'max']
        return r1, r2
    else:
        return na, na



# exit(-1)
# def filter_func(x) -> bool:
#     return not pd.isna(x["可利霉素开始时间"])
# df_wkyc = df_wkyc[df_wkyc.apply(filter_func, axis=1)]

# d = {
#     "before": ["可利霉素前24小时", "可D1"],
#     "3": ["可后D3-D4", "可后D5-D6"],
#     "5": ["可后D5-D6", "可后D7-D8"],
#     "7": ["可后D7-D8", "结束可利霉素时间.1"],
#     "stop": ["结束可利霉素时间.1", "出院时间.1"],
#     "discharge": ["出院时间.1", ""]
# }

for ip, prop in enumerate(extracted_props):
    for t, postfix in zip(timing, timing_postfix):
        col = prop + "_" + t
        df1[col + "_min"] = ""
        df1[col + "_max"] = ""

for ip, prop in enumerate(extracted_props):
    print(f"正在处理属性{prop}({ip}/{len(extracted_props)})")
    for t, postfix in zip(timing, timing_postfix):
        col = prop + "_" + t
        pbar = tqdm(total=len(df1))
        for index, row in df1.iterrows():
            desc = False
            if t == "入院或入ICU时间":
                from_day = df1.loc[index, "入院或入ICU时间"]
                to_day = df1.loc[index, "可利霉素前24小时"]
            elif t == "可利霉素前24小时":
                from_day = df1.loc[index, "入院或入ICU时间"]
                to_day = df1.loc[index, "可利霉素前24小时"]
                desc = True
            elif t == "可D1-2":
                from_day = df1.loc[index, "可D1-2"] + pd.Timedelta(days=1)
                to_day = df1.loc[index, "可D1-2"] + pd.Timedelta(days=2)
            elif t == "可后D3-D4":
                from_day = df1.loc[index, "可后D3-D4"] + pd.Timedelta(days=0)
                to_day = df1.loc[index, "可后D3-D4"] + pd.Timedelta(days=1)
            elif t == "可后D5-D6":
                from_day = df1.loc[index, "可后D5-D6"] + pd.Timedelta(days=0)
                to_day = df1.loc[index, "可后D5-D6"] + pd.Timedelta(days=1)
            elif t == "可后D7-D8":
                from_day = df1.loc[index, "可后D7-D8"] + pd.Timedelta(days=0)
                to_day = df1.loc[index, "可后D7-D8"] + pd.Timedelta(days=1)
            else:  # 出院
                print("未知时间段")
                continue
            r1, r2 = get_result(f"ZY01000{df1.loc[index, '住院号']}", prop, from_day=from_day, to_day=to_day, desc=desc)
            df1.loc[index, col + "_min"] = r1
            df1.loc[index, col + "_max"] = r2
            pbar.update()
        pbar.close()
df1.to_excel(output_file, index=False)
