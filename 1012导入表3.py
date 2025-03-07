import pymysql
import pandas as pd
from tqdm import tqdm


mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                       password="root", database="medical", charset="utf8mb4")

sql = "drop table if exists check_record_table3;"
mysql.query(sql)

sql = """create table if not exists check_record_table3 (
    `患者编号` char(20) not null,
    `住院号` char(20) not null,
    `记录时间` datetime not null,
    `项目` varchar(512) not null,
    `结果` varchar(512) not null
) character set utf8mb4"""
mysql.query(sql)

for s in range(1, 34):
    if s == 1:
        sheet_name = "Sheet1"
        df = pd.read_excel(r"V:\huihui\data\icu数据提取-李一鸣\表3.xlsx", sheet_name=sheet_name)
    else:
        sheet_name = f"Sheet1({s})"
        df = pd.read_excel(
            r"V:\huihui\data\icu数据提取-李一鸣\表3.xlsx",
            sheet_name=sheet_name,
            header=None,
            names=["患者编号", "住院号", "项目", "记录时间", "结果"]
        )
    print(f"读取{sheet_name}成功，正在导入...")
    pbar = tqdm(total=len(df))
    batch = []
    for i, row in df.iterrows():
        row_result = row["结果"]
        if isinstance(row_result, str):
            if "\\" in row_result:
                row_result = row_result.replace("\\", "\\\\")
            if "'" in row_result:
                row_result = row_result.replace("'", "\\'")
            row_result = row_result[:500]
        batch.append("('{}', '{}', '{}', '{}', '{}')".format(
            row["患者编号"], row["住院号"], row["记录时间"], row["项目"], row_result)
        )
        if len(batch) == 500:
            sql = """insert into check_record_table3 (
                        `患者编号`, `住院号`, `记录时间`, `项目`, `结果`
                    ) values """ + ",".join(batch)
            mysql.query(sql)
            mysql.commit()
            batch.clear()
        pbar.update()
    if len(batch) > 0:
        sql = """insert into check_record_table3 (
                    `患者编号`, `住院号`, `记录时间`, `项目`, `结果`
                ) values """ + ",".join(batch)
        mysql.query(sql)
        mysql.commit()
    pbar.close()

