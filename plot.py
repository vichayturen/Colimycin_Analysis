import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/可利霉素分析_baseline.csv")


plt.figure(figsize=(20,8))
tab = plt.table(cellText=df,
                colLabels=df.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
tab.scale(1,2)
plt.axis('off')

