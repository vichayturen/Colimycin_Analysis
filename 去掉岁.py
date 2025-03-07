import pandas as pd
import re



def handle(x: str) -> float:
    if isinstance(x, int):
        return x
    try:
        sui = 0
        yue = 0
        match = re.search(r"\d+岁", x)
        if match:
            sui = int(match.group().replace("岁", ""))
        match = re.search(r"\d+月", x)
        if match:
            yue = int(match.group().replace("月", ""))
        return sui + yue/12
    except Exception as e:
        print(x)
        print(type(x))
        print(e)
        exit(-1)


df = pd.read_excel('data/apacheii score.xlsx')
df['age'] = df['age'].map(handle)
df.to_excel('data/apacheii score_v1.xlsx', index=False)

