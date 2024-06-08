import pandas as pd
import numpy as np
from collections import defaultdict

#target_list = ['PD','SP','GA']#'PD','SP','GA'
def main(target_list):
    excels = ['group', 'pieces']
    for a in target_list :
        for b in excels:
            color = []       
            hsv = []      # mean,median,variance,std_dev,percentile_25,percentile_75
            df = pd.read_excel(f'stage1_excels/{a}/{b}{a}_color_space.xlsx', engine='openpyxl')
            all_column = list(df.columns)
            all_column.remove('name')
            #print('所有列名稱',all_column)
            name = df['name'].values 
            for x in name:
                name1= x.split('-')
                color.append(name1[0])
            #print('只剩下色階的list',color)

            duplicates = defaultdict(list)
            for index, word in enumerate(color):
                duplicates[word].append(index)
            # 仅保留有多个位置的字符串
            duplicates = {word: positions for word, positions in duplicates.items() if len(positions) > 1}
            keys_list = list(duplicates.keys())     # 色階名字
            keys_list.sort(reverse=True)
            num = len(keys_list)        # 幾個色階
            #print('同一個顏色在哪些位子的dict',duplicates)
            #print('色階的順序的list',keys_list)
            #print('第一個色階的所有位子',duplicates[keys_list[0]])     # 某個色階相同的位子

            for tag_name in all_column:     # 瀏覽每個feature
                #print('現在統計指標',tag_name)
                tag = df[tag_name]      # 同個feature所有的值
                #print('統計指標的所有值',tag)
                temp = []
                for i in range(num):        # 每個色階
                    sum = 0
                    number = 0
                    for j in duplicates[keys_list[i]]:      # 相同顏色的位子
                        sum = sum + float(tag[j])
                        number +=1
                    #print(keys_list[i],'有',number,'個')
                    avr = sum / number
                    #print(keys_list[i],'色階的統計指標',tag_name,'的平均為',avr)
                    temp.append(avr)
                #print(temp)
                hsv.append(temp)
            #print(len(hsv))
                
                    
                    
            file_path = f"stage1_excels/{a}/{a}{b}_mean.xlsx"        # excel 儲存位址
            column = ["name",
                    "rgb_b_mean","rgb_b_median","rgb_b_variance","rgb_b_std_dev","rgb_b_percentile_25","rgb_b_percentile_75",
                "rgb_g_mean","rgb_g_median","rgb_g_variance","rgb_g_std_dev","rgb_g_percentile_25","rgb_g_percentile_75",
                "rgb_r_mean","rgb_r_median","rgb_r_variance","rgb_r_std_dev","rgb_r_percentile_25","rgb_r_percentile_75"]
            data = pd.DataFrame({column[0] : keys_list,
                                column[1]: hsv[0], column[2]: hsv[1], column[3]: hsv[2], column[4]: hsv[3], column[5]: hsv[4], column[6]: hsv[5],
                                column[7]: hsv[6], column[8]: hsv[7], column[9]: hsv[8], column[10]: hsv[9], column[11]: hsv[10], column[12]: hsv[11],
                                column[13]: hsv[12], column[14]: hsv[13], column[15]: hsv[14], column[16]: hsv[15], column[17]: hsv[16], column[18]: hsv[17]})       # 所有資料變成dataframe
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:     # 設定？
                data.to_excel(writer, index=False)       # 將資料寫入excel
                print(f"{b}{a} Excel file saved.")