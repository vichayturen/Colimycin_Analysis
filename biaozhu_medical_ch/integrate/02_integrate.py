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


once_props = ["新冠", "传染病"]
time_props = [
    "WBC", "HB", "PLT", "N", "L", "MONO", "HCT", "ALT", "AST", "TB", "UB", "DB", "ALB", "G", "BUN", "Cr",
    "K", "Na", "PT", "Cl", "Ca",
    "INR", "PTTA", "APTT", "TT", "FIB", "pro-BNP", "BNP", "HSTNI", "MYO", "PCT", "CRP", "血沉", "IL6",
    "氧合指数"]
timeing = ["before", "3", "5", "7", "stop", "discharge"]
prop_cols = deepcopy(once_props)
for prop in time_props:
    for t in timeing:
        prop_cols.append(prop + "_" + t)
time_format = "%Y/%m/%d"
na = "NA"

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
    check_name_rule = " and (" + " or ".join(
        [f"`检验项目名称` like '%%{keyword}%%'" for keyword in check_setting[0]]) + ")"
    check_item_rule = " and (" + " or ".join(
        [f"`检验子项中文名` = '{keyword}'" for keyword in check_setting[1]]) + ")"
    if prop == "新冠":
        sql = f"""select * from check_record
                    where `患者编号`={id} {check_name_rule} {check_item_rule} order by `采集时间`"""
        df = pd.read_sql(sql, con=engine)
        if len(df) > 0:
            result = df.loc[0, '检验子项结果']
        else:
            result = na
    elif prop == "传染病":
        sql = f"select * from check_record where `患者编号`={id} {check_name_rule} order by `采集时间`"
        df = pd.read_sql(sql, con=engine)
        if len(df) > 0:
            result = json.dumps({df.loc[i, "检验子项中文名"]: df.loc[i, "检验子项结果"]
                             for i in range(len(df))}, ensure_ascii=False, indent=4) if len(df) > 0 else None
        else:
            result = na
    elif prop == "氧合指数":
        sql = f"""select * from check_record
                    where `患者编号`={id} {check_name_rule} {check_time_rule} order by `采集时间`"""
        df = pd.read_sql(sql, con=engine)
        if len(df) > 0:
            result = json.dumps({df.loc[i, "检验子项中文名"]: df.loc[i, "检验子项结果"]
                             for i in range(len(df))}, ensure_ascii=False, indent=4) if len(df) > 0 else None
        else:
            result = na
    else:
        sql = f"""select * from check_record
                  where `患者编号`={id} {check_name_rule} {check_item_rule} {check_time_rule} order by `采集时间`"""
        if desc:
            sql += " desc"
        df = pd.read_sql(sql, con=engine)
        if len(df) > 0:
            result = df.loc[0, '检验子项结果']
        else:
            result = na
    return result


def get_col_between_two_cols(col_pattern, col1, col2, col_list) -> str | None:
    i = 0
    while i < len(col_list) and col_list[i] != col1:
        i += 1
    while i < len(col_list) and col_list[i] != col2:
        if col_list[i].startswith(col_pattern):
            return col_list[i]
        i += 1
    return None


df_ch1 = pd.read_excel('../data/可利霉素_ch.xls', sheet_name="检验1", index_col="编号")
df_ch2 = pd.read_excel('../data/可利霉素_ch.xls', sheet_name="检验2", index_col="编号")
df_wkyc = pd.read_excel('../data/可利霉素_wkyc_wide_01_initial.xlsx', sheet_name="Sheet1")
df_wkyc = df_wkyc.reindex(columns=df_wkyc.columns.tolist() + prop_cols, fill_value="")
def filter_func(x) -> bool:
    return not pd.isna(x["可利霉素开始时间"])
df_wkyc = df_wkyc[df_wkyc.apply(filter_func, axis=1)]

print("正在处理时间无关列...")
pbar = tqdm(total=len(df_wkyc))
for index, row in df_wkyc.iterrows():
    id = row["编号"]
    for prop in once_props:
        if not pd.isna(df_ch1.loc[id, prop]):
            result = df_ch1.loc[id, prop]
        else:
            result = get_result(id, prop)
        df_wkyc.loc[index, prop] = result if result is not None else na
    pbar.update()
pbar.close()

print("正在处理时间有关的列...")

d = {
    "before": ["可利霉素前24小时", "可D1"],
    "3": ["可后D3-D4", "可后D5-D6"],
    "5": ["可后D5-D6", "可后D7-D8"],
    "7": ["可后D7-D8", "结束可利霉素时间.1"],
    "stop": ["结束可利霉素时间.1", "出院时间.1"],
    "discharge": ["出院时间.1", ""]
}
for ip, prop in enumerate(time_props):
    print(f"正在处理属性{prop}({ip}/{len(time_props)})")
    for t in timeing:
        if t == "before":
            df_ch = df_ch1
            col_ch = get_col_between_two_cols(prop, d[t][0], d[t][1], df_ch.columns.tolist())
        else:
            df_ch = df_ch2
            col_ch = get_col_between_two_cols(prop, d[t][0], d[t][1], df_ch.columns.tolist())
        if col_ch is None:
            for index, row in df_wkyc.iterrows():
                df_wkyc.loc[index, prop + "_" + t] = na
            break
        pbar = tqdm(total=len(df_wkyc))
        for index, row in df_wkyc.iterrows():
            if not pd.isna(df_ch.loc[row["编号"], col_ch]):
                df_wkyc.loc[index, prop + "_" + t] = df_ch.loc[row["编号"], col_ch]
            else:
                if t == "before":
                    from_day = datetime.strptime(df_wkyc.loc[index, "入院时间"], time_format)
                    to_day = datetime.strptime(df_wkyc.loc[index, "可利霉素开始时间"], time_format) + pd.Timedelta(days=-1)
                    desc = True
                elif t == "3":
                    from_day = datetime.strptime(df_wkyc.loc[index, "可利霉素后3天"], time_format)
                    to_day = datetime.strptime(df_wkyc.loc[index, "可利霉素后3天"], time_format) + pd.Timedelta(days=1)
                    desc = False
                elif t == "5":
                    from_day = datetime.strptime(df_wkyc.loc[index, "可利霉素后5天"], time_format)
                    to_day = datetime.strptime(df_wkyc.loc[index, "可利霉素后5天"], time_format) + pd.Timedelta(days=1)
                    desc = False
                elif t == "7":
                    from_day = datetime.strptime(df_wkyc.loc[index, "可利霉素后7天"], time_format)
                    to_day = datetime.strptime(df_wkyc.loc[index, "可利霉素后7天"], time_format) + pd.Timedelta(days=1)
                    desc = False
                elif t == "stop":
                    from_day = datetime.strptime(df_wkyc.loc[index, "结束可利霉素时间"], time_format)
                    to_day = datetime.strptime(df_wkyc.loc[index, "出院时间"], time_format)
                    desc = False
                else:  # 出院
                    from_day = datetime.strptime(df_wkyc.loc[index, "结束可利霉素时间"], time_format)
                    to_day = datetime.strptime(df_wkyc.loc[index, "出院时间"], time_format)
                    desc = True
                df_wkyc.loc[index, prop + "_" + t] = get_result(df_wkyc.loc[index, "患者编号"], prop,
                                                                from_day=from_day,
                                                                to_day=to_day)
            pbar.update()
        pbar.close()
df_wkyc.to_excel("../data/可利霉素_wkyc_wide_02_fillvalue.xlsx", index=False)
