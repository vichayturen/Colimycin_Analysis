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

import pymysql
import pandas as pd
from tqdm import tqdm


df = pd.read_excel("ch/非隐私信息.普通检验报告.普通检验子项报告.药敏及结果.xlsx", sheet_name="非隐私信息.普通检验报告.普通检验子项报告.药敏及结果")
print("读取成功")


mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                       password="root", database="medical", charset="utf8mb4")

sql = "drop table if exists check_record;"
mysql.query(sql)

sql = """create table if not exists check_record (
    `患者编号` char(20) not null,
    `检验项目名称` varchar(200) not null,
    `采集时间` datetime not null,
    `检验子项中文名` varchar(200) not null,
    `检验子项结果` varchar(200) not null
) character set utf8mb4"""
mysql.query(sql)

pbar = tqdm(total=len(df))
for i, row in df.iterrows():
    sql = """insert into check_record (
        `患者编号`, `检验项目名称`, `采集时间`, `检验子项中文名`, `检验子项结果`
    ) values (
        '{}', '{}', '{}', '{}', '{}'
    )""".format(row["患者编号"], row["检验项目名称"], row["采集时间"], row["检验子项中文名"], row["检验子项结果"])
    mysql.query(sql)
    mysql.commit()
    pbar.update()
pbar.close()

