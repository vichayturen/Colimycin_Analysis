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


def main():
    time_type = [
        "可利霉素前", "可利霉素后第3天", "可利霉素后第5天", "可利霉素后第7天", "结束可利霉素", "出院"
    ]
    # initial_columns = [
    #     "编号", "住院号", "入院时间", "备注", "出院时间", "死亡时间", "结束可利霉素时间", "姓名", "时间标签"
    # ]
    from_df = pd.read_excel('../data/可利霉素_ch.xls', sheet_name="检验1")
    from_df2 = pd.read_excel('../data/可利霉素_ch.xls', sheet_name="检验2")
    to_df = pd.read_excel('../data/可利霉素_wkyc.xlsx', sheet_name="Sheet1")
    new_row_index = 0
    for index, row in from_df.iterrows():
        keli_time = from_df2.loc[index, "可利霉素开始时间"]
        for t in time_type:
            if t == "可利霉素前":
                time_value = keli_time + pd.Timedelta(days=-1)
            elif t == "可利霉素后第3天":
                time_value = keli_time + pd.Timedelta(days=3)
            elif t == "可利霉素后第5天":
                time_value = keli_time + pd.Timedelta(days=5)
            elif t == "可利霉素后第7天":
                time_value = keli_time + pd.Timedelta(days=7)
            elif t == "结束可利霉素":
                time_value = from_df2.loc[index, "结束可利霉素时间"]
            else:
                time_value = row["出院时间"]
            try:
                to_df.loc[new_row_index, "编号"] = row["编号"]
                to_df.loc[new_row_index, "住院号"] = row["住院号"]
                to_df.loc[new_row_index, "患者编号"] = from_df2.loc[index, "患者编号"]
                to_df.loc[new_row_index, "备注"] = row["备注"]
                to_df.loc[new_row_index, "入院时间"] = row["入院时间"].strftime("%Y/%m/%d")
                to_df.loc[new_row_index, "出院时间"] = row["出院时间"].strftime("%Y/%m/%d")
                to_df.loc[new_row_index, "死亡时间"] = row["死亡时间"].strftime("%Y/%m/%d") if not pd.isna(row["死亡时间"]) else "NA"
                to_df.loc[new_row_index, "可利霉素开始时间"] = from_df2.loc[index, "可利霉素开始时间"].strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "可利霉素开始时间"]) else "NA"
                to_df.loc[new_row_index, "结束可利霉素时间"] = from_df2.loc[index, "结束可利霉素时间"].strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "结束可利霉素时间"]) else "NA"
                to_df.loc[new_row_index, "姓名"] = row["姓名"]
                to_df.loc[new_row_index, "时间标签"] = t
                to_df.loc[new_row_index, "时间值"] = time_value.strftime("%Y/%m/%d") if not pd.isna(time_value) else "NA"
                new_row_index += 1
            except Exception as e:
                print(index)
                raise e
    to_df.to_excel('../data/可利霉素_wkyc_01_initial.xlsx', index=False)


if __name__ == '__main__':
    main()
