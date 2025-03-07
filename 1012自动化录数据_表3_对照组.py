import json
import re
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
input_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\录数据\1008基线情况汇总_v2填充数据1012v1.xlsx"
output_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\录数据\1008基线情况汇总_v2填充数据1015_对照组四项.xlsx"
extracted_props = ["HR(bpm)", "Bp", "Resp", "SpO2"]
timing = ["入院12", "入院34", "入院56", "入院78"]
timing_postfix = ["", ".1", ".2", ".3"]
time_format = "%Y/%m/%d"
na = "NA"
df1 = pd.read_excel(input_file, sheet_name="Sheet1")
print(df1.columns.tolist())


col_pattern_map = {
    "HR(bpm)": ["HR(bpm)"],
    "Bp": ["NBP(mmHg)"],
    "Resp": ["Resp"],
    "SpO2": ["SpO2", "SpO2(%%)"]
}

# print(len(time_props))
# print(len(col_pattern_map))
# print(set(col_pattern_map.keys()).difference(set(time_props)))
# print(set(time_props).difference(set(col_pattern_map.keys())))
# exit(-1)

def get_num(x, prop):
    if prop == "Bp":
        return float(re.search(r"\(.*\)", x).group()[1:-1])
    else:
        try:
            return float(x)
        except Exception as e:
            print(e)
            return float('nan')


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
select `结果` as result from check_record_table3
where `住院号`='{id}'
  {check_item_rule}
  and (`记录时间` between '{from_day}' and '{to_day}')
order by `记录时间`"""
    try:
        df = pd.read_sql(sql, con=engine)
        df["value"] = df["result"].apply(lambda x: get_num(x, prop))
        df = df.sort_values(by="value")
    except Exception as e:
        print(sql)
        raise e
    if len(df) > 0:
        r1 = df.iloc[0, 0]
        r2 = df.iloc[df.shape[0]-1, 0]
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
            if t == "入院12":
                from_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=1)
                to_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=1)
            elif t == "入院34":
                from_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=3)
                to_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=3)
            elif t == "入院56":
                from_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=5)
                to_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=5)
            elif t == "入院78":
                from_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=7)
                to_day = df1.loc[index, "入院或入ICU时间.1"] + pd.Timedelta(days=7)
            else:  # 出院
                print("未知时间段")
                continue
            r1, r2 = get_result(f"ZY01000{df1.loc[index, '住院号']}", prop, from_day=from_day, to_day=to_day)
            df1.loc[index, col + "_min"] = r1
            df1.loc[index, col + "_max"] = r2
            pbar.update()
        pbar.close()
df1.to_excel(output_file, index=False)
