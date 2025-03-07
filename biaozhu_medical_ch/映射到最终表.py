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
    "pro-BNP": [["BNP"], ["氨基末端B型利钠肽前体"]],
    "BNP": [["BNP"], ["脑钠肽"]],
    "HSTNI": [["高敏肌钙蛋白I"], ["高敏肌钙蛋白I"]],
    "MYO": [["高敏肌钙蛋白I"], ["肌红蛋白"]],
    "PCT": [["降钙素原"], ["降钙素原"]],
    "CRP": [["CRP"], ["C反应蛋白(CRP)"]],
    "血沉": [["血沉"], ["血沉"]],
    "IL6": [["白介素6"], ["白介素6"]],
    "氧合指数": [["淋巴细胞亚群"], []],
}

sheet = "检验1"


df = pd.read_excel(f"/media/vv/8ee675f7-ec97-4bf1-95d5-b326aece4f1e/code/biaozhu_medical_ch/data/可利霉素_除去时间标记_{sheet}_new.xlsx", sheet_name=sheet)

cache = {}
pbar = tqdm(total=len(df))
for i, row in df.iterrows():
    id = row["住院号"]
    cache[id] = {}
    now_time = None
    now_time_type = None
    now_time_setting = None
    time_cache = {}
    for col in df.columns:
        for pattern in time_pattern_map:
            if col.startswith(pattern):
                now_time_type = pattern
                now_time = row[col]
                cache[id][now_time_type] = {}
                break
        if now_time is not None:
            for pattern in col_pattern_map:
                if col.startswith(pattern):
                    cache[id][now_time_type][pattern] = row[col]
    pbar.update()
pbar.close()
# print(cache)
# exit(0)


final_df = pd.read_excel("/media/vv/8ee675f7-ec97-4bf1-95d5-b326aece4f1e/code/biaozhu_medical_ch/data/可利霉素_ch.xls", sheet_name=sheet)

def is_empty(ele):
    if pd.isna(ele):
        return True
    if isinstance(ele, str) and ele.strip() == "":
        return True
    return False

pbar = tqdm(total=final_df.shape[0])
for i, row in final_df.iterrows():
    id = row["住院号"]
    now_time = None
    now_time_type = None
    for col in final_df.columns:
        for pattern in time_pattern_map:
            if col.startswith(pattern):
                now_time_type = pattern
                now_time = row[col]
                break
        if now_time is not None:
            for pattern in col_pattern_map:
                if col.startswith(pattern):
                    if is_empty(final_df.loc[i, col]):
                        final_df.loc[i, col] = cache[id][now_time_type][pattern]
    pbar.update()
pbar.close()
final_df.to_excel(f"data/可利霉素_ch_{sheet}.xlsx", sheet_name=sheet, index=False, na_rep="NA")


