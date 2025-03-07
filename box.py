import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei'] #解决中文显示
plt.rcParams['axes.unicode_minus'] = False #解决符号无法显示


data = pd.read_csv(r'data\可利霉素分析_检验1_imputed3.csv')
print(data.columns.tolist())

# 生成示例数据
# data = np.random.normal(0, 1, 1000)
# all_props = ['WBC', 'N', 'L', 'MONO', 'HB', 'PLT', 'HCT', 'ALT', 'AST', 'TB', 'DB', 'ALB', 'G', 'BUN', 'Cr', 'PCT', 'CRP', '血沉', 'IL6']
all_props = ['L']

def relu(x):
    return max(0., x)

for prop in all_props:
    # prop = 'WBC'
    try:
        plt.figure()
        props = [prop]
        for i in range(1, 7):
            props.append(prop + '.' + str(i))
        df = data[props]
        df = df.applymap(relu)

        # 画箱线图
        plt.boxplot(df, whis=10, tick_labels=["入院/入ICU", "可利霉素前", "1-2天", "3-4天", "5-6天", "7-8天", "出院"], medianprops={'color': 'black'})
        # sns.set_style('darkgrid', {'font.sans-serif':['SimHei', 'Arial']})#设置图表背景颜色字体
        # sns.boxplot(y='charges', data=data, x='sex')
        plt.title(f'可利霉素前后{prop}变化')
        plt.xlabel('时间')
        # plt.xlim(0, 7)
        plt.ylabel(prop)

        # plt.xticks(np.array())

        # 显示图表
        print(plt)
        plt.show()
        plt.savefig(rf".\imgs2\{prop}_box_0917.png", dpi=400)
    except Exception as e:
        print(e)
        print(prop)
