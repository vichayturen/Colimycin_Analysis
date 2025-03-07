# -*- coding: UTF-8 -*-

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
    with gr.Tab("大表"):
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
        def search1(pid, check, sub_check, from_time, to_time):
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
            sql += "limit 100"
            try:
                tmp_df = pd.read_sql(sql=sql, con=engine)
                return tmp_df
            except Exception as e:
                raise gr.Error(e)
    with gr.Tab("表3"):
        pid = gr.Textbox(label="患者编号")
        zid = gr.Textbox(label="住院号")
        check = gr.Textbox(label="项目")
        with gr.Row():
            from_time = gr.DateTime(label="开始时间", visible=False)
            to_time = gr.DateTime(label="结束时间", visible=False)
        with gr.Row():
            clean_btn = gr.ClearButton([pid, zid, check, from_time, to_time], value="清空")
            btn = gr.Button("查询", variant="primary")
        output = gr.Dataframe()


        @btn.click(inputs=[pid, zid, check, from_time, to_time], outputs=[output])
        def search2(pid, zid, check, from_time, to_time):
            conditions = []
            if pid != "":
                conditions.append(f"`患者编号`={pid}")
            if check != "":
                conditions.append(f"`住院号`='{zid}'")
            if sub_check != "":
                conditions.append(f"`项目` like '%%{check}%%'")
            condition = "where " + " and ".join(conditions)
            sql = f"""select * from check_record_table3
                      {condition}
                      order by `记录时间`"""
            sql += "limit 1000"
            try:
                tmp_df = pd.read_sql(sql=sql, con=engine)
                return tmp_df
            except Exception as e:
                raise gr.Error(e)
    with gr.Tab("表4"):
        pid = gr.Textbox(label="患者编号")
        zid = gr.Textbox(label="住院号")
        check = gr.Textbox(label="检验项目")
        item = gr.Textbox(label="项目名称")
        with gr.Row():
            from_time = gr.DateTime(label="开始时间", visible=False)
            to_time = gr.DateTime(label="结束时间", visible=False)
        with gr.Row():
            clean_btn = gr.ClearButton([pid, zid, check, from_time, to_time], value="清空")
            btn = gr.Button("查询", variant="primary")
        output = gr.Dataframe()


        @btn.click(inputs=[pid, zid, check, item, from_time, to_time], outputs=[output])
        def search3(pid, zid, check, item, from_time, to_time):
            conditions = []
            if pid != "":
                conditions.append(f"`患者编号`={pid}")
            if check != "":
                conditions.append(f"`住院号`='{zid}'")
            if sub_check != "":
                conditions.append(f"`检验项目` like '%%{check}%%'")
            if sub_check != "":
                conditions.append(f"`项目名称` like '%%{item}%%'")
            condition = "where " + " and ".join(conditions)
            sql = f"""select * from check_record_table4
                      {condition}
                      order by `采集时间`"""
            sql += "limit 1000"
            try:
                tmp_df = pd.read_sql(sql=sql, con=engine)
                return tmp_df
            except Exception as e:
                raise gr.Error(e)

demo.launch(server_name="127.0.0.1")
