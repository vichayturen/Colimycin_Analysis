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



import pandas as pd
from sqlalchemy import create_engine


df = pd.read_excel("/media/root1/备份/data/ch/非隐私信息.普通检验报告.普通检验子项报告.药敏及结果.xlsx", sheet_name="非隐私信息.普通检验报告.普通检验子项报告.药敏及结果")

engine = create_engine("mysql+pymysql://root:root@localhost:3306/medical?charset=utf8mb4")
df.to_sql("check", engine, schema="medical", if_exists='replace', index=True, chunksize=None, dtype=None)
