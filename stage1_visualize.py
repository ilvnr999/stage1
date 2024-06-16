# 1.读取数据
import pandas as pd
import numpy as np
#target_list = ['PD','SP','GA']
def main(target_list):
    for a in target_list:
        name = []
        name_2 = []
        R2 = []
        R2_2 = []
        df1 = pd.read_excel(f'excels/{a}/group{a}mean.xlsx')
        df2 = pd.read_excel(f'excels/{a}/pieces{a}mean.xlsx')
        
        alltag = df1.columns.tolist()
        for i in range(1, len(alltag)) :
            tags = alltag[i]
            #tags = 'hsv_h_std_dev'
            X = df1[[tags]]
            Y = df2[tags]

            # 2.模型训练
            from sklearn.linear_model import LinearRegression
            regr = LinearRegression()
            regr.fit(X,Y)

            score = regr.score(X,Y)
            print(tags,score)
            # 3.模型可视化
            from matplotlib import pyplot as plt
            plt.scatter(X,Y)
            plt.plot(X, regr.predict(X), color='red')  # color='red'设置为红色
            plt.title(f'{tags} \n{score}',fontsize=23)  # 添加标题
            plt.xlabel('group')
            plt.ylabel('pieces')
            plt.tight_layout()
            plt.savefig(f'chart/{a}{tags}.png') 
            plt.close()

            # 4.线性回归方程构造
           
            name.append(tags)
            R2.append(score)
        R2_list = np.argsort(R2)
        for i in R2_list:
            R2_2.append(R2[i])
            name_2.append(name[i])
        R2_2.sort(reverse=True)
        name_2.sort(reverse=True)
        df = pd.DataFrame({"name":name_2, "R2":R2_2})
        file_path = f'excels/{a}/{a}_RGB_R2.xlsx'     # 輸出excel檔案名稱
        with pd.ExcelWriter(file_path, engine = 'openpyxl', mode = 'w') as writer:
            df.to_excel(writer, index = False)
            print(f'{a} saved.')
