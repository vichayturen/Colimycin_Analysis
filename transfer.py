import pandas as pd


data = pd.read_excel("data/可利霉素分析_检验1_imputed2.xlsx")

data.to_csv("data/可利霉素分析_检验1_imputed3.csv")
