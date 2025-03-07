from scipy import stats
import pandas as pd


df = pd.read_excel('data/可利霉素分析_检验1_imputed2.xlsx')
print(df.columns.tolist())
# exit()

props = ['WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', 'IL6']
for prop in props:
    print("针对指标", prop)
    groups = []
    groups.append(df[f"{prop}"])
    for i in range(1, 7):
        groups.append(df[f"{prop}.{i}"])

    # perform Friedman Test
    result = stats.friedmanchisquare(*groups)
    # stats.wilcoxon()
    # print(result)
    print('Friedman结果：Statistics=%.10f, p=%.10f' % (result.statistic, result.pvalue))
    # for i in range(len(groups))
