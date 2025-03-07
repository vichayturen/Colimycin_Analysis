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
output_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\分析1210\1210检验结果_v1.0.csv"
time_format = "%Y/%m/%d"
na = ""
df1 = pd.read_excel(input_file, sheet_name="Sheet1")
print(df1.columns.tolist())
columns = set(df1.columns.tolist())
# exit(0)


sql_map = {
    "WBC": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` like '%%白细胞%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "N": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` like '%%中性粒细胞绝对值%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "L": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` like '%%淋巴细胞绝对值%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "MONO": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` like '%%单核细胞绝对值%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "HB": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` = '血红蛋白' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "PLT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` = '血小板' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "HCT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` like '%%血常规分析%%' and `检验子项中文名` like '%%红细胞压积%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",

    "ALT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%丙氨酸氨基转移酶%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "AST": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%天冬氨酸氨基转移酶%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "TB": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%总胆红素%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "DB": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%直接胆红素%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "ALB": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%白蛋白(ALB)%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "BUN": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%尿素氮%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "Cr": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%肌酐%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "Cysc": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%胱抑素C%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "PT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` = '凝血酶原时间' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "APTT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%活化部分凝血活酶时间%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "PTTA": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%凝血酶原时间活动度%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "TT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%凝血酶时间%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "INR": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` like '%%凝血酶原标准化比值%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",

    "G": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验项目名称` not like '%%尿%%' and `检验子项中文名` like '%%葡萄糖%%' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",

    "NA": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` in ('钠离子', '钠(Na+)') and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "K": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` in ('钾(K+)', '钾离子') and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "Mg": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` = '镁(Mg++)' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "Cl": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` in ('氯(Cl-)', '氯离子') and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "Ca": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` in ('钙离子', '钙(Ca++)') and `采集时间` between '{begin}' and '{end}' order by `采集时间`",

    "PCT": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` = '降钙素原' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
    "IL6": "select `检验子项结果` as result from check_record where `患者编号` = '{id}' and `检验子项中文名` = '白介素6' and `采集时间` between '{begin}' and '{end}' order by `采集时间`",
}

time2postfix = {
    "入院或入ICU时间": "",
    "可利霉素前24小时": ".1",
    "可D1-2": ".2",
    "可后D3-D4": ".3",
    "可后D5-D6": ".4",
    "可后D7-D8": ".5"
}

def get_result(
        id: str,
        prop: str,
        from_day: Optional[datetime] = None,
        to_day: Optional[datetime] = None,
        desc: bool = False):

    if from_day is not None:
        from_day = from_day.replace(hour=0, minute=0, second=0)
    if to_day is not None:
        to_day = to_day.replace(hour=23, minute=59, second=59)
    sql = sql_map[prop].format(
        id=id,
        begin=from_day,
        end=to_day
    )
    if desc:
        sql += " desc"
    try:
        df = pd.read_sql(sql, con=engine)
    except Exception as e:
        print(sql)
        raise e
    if len(df) > 0:
        return df.loc[0, 'result']
    else:
        return na

for index, row in df1.iterrows():
    if index >= 100:
        break
    for t, postfix in time2postfix.items():
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
        for prop in sql_map.keys():
            # if prop == "Cysc":
            #     print("debug")
            col = prop + postfix
            if col in columns:
                print(f"正在处理属性{index}行 {col}列")
            if col in columns and pd.isna(row[col]):
                result = get_result(str(int(row['患者编号'])), prop, from_day, to_day, desc)
                df1.loc[index, col] = result

df1.to_csv(output_file, index=False)
