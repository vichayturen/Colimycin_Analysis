import pymysql
import pandas as pd
from tqdm import tqdm





mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                       password="root", database="medical", charset="utf8mb4")

sql = "drop table if exists check_record_table4;"
mysql.query(sql)

sql = """create table if not exists check_record_table4 (
    `患者编号` char(20) not null,
    `住院号` char(20) not null,
    `采集时间` datetime not null,
    `检验项目` varchar(512) not null,
    `项目名称` varchar(512) not null,
    `检验结果` varchar(256) not null
) character set utf8mb4"""
mysql.query(sql)


for s in range(1, 4):
    if s == 1:
        df = pd.read_excel(r"V:\huihui\data\icu数据提取-李一鸣\表4.xlsx", sheet_name="Sheet1")
    else:
        sheet_name = f"Sheet1({s})"
        df = pd.read_excel(
            r"V:\huihui\data\icu数据提取-李一鸣\表4.xlsx",
            sheet_name=sheet_name,
            header=None,
            names=["患者编号", "住院号", "采集时间", "检验项目", "项目名称", "检验结果"]
        )
    print(f"读取{sheet_name}成功，正在导入...")

    pbar = tqdm(total=len(df))
    batch = []
    for i, row in df.iterrows():
        batch.append("('{}', '{}', '{}', '{}', '{}', '{}')".format(
            row["患者编号"], row["住院号"], row["采集时间"], row["检验项目"], row["项目名称"], row["检验结果"])
        )
        if len(batch) == 100:
            batch_data = ",".join(batch)
            sql = """insert into check_record_table4 (
                `患者编号`, `住院号`, `采集时间`, `检验项目`, `项目名称`, `检验结果`
            ) values {};""".format(batch_data)
            mysql.query(sql)
            mysql.commit()
            batch.clear()
        pbar.update()
    if len(batch) > 0:
        batch_data = ",".join(batch)
        sql = """insert into check_record_table4 (
            `患者编号`, `住院号`, `采集时间`, `检验项目`, `项目名称`, `检验结果`
        ) values {};""".format(batch_data)
        mysql.query(sql)
        mysql.commit()
    pbar.close()

