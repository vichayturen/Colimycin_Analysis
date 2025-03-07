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
input_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\基线情况\1008基线情况汇总_v2填充数据1012v1.xlsx"
output_file = r"C:\Users\Administrator\Desktop\可利霉素分析结果\基线情况\1008基线情况汇总_v2填充数据1013_对照组检验.xlsx"
time_props = [
    "WBC", "HB", "PLT", "N", "L", "MONO", "HCT", "ALT", "AST", "TB", "DB", "ALB", "G", "BUN", "Cr",
    "K", "PT", "Cl", "Ca", "INR", "APTT", "TT", "PCT", "CRP", "血沉", "IL6"]
timing = ["入院12", "入院34", "入院56", "入院78"]
timing_postfix = ["", ".1", ".2", ".3"]
# timeing = ["before", "3", "5", "7", "stop", "discharge"]

time_format = "%Y/%m/%d"
na = "NA"
df1 = pd.read_excel(input_file, sheet_name="Sheet4")
print(df1.columns.tolist())

col_pattern_map = {
    # # "要填入的列名称的头": [[检查可以包含的关键词], [检查子表内匹配的项]],
    "新冠": [["新型冠状病毒", "流感病毒"], ["新型冠状病毒核酸"]],
    "传染病": [["输血全套检查"], []],
    "WBC": [["血常规分析"], ["白细胞"]],
    "HB": [["血常规分析"], ["红细胞"]],
    "HCT": [["血常规分析"], ["红细胞压积"]],
    "N": [["血常规分析"], ["中性粒细胞绝对值"]],
    "MONO": [["血常规分析"], ["单核细胞绝对值"]],
    "L": [["血常规分析"], ["淋巴细胞绝对值"]],
    "PLT": [["血常规分析"], ["血小板"]],
    "ALT": [["肝肾糖电解质", "肝肾电解质"], ["丙氨酸氨基转移酶"]],
    "AST": [["肝肾糖电解质", "肝肾电解质"], ["天冬氨酸氨基转移酶"]],
    "TB": [["肝肾糖电解质", "肝肾电解质"], ["总胆红素(TBIL)"]],
    "DB": [["肝肾糖电解质", "肝肾电解质"], ["直接胆红素(DBIL)"]],
    "UB": [["肝肾糖电解质", "肝肾电解质"], ["间接胆红素(IDBIL)"]],
    "ALB": [["肝肾糖电解质", "肝肾电解质"], ["白蛋白(ALB)"]],
    "G": [["肝肾糖电解质"], ["葡萄糖(GLU)", "葡萄糖"]],
    "BUN": [["肝肾糖电解质", "肝肾电解质"], ["尿素氮(BUN)"]],
    "Cr": [["肝肾糖电解质", "肝肾电解质"], ["肌酐(CREA)"]],
    "Cysc": [["肝肾糖电解质", "肝肾电解质"], ["胱抑素C(Cys-C)"]],
    "K": [["电解质"], ["钾(K+)", "钾离子"]],
    "Na": [["电解质"], ["钠(Na+)", "钠离子"]],
    "Cl": [["电解质"], ["氯(Cl-)", "钠离子"]],
    "Ca": [["电解质"], ["钙(Ca++)", "钙离子"]],
    "PT": [["凝血象+D"], ["凝血酶原时间"]],
    "INR": [["凝血象+D"], ["凝血酶原标准化比值"]],
    "PTTA": [["凝血象+D"], ["凝血酶原时间活动度"]],
    "APTT": [["凝血象+D"], ["活化部分凝血活酶时间"]],
    "TT": [["凝血象+D"], ["凝血酶时间"]],
    "FIB": [["凝血象+D"], ["纤维蛋白原降解产物"]],
    "pro-BNP": [["BNP"], ["氨基末端B型利钠肽前体", "脑肭肽前体(NT-ProBNP)"]],
    "BNP": [["BNP"], ["脑钠肽"]],
    "HSTNI": [["高敏肌钙蛋白I"], ["高敏肌钙蛋白I"]],
    "MYO": [["肌红蛋白"], ["心肌红蛋白"]],
    "PCT": [["降钙素原"], ["降钙素原"]],
    "CRP": [["CRP"], ["C反应蛋白(CRP)"]],
    "血沉": [["血沉"], ["血沉"]],
    "IL6": [["白介素6"], ["白介素6"]],
    "氧合指数": [["淋巴细胞亚群"], []]
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
        desc: bool = False) -> str:
    check_setting = col_pattern_map[prop]
    if from_day is not None:
        from_day = from_day.replace(hour=0, minute=0, second=0)
    if to_day is not None:
        to_day = to_day.replace(hour=23, minute=59, second=59)
    check_time_rule = f"and `采集时间` between '{from_day}' and '{to_day}'"
    # check_name_rule = " and (" + " or ".join(
    #     [f"`检验项目` like '%%{keyword}%%'" for keyword in check_setting[0]]) + ")"
    check_item_rule = " and (" + " or ".join(
        [f"`项目名称` = '{keyword}'" for keyword in check_setting[1]]) + ")"
    sql = f"""select * from check_record_table4
              where `住院号`='{id}' {check_item_rule} {check_time_rule} order by `采集时间`"""
    if desc:
        sql += " desc"
    df = pd.read_sql(sql, con=engine)
    if len(df) > 0:
        print(df.loc[0, '检验结果'])
        result = df.loc[0, '检验结果']
    else:
        print("na")
        result = na
    return result

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

for ip, prop in enumerate(time_props):
    print(f"正在处理属性{prop}({ip}/{len(time_props)})")
    for t, postfix in zip(timing, timing_postfix):
        col = prop + postfix
        pbar = tqdm(total=len(df1))
        for index, row in df1.iterrows():
            if pd.isna(df1.loc[index, col]):
                desc = False
                if t == "入院12":
                    from_day = df1.loc[index, "入院12"]
                    to_day = df1.loc[index, "入院12"] + pd.Timedelta(days=2)
                elif t == "入院34":
                    from_day = df1.loc[index, "入院12"] + pd.Timedelta(days=3)
                    to_day = df1.loc[index, "入院12"] + pd.Timedelta(days=4)
                elif t == "入院56":
                    from_day = df1.loc[index, "入院12"] + pd.Timedelta(days=5)
                    to_day = df1.loc[index, "入院12"] + pd.Timedelta(days=6)
                elif t == "入院78":
                    from_day = df1.loc[index, "入院12"] + pd.Timedelta(days=7)
                    to_day = df1.loc[index, "入院12"] + pd.Timedelta(days=8)
                else:  # 出院
                    print("未知时间段")
                    continue
                if pd.isna(row[t]):
                    df1.loc[index, t] = from_day
                df1.loc[index, col] = get_result(f"ZY01000{df1.loc[index, '住院号']}", prop, from_day=from_day, to_day=to_day, desc=desc)
            pbar.update()
        pbar.close()
df1.to_excel(output_file, index=False)
