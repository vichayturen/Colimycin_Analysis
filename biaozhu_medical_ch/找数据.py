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
import os

import gradio as gr
import pandas as pd
from sqlalchemy import create_engine
pd.set_option('display.width', 180)  # 150，设置打印宽度
pd.set_option('display.max_rows', None)
pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', 40)

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/medical?charset=utf8mb4")

# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"


with gr.Blocks(title="中南医院数据中心") as demo:
    pid = gr.Textbox(label="患者编号")
    check = gr.Textbox(label="检验项目名称")
    sub_check = gr.Textbox(label="检验子项中文名")
    with gr.Row():
        from_time = gr.DateTime(label="开始时间", visible=False)
        to_time = gr.DateTime(label="结束时间", visible=False)
    with gr.Row():
        clean_btn = gr.ClearButton([pid, check, sub_check, from_time, to_time], value="清空")
        btn = gr.Button("查询", variant="primary")
    output = gr.Dataframe()

    @btn.click(inputs=[pid, check, sub_check, from_time, to_time], outputs=[output])
    def search(pid, check, sub_check, from_time, to_time):
        conditions = []
        if pid != "":
            conditions.append(f"`患者编号`={pid}")
        if check != "":
            conditions.append(f"`检验项目名称` like '%%{check}%%'")
        if sub_check != "":
            conditions.append(f"`检验子项中文名` like '%%{sub_check}%%'")
        condition = "where " + " and ".join(conditions)
        sql = f"""select * from check_record
                  {condition}
                  order by `采集时间`"""
        if pid == "":
            sql += "limit 100"
        try:
            tmp_df = pd.read_sql(sql=sql, con=engine)
            return tmp_df
        except Exception as e:
            raise gr.Error(e)

demo.launch(server_name="0.0.0.0", auth=("hhkk", "lovelove"))
