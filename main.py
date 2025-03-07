from tqdm import tqdm
import pandas as pd
from scipy.stats import normaltest
from plottable import Table
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
import pandas as pd
import numpy as np

# pandas设置最大显示行和列
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 调整显示宽度，以便整行显示
pd.set_option('display.width', 1000)

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)
# 黑体（宋体？） SimHei
# 微软雅黑 Microsoft YaHei
# 微软正黑体 Microsoft JHengHei
# 新宋体 NSimSun
# 新细明体 PMingLiU
# 细明体 MingLiU
# 标楷体 DFKai-SB
# 仿宋 FangSong
# 楷体 KaiTi
# 仿宋-GB2312 FangSong_GB2312
# 楷体-GB2312 KaiTi_GB2312

# font.sans-serif : SimHei, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
# ‘font.family’ 用于显示字体的名字
# ‘font.style’ 字体风格，正常’normal’ 或斜体’italic’
# ‘font.size’ 字体大小，整数字号或者’large’ ‘x-small’



df = pd.read_excel("data/可利霉素分析(1).xlsx", sheet_name="基线情况")
print(df.columns.tolist())
# exit(0)
# print(df.dtypes.to_dict())
titles = ['可利霉素时间','APACHEII', 'SOFA', '身高', '体重（kg）', 'BMI', "0死亡；1放弃；2康复；3出院",
         '死亡',
         '28天死亡',
         '入ICU',
         '新冠',
         '年龄', '性别',
         '病房类型（内科、外科、ICU）',
         '抽烟',
         '饮酒',
         '糖尿病',
         '糖尿病并发症',
         '心衰',
         '高血压',
         'COPD',
         '冠心病',
         '脑血管病',
         'CKD',
         '呼吸系统疾病',
         '恶性肿瘤',
         '转移',
         'AMI',
         '充血性心力衰竭',
         '周围血管疾病',
         '痴呆症',
         '结缔组织病',
         '消化性溃疡疾病',
         '偏瘫',
         '脑梗死',
         '实体瘤',
         '白血病',
         '恶性淋巴瘤',
         '肝脏疾病',
         'AIDS',
      '真菌感染',
         '严重肺炎',
         '呼吸衰竭',
         '肾功能不全',
         '消化道出血',
         '中风',
         '肝功能不全',
         '心功能不全',
         '心肌梗塞',
         '休克',
         '血管活性药物',
         '血活时间', '气管插管',
        # '拔出插管',
         '气管切开',
         '机械通气（脱机时间）',
         '无创',
         '高流量',
         '鼻导管',
         'AKI',
         'CRRT',
         'GM',
         '真菌D',
          '真菌抗生素', '病毒', '病毒名称', '抗病毒药物', '其他.1', '可利霉素使用时间（天）', '方式', '联合抗生素', '真菌', '病毒.1', '磺胺', '喹诺酮类', '青霉素类', 'β内酰胺酶抑制剂', '头孢类', '碳青霉烯类', '大环内酯类', '氨基糖苷类', '糖肽类', '恶唑烷酮类', '甲硝唑', '四环素', '氯霉素', '环酯肽类', '粘菌素']
con_titles = {'可利霉素时间', 'APACHEII', 'SOFA', '身高', '体重（kg）', 'BMI','年龄', '血活时间'}
value_map = {
    "0死亡；1放弃；2康复；3出院": {
        0: "死亡",
        1: "放弃",
        2: "康复",
        3: "出院"
    },
    "死亡": {
        0: "存活",
        1: "死亡"
    },
    "28天死亡": {
        0: "存活",
        1: "死亡"
    },
}
new_df1 = pd.DataFrame(columns=["Variable", "Character"])
new_df2 = pd.DataFrame(columns=["Variable","Class", "Character"])

for title in tqdm(titles):
    if title in con_titles:  # 连续型
        values = df[title]
        test_result = normaltest(values)
        details = values.describe()
        if test_result.pvalue < 0.05:
            character = f"{round(details['50%'],2)} ({round(details['25%'],2)}-{round(details['75%'],2)})"
        else:
            character = f"{round(details['mean'],2)} (± {round(details['std'], 2)})"
        new_df1 = new_df1._append({"Variable": title, "Character": character}, ignore_index=True)
    else:  # 分类型
        values = df[title]
        # new_df2 = new_df2._append({"Variable": title, "Character": ""}, ignore_index=True)
        character = values.value_counts()
        s = character.sum()
        for index, item in character.items():
            try:
                if title in value_map:
                    sub_title = value_map[title].get(index, index)
                else:
                    try:
                        if int(index) == 0:
                            sub_title = "无"
                        elif int(index) == 1:
                            sub_title = "有"
                        else:
                            sub_title = index
                    except:
                        sub_title = index
                new_df2 = new_df2._append({"Variable": title, "Class":sub_title, "Character": f"{item} ({round(item/s*100, 2)}%)"}, ignore_index=True)
            except Exception as e:
                print("="*50)
                print(character)
                print(e)
                # print(i)
                # print(item)
# print(new_df)
# new_df.style
new_df1.to_csv("data/可利霉素分析_baseline1_0922.csv", index=False)
new_df2.to_csv("data/可利霉素分析_baseline2_0922.csv", index=False)


# fig, ax = plt.subplots(figsize=(10, 28))
# Table(new_df, columns=new_df.columns.tolist(),
#       row_dividers=False)
# plt.show()
