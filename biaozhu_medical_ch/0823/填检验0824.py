from config import pd
import json
from datetime import datetime
from copy import deepcopy
from typing import Optional

from tqdm import tqdm
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/medical?charset=utf8mb4")

df1 = pd.read_excel('/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/可利霉素(1).xls',
                    sheet_name='检验1')

print(df1.columns.tolist())
# exit(0)

# props = ["WBC", "N", "L", "MONO", "HB", "PLT", "HCT", "ALT", "AST", "TB", "ALB", "BUN", "Cr", "K", "Na", "PCT", "CRP", "血沉", "IL6"]
# props = ["WBC", "N", "L", "MONO", "HB", "PLT", "HCT", "ALT", "AST", "TB", "DB", "ALB", "G", "BUN", "Cr", "PCT", "CRP", "血沉", "IL6"]
# props = ["HB", "UREA"]
props = ["HB", "ALT", "AST", "TB", "DB", "ALB", "G", "BUN", "Cr", "UREA"]

# timeing = ["基线时间", "可利霉素前24小时", "可D1", "可后D3-D4", "可后D5-D6", "可后D7-D8"]
timeing = ["入院时间.1", "入ICU时间", "可利霉素前24小时", "可D1-2", "可后D3-D4", "可后D5-D6", "可后D7-D8", "出院时间.1"]

time_format = "%Y/%m/%d"
na = "NA"

col_pattern_map = {
    # # "要填入的列名称的头": [[检查可以包含的关键词], [检查子表内匹配的项]],
    "UREA": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["尿素(UREA)"]],
    "新冠": [["新型冠状病毒", "流感病毒"], ["新型冠状病毒核酸"]],
    "传染病": [["输血全套检查"], []],
    "WBC": [["血常规分析"], ["白细胞"]],
    "HB": [["血常规分析"], ["血红蛋白"]],
    "HCT": [["血常规分析"], ["红细胞压积"]],
    "N": [["血常规分析"], ["中性粒细胞绝对值"]],
    "MONO": [["血常规分析"], ["单核细胞绝对值"]],
    "L": [["血常规分析"], ["淋巴细胞绝对值"]],
    "PLT": [["血常规分析"], ["血小板"]],
    "ALT": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["丙氨酸氨基转移酶"]],
    "AST": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["天冬氨酸氨基转移酶"]],
    "TB": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["总胆红素(TBIL)"]],
    "DB": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["直接胆红素(DBIL)"]],
    "UB": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["间接胆红素(IDBIL)"]],
    "ALB": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["白蛋白(ALB)"]],
    "G": [["肝肾糖电解质", "肾功能", "肝功能"], ["葡萄糖(GLU)", "葡萄糖"]],
    "BUN": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["尿素氮(BUN)"]],
    "Cr": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["肌酐(CREA)"]],
    "Cysc": [["肝肾糖电解质", "肝肾电解质", "肾功能", "肝功能"], ["胱抑素C(Cys-C)"]],
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

def get_time(dt):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y/%m/%d")
    elif isinstance(dt, pd.Timestamp):
        dt = dt.to_pydatetime()
    return dt



print("正在处理时间有关的列...")

pbar = tqdm(total=df1.shape[0])
for row_index, row in df1.iterrows():
    id = row['患者编号']
    keshijian = row['可利霉素时间']
    ruyuan = get_time(row['入院时间.1'])
    ruicu = get_time(row['入ICU时间'])
    keqian = get_time(row['可利霉素前24小时'])
    ked1 = get_time(row['可D1-2']) + pd.Timedelta(days=1)
    ked3 = get_time(row['可后D3-D4'])
    ked5 = get_time(row['可后D5-D6'])
    ked7 = get_time(row['可后D7-D8'])
    chuyuan = get_time(row['出院时间.1'])
    for prop in props:
        # 入院
        df1.loc[row_index, prop] = get_result(id, prop, ruyuan, keqian)
        # 入ICU
        df1.loc[row_index, prop+'.1'] = get_result(id, prop, ruicu, keqian)
        # 可前
        df1.loc[row_index, prop+'.2'] = get_result(id, prop, keqian+pd.Timedelta(days=-6), keqian, True)
        # 可1
        df1.loc[row_index, prop+'.3'] = get_result(id, prop, ked1, ked1+pd.Timedelta(days=1))
        # 可3
        df1.loc[row_index, prop+'.4'] = get_result(id, prop, ked3, ked3+pd.Timedelta(days=1))
        # 可5
        df1.loc[row_index, prop+'.5'] = get_result(id, prop, ked5, ked5+pd.Timedelta(days=1))
        # 可7
        df1.loc[row_index, prop+'.6'] = get_result(id, prop, ked7, ked7+pd.Timedelta(days=1))
        # 出院
        df1.loc[row_index, prop+'.7'] = get_result(id, prop, chuyuan+pd.Timedelta(days=-5), chuyuan, True)
    pbar.update()
pbar.close()

df1.to_excel("/home/vv/文档/xwechat_files/wxid_vlh3ec6ed7tx22_8772/msg/file/2024-08/baseline可利霉素_检验1_0825_补充.xlsx", index=False)
