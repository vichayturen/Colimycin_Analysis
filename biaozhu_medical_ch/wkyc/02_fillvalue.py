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


from datetime import datetime

import pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/medical?charset=utf8mb4")

other_sub_item = ["WBC", "HB", "HCT", "N", "L", "PLT", "PCT", "CRP", "IL6"]


col_pattern_map = {
    # # "要填入的列名称的头": [[检查可以包含的关键词], [检查子表内匹配的项]],
    # "新冠": [["新型冠状病毒", "流感病毒"], ["新型冠状病毒核酸"]],
    # "传染病": [["输血全套检查"], []],
    "WBC": [["血常规分析"], ["白细胞"]],
    "HB": [["血常规分析"], ["红细胞"]],
    "HCT": [["血常规分析"], ["红细胞压积"]],
    "N": [["血常规分析"], ["中性粒细胞绝对值"]],
    # "MONO": [["血常规分析"], ["单核细胞绝对值"]],
    "L": [["血常规分析"], ["淋巴细胞绝对值"]],
    "PLT": [["血常规分析"], ["血小板"]],
    # "ALT": [["肝肾糖电解质", "肝肾电解质"], ["丙氨酸氨基转移酶"]],
    # "AST": [["肝肾糖电解质", "肝肾电解质"], ["天冬氨酸氨基转移酶"]],
    # "TB": [["肝肾糖电解质", "肝肾电解质"], ["总胆红素(TBIL)"]],
    # "DB": [["肝肾糖电解质", "肝肾电解质"], ["直接胆红素(DBIL)"]],
    # "UB": [["肝肾糖电解质", "肝肾电解质"], ["间接胆红素(IDBIL)"]],
    # "ALB": [["肝肾糖电解质", "肝肾电解质"], ["白蛋白(ALB)"]],
    # "G": [["肝肾糖电解质"], ["葡萄糖(GLU)", "葡萄糖"]],
    # "BUN": [["肝肾糖电解质", "肝肾电解质"], ["尿素氮(BUN)"]],
    # "Cr": [["肝肾糖电解质", "肝肾电解质"], ["肌酐(CREA)"]],
    # "Cysc": [["肝肾糖电解质", "肝肾电解质"], ["胱抑素C(Cys-C)"]],
    # "K": [["电解质"], ["钾(K+)", "钾离子"]],
    # "Na": [["电解质"], ["钠(Na+)", "钠离子"]],
    # "Cl": [["电解质"], ["氯(Cl-)", "钠离子"]],
    # "Ca": [["电解质"], ["钙(Ca++)", "钙离子"]],
    # "PT": [["凝血象+D"], ["凝血酶原时间"]],
    # "INR": [["凝血象+D"], ["凝血酶原标准化比值"]],
    # "PTTA": [["凝血象+D"], ["凝血酶原时间活动度"]],
    # "APTT": [["凝血象+D"], ["活化部分凝血活酶时间"]],
    # "TT": [["凝血象+D"], ["凝血酶时间"]],
    # "FIB": [["凝血象+D"], ["纤维蛋白原降解产物"]],
    # "pro-BNP": [["BNP"], ["氨基末端B型利钠肽前体"]],
    # "BNP": [["BNP"], ["脑钠肽"]],
    # "HSTNI": [["高敏肌钙蛋白I"], ["高敏肌钙蛋白I"]],
    # # "MYO": [["高敏肌钙蛋白I"], ["肌红蛋白"]],
    "PCT": [["降钙素原"], ["降钙素原"]],
    "CRP": [["CRP"], ["C反应蛋白(CRP)"]],
    # "血沉": [["血沉"], ["血沉"]],
    "IL6": [["白介素6"], ["白介素6"]],
    # "氧合指数": [["淋巴细胞亚群"], []],
}


check_time_rule = "and `采集时间` between '2020-03-01' and '2020-03-31'"


def main():
    df = pd.read_excel('../data/可利霉素_wkyc_01_initial.xlsx')
    pbar = tqdm(total=df.shape[0])
    for index, row in df.iterrows():
        if pd.isna(row['可利霉素开始时间']): continue
        time_type = row['时间标签']
        ruyuan_time = datetime.strptime(row['入院时间'], "%Y/%m/%d")
        chuyuan_time = datetime.strptime(row['出院时间'], "%Y/%m/%d")
        keli_time = datetime.strptime(row['可利霉素开始时间'], "%Y/%m/%d")
        keli_jieshu_time = datetime.strptime(row['结束可利霉素时间'], "%Y/%m/%d")
        if time_type == '可利霉素前':
            from_time = ruyuan_time
            to_time = keli_time + pd.Timedelta(days=-1)
            to_time.replace(hour=23, minute=59, second=59)
            desc = True
        elif time_type == '可利霉素后第3天':
            from_time = keli_time + pd.Timedelta(days=3)
            to_time = keli_time + pd.Timedelta(days=4)
            to_time.replace(hour=23, minute=59, second=59)
            desc = False
        elif time_type == '可利霉素后第5天':
            from_time = keli_time + pd.Timedelta(days=5)
            to_time = keli_time + pd.Timedelta(days=6)
            to_time.replace(hour=23, minute=59, second=59)
            desc = False
        elif time_type == '可利霉素后第7天':
            from_time = keli_time + pd.Timedelta(days=7)
            to_time = keli_time + pd.Timedelta(days=8)
            to_time.replace(hour=23, minute=59, second=59)
            desc = False
        elif time_type == '结束可利霉素':
            from_time = keli_jieshu_time
            to_time = chuyuan_time
            to_time.replace(hour=23, minute=59, second=59)
            desc = False
        else:  # 出院
            from_time = keli_jieshu_time
            to_time = chuyuan_time
            to_time.replace(hour=23, minute=59, second=59)
            desc = True
        check_time_rule = f"and `采集时间` between '{from_time}' and '{to_time}'"
        for col in other_sub_item:
            check_setting = col_pattern_map[col]
            check_name_rule = " and (" + " or ".join(
                [f"`检验项目名称` like '%%{keyword}%%'" for keyword in check_setting[0]]) + ")"
            check_item_rule = " and (" + " or ".join(
                [f"`检验子项中文名` = '{keyword}'" for keyword in check_setting[1]]) + ")"
            sql = f"""select * from check_record
                   where `患者编号`={row['患者编号']} {check_name_rule} {check_item_rule} {check_time_rule} order by `采集时间`"""
            if desc:
                sql += " desc"
            tmp_df = pd.read_sql(sql, con=engine)
            if tmp_df.empty:
                df.loc[index, col] = "NA"
            else:
                df.loc[index, col] = tmp_df.loc[0, '检验子项结果']
        pbar.update()
    pbar.close()
    df.to_excel('../data/可利霉素_wkyc_02_fillvalue.xlsx', index=False)


if __name__ == '__main__':
    main()
