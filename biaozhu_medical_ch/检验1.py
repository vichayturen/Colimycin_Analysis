# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import re
import json
from datetime import datetime

import pymysql
from sqlalchemy import create_engine
from tqdm import tqdm
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
pd.set_option('display.width', 180)  # 150，设置打印宽度
pd.set_option("display.max_columns", 10)
pd.set_option('display.max_colwidth', 40)

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/medical?charset=utf8mb4")



df = pd.read_excel("可利霉素.xls", sheet_name="检验1")
# mysql = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="medical", charset="utf8mb4")

time_patterm_sequence = [
    "入院时间",
    "入ICU时间",
    "可利霉素前24小时",
    "可后D2",
    "可后D3-D4",
    "可后D5-D6",
    "可后D7-D8",
    "结束可利霉素时间",
    "出院时间"
]
time_pattern_map = {
    # "代表时间的列名称": [允许向前延伸的天数, 允许向后延伸的天数, 尽量前 0/尽量后 1],
    "入院时间": [0, None, 0],
    "入ICU时间": [0, None, 0],
    "可利霉素前24小时": [-2, -1, 1],
    "可后D2": [-1, 0, 0],
    "可后D3-D4": [0, 1, 0],
    "可后D5-D6": [0, 1, 0],
    "可后D7-D8": [0, 1, 0],
    "结束可利霉素时间": [0, None, 0],
    "出院时间": [None, 0, 1]
}
col_pattern_map = {
    # "要填入的列名称的头": [[检查可以包含的关键词], [检查子表内匹配的项]],
    "新冠": [["新型冠状病毒"], ["新型冠状病毒核酸"]],
    "传染病": [["输血全套检查"], []],
    "WBC": [["血常规分析"], ["白细胞"]],
    "HB": [["血常规分析"], ["红细胞"]],
    "HCT": [["血常规分析"], ["红细胞压积"]],
    "N": [["血常规分析"], ["中性粒细胞绝对值"]],
    "MONO": [["血常规分析"], ["单核细胞绝对值"]],
    "L": [["血常规分析"], ["淋巴细胞绝对值"]],
    "PLT": [["血常规分析"], ["血小板"]],
    "ALT": [["肝肾糖电解质", "肝肾电解质"], ["AST/ALT", "AST/ALT比值"]],
    "AST": [["肝肾糖电解质", "肝肾电解质"], ["AST/ALT", "AST/ALT比值"]],
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
    "pro-BNP": [["BNP"], ["氨基末端B型利钠肽前体"]],
    "BNP": [["BNP"], ["脑钠肽"]],
    "HSTNI": [["高敏肌钙蛋白I"], ["高敏肌钙蛋白I"]],
    # "MYO": [["高敏肌钙蛋白I"], ["肌红蛋白"]],
    "PCT": [["降钙素原"], ["降钙素原"]],
    "CRP": [["CRP"], ["C反应蛋白(CRP)"]],
    "血沉": [["血沉"], ["血沉"]],
    "IL6": [["白介素6"], ["白介素6"]],
    "氧合指数": [["淋巴细胞亚群"], []],
}

pbar = tqdm(total=len(df))
for i, row in df.iterrows():
    now_time = None
    now_time_type = None
    now_time_setting = None
    time_cache = {}
    for col in df.columns:
        for pattern in time_pattern_map:
            if col.startswith(pattern):
                now_time = row[col]
                if isinstance(now_time, Timestamp):
                    now_time = now_time.to_pydatetime()
                if isinstance(now_time, datetime):
                    time_cache[pattern] = now_time
    for col in df.columns:
        for pattern in time_pattern_map:
            if col.startswith(pattern):
                now_time = row[col]
                now_time_type = pattern
                now_time_setting = time_pattern_map[pattern]
                if pd.isna(now_time):
                    now_time = None
                    # print("空值")
                elif isinstance(now_time, Timestamp):
                    # print("timestamp正常")
                    now_time = now_time.to_pydatetime()
                elif isinstance(now_time, datetime):
                    pass
                    # print("timestamp正常")
                elif isinstance(now_time, str):
                    now_time = None
                    # print("str格式")
                else:
                    now_time = None
                    # print("其他格式")
                    # print(type(now_time))
                break
        if now_time is not None:
            for pattern in col_pattern_map:
                if col.startswith(pattern):
                    check_name_keyword = col_pattern_map[pattern][0]
                    check_item_keyword = col_pattern_map[pattern][1]
                    if now_time_setting[0] is None:
                        from_time = None
                        time_id = time_patterm_sequence.index(now_time_type)
                        for idx in range(time_id-1, -1, -1):
                            if time_cache.get(time_patterm_sequence[idx]) is not None:
                                from_time = time_cache.get(time_patterm_sequence[idx])
                                from_time = from_time.replace(hour=0, minute=0, second=0)
                                break
                    else:
                        from_time = now_time + pd.Timedelta(days=now_time_setting[0])
                        from_time = from_time.replace(hour=0, minute=0, second=0)
                    if now_time_setting[1] is None:
                        to_time = None
                        time_id = time_patterm_sequence.index(now_time_type)
                        for idx in range(time_id + 1, len(time_patterm_sequence)):
                            if time_cache.get(time_patterm_sequence[idx]) is not None:
                                to_time = time_cache.get(time_patterm_sequence[idx])
                                to_time = to_time.replace(hour=23, minute=59, second=59)
                                break
                    else:
                        to_time = now_time + pd.Timedelta(days=now_time_setting[1])
                        to_time = to_time.replace(hour=23, minute=59, second=59)
                    if from_time is not None and to_time is not None:
                        check_time_rule = f"and `采集时间` between '{from_time}' and '{to_time}'"
                    elif from_time is not None:
                        check_time_rule = f"and `采集时间` > '{from_time}'"
                    elif to_time is not None:
                        check_time_rule = f"and `采集时间` < '{to_time}'"
                    else:
                        check_time_rule = ""
                    check_name_rule = " and (" + " or ".join([f"`检验项目名称` like '%%{keyword}%%'" for keyword in check_name_keyword]) + ")"
                    check_item_rule = " and (" + " or ".join([f"`检验子项中文名` = '{keyword}'" for keyword in check_item_keyword]) + ")"
                    # if now_time_type == "入院时间":
                    #     print("parse")
                    if pattern == "新冠":
                        sql = f"""select * from check_record
                        where `患者编号`={row['患者编号']}
                        {check_name_rule}
                        {check_item_rule}
                        order by `采集时间`"""
                        tmp_df = pd.read_sql(sql=sql, con=engine)
                        tmp_result = f"{tmp_df.loc[0, "检验子项结果"]}({tmp_df.loc[0, "采集时间"]})" if len(tmp_df) > 0 else None
                    elif pattern == "传染病":
                        sql = f"""select * from check_record
                        where `患者编号`={row['患者编号']}
                        {check_name_rule}
                        order by `采集时间`"""
                        tmp_df = pd.read_sql(sql=sql, con=engine)
                        tmp_result = json.dumps({tmp_df.loc[i, "检验子项中文名"]: tmp_df.loc[i, "检验子项结果"]
                                                 for i in range(len(tmp_df))}, ensure_ascii=False, indent=4) if len(tmp_df) > 0 else None
                    elif pattern == "氧合指数":
                        sql = f"""select * from check_record
                        where `患者编号`={row['患者编号']}
                        {check_name_rule}
                        order by `采集时间`"""
                        tmp_df = pd.read_sql(sql=sql, con=engine)
                        tmp_result = json.dumps({tmp_df.loc[i, "检验子项中文名"]: tmp_df.loc[i, "检验子项结果"]
                                                 for i in range(len(tmp_df))}, ensure_ascii=False, indent=4) if len(tmp_df) > 0 else None
                    else:
                        sql = f"""select * from check_record
                        where `患者编号`={row['患者编号']}
                        {check_name_rule}
                        {check_item_rule}
                        {check_time_rule}
                        order by `采集时间`"""
                        if now_time_setting[2] == 1:
                            sql += " desc"
                        tmp_df = pd.read_sql(sql=sql, con=engine)
                        tmp_result = f"{tmp_df.loc[0, "检验子项结果"]}({tmp_df.loc[0, "采集时间"]})" if len(tmp_df) > 0 else None
                    tmp_df = pd.read_sql(sql=sql, con=engine)
                    # print(tmp_df.head())
                    # exit()
                    if tmp_result is not None:
                        df.loc[i, col] = tmp_result
                    else:
                        df.loc[i, col] = "NA"
                    break
    pbar.update()
    # if i == 5:
    #     break
pbar.close()
df.to_excel("可利霉素_检验1_all.xlsx", sheet_name="检验1", index=False)
