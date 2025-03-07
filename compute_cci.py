score1 = ['AMI', '充血性心力衰竭', '周围血管疾病', '脑血管病', '痴呆症', '呼吸系统疾病', '结缔组织病', '消化性溃疡疾病', '糖尿病']
score2 = ['糖尿病并发症', '偏瘫', 'CKD', '白血病', '恶性淋巴瘤']
score3 = ['肝脏疾病']
score6 = ['AIDS']

special = ['恶性肿瘤', '转移']

import pandas as pd

pd.set_option("display.max_row", None)

data = pd.read_excel("data/可利霉素分析(1).xlsx")

result = {
    "编号": [],
    "cci": [],
    "level": []
}

for i, row in data.iterrows():
    score = 0
    for s in score1:
        if int(row[s]) == 1:
            score += 1
    for s in score2:
        if int(row[s]) == 1:
            score += 2
    for s in score3:
        if int(row[s]) == 1:
            score += 3
    for s in score6:
        if int(row[s]) == 1:
            score += 6

    if int(row[special[0]]) == 1 and int(row[special[1]]) == 1:
        score += 6
    elif int(row[special[0]]) == 1:
        score += 2

    age = int(row["年龄"])
    if age >= 50:
        score += int((age-40)/10)
    if score == 0:
        level = 0
    elif 1<=score<=2:
        level = 1
    elif 3<=score<=4:
        level = 2
    elif score >= 5:
        level = 3
    else:
        level = -1
        print("exception")

    result["编号"].append(row["编号"])
    result["cci"].append(score)
    result["level"].append(level)



result_df = pd.DataFrame(result)
print(result_df["level"].value_counts(dropna=False))
result_df.to_csv("data/cci.csv", index=False)
