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
    from_df = pd.read_excel('../data/可利霉素_ch.xls', sheet_name="检验1")
    from_df2 = pd.read_excel('../data/可利霉素_ch.xls', sheet_name="检验2")
    to_df = pd.read_excel('../data/可利霉素_wkyc_wide.xlsx', sheet_name="Sheet1")
    new_row_index = 0
    for index, row in from_df.iterrows():
        time_value1 = from_df2.loc[index, "可利霉素开始时间"]
        time_value0 = time_value1 + pd.Timedelta(days=-1)
        time_value3 = time_value1 + pd.Timedelta(days=3)
        time_value5 = time_value1 + pd.Timedelta(days=5)
        time_value7 = time_value1 + pd.Timedelta(days=7)
        time_value9 = from_df2.loc[index, "结束可利霉素时间"]
        try:
            to_df.loc[new_row_index, "编号"] = row["编号"]
            to_df.loc[new_row_index, "住院号"] = row["住院号"]
            to_df.loc[new_row_index, "患者编号"] = from_df2.loc[index, "患者编号"]
            to_df.loc[new_row_index, "姓名"] = row["姓名"]
            to_df.loc[new_row_index, "备注"] = row["备注"]
            to_df.loc[new_row_index, "入院时间"] = row["入院时间"].strftime("%Y/%m/%d")
            to_df.loc[new_row_index, "出院时间"] = row["出院时间"].strftime("%Y/%m/%d")
            to_df.loc[new_row_index, "死亡时间"] = row["死亡时间"].strftime("%Y/%m/%d") if not pd.isna(row["死亡时间"]) else "NA"
            to_df.loc[new_row_index, "可利霉素前"] = time_value0.strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "可利霉素开始时间"]) else "NA"
            to_df.loc[new_row_index, "可利霉素开始时间"] = time_value1.strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "可利霉素开始时间"]) else "NA"
            to_df.loc[new_row_index, "可利霉素后3天"] = time_value3.strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "可利霉素开始时间"]) else "NA"
            to_df.loc[new_row_index, "可利霉素后5天"] = time_value5.strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "可利霉素开始时间"]) else "NA"
            to_df.loc[new_row_index, "可利霉素后7天"] = time_value7.strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "可利霉素开始时间"]) else "NA"
            to_df.loc[new_row_index, "结束可利霉素时间"] = time_value9.strftime("%Y/%m/%d") if not pd.isna(from_df2.loc[index, "结束可利霉素时间"]) else "NA"
            new_row_index += 1
        except Exception as e:
            print(index)
            raise e
    to_df.to_excel('../data/可利霉素_wkyc_wide_01_initial.xlsx', index=False)


if __name__ == '__main__':
    main()
