import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import copy

# 圖像經過閥值處理，'計算面積'和顏色通道的各'種統計指標'，原始圖像以及數據的excel
# 輸出color_space、ROI圖片
def main(target_list):

    def find_ROI(picture):      # 讀取相片選取出ROI 輸入相片路徑 回傳ROI 原始圖像
        image = cv2.imread(picture)     # 讀取資料源圖像
        #hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)      # 將圖像轉換為HSV色彩空間
        return  image     # 回傳ROI、原始圖片

    def statistical_indicator_processing(result,a):      # 轉換顏色空間 儲存所有通道的統計指標到list 輸入ROI圖片
        if a == 'PD':
            result1 = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
            channel = result1[:, :, 2]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag1_value = np.median(arr)     # 計算通道所有數值的中位數
            tag1.append(tag1_value)

            result2 = cv2.cvtColor(result, cv2.COLOR_BGR2YUV)
            channel = result2[:, :, 0]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag2_value = np.percentile(arr, 75)      # 計算通道所有數值的75百分位數
            tag2.append(tag2_value)

            result3 = cv2.cvtColor(result, cv2.COLOR_BGR2XYZ)
            channel = result3[:, :, 0]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag3_value = np.percentile(arr, 75)      # 計算通道所有數值的75百分位數
            tag3.append(tag3_value)

        if a == 'SP':
            result1 = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
            channel = result1[:, :, 1]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag1_value = np.percentile(arr, 75)      # 計算通道所有數值的75百分位數
            tag1.append(tag1_value)

            result2 = cv2.cvtColor(result, cv2.COLOR_BGR2YUV)
            channel = result2[:, :, 0]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag2_value = mean = np.mean(arr)     # 計算通道所有數值的平均值
            tag2.append(tag2_value)

            result3 = cv2.cvtColor(result, cv2.COLOR_BGR2XYZ)
            channel = result3[:, :, 0]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag3_value = np.percentile(arr, 75)      # 計算通道所有數值的75百分位數
            tag3.append(tag3_value)

        if a == 'GA':
            result1 = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
            channel = result1[:, :, 0]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag1_value = np.median(arr)     # 計算通道所有數值的中位數
            tag1.append(tag1_value)

            channel = result1[:, :, 1]       # 第一個通道
            arr = channel[channel != 0]    # 去除為0的像素
            tag2_value = np.median(arr)     # 計算通道所有數值的中位數
            tag2.append(tag2_value)

            arr = channel[channel != 0]    # 去除為0的像素
            tag3_value = np.percentile(arr, 75)      # 計算通道所有數值的75百分位數
            tag3.append(tag3_value)
        
    def save_name(picture):      # 照片名稱、面積 加入list 輸入圖片名稱 原始圖片面積
        picture_name = os.path.splitext(picture)      # 取出照片名稱（不含位址）
        name.append(picture_name[0])        # 將名稱加入 name list

    def save_excel_data(name,tag1,tag2,tag3):       
        # 儲存所有值到excel檔案當中的個別種類工作表中
        # excel column 名稱
        '''tag1 = np.array(tag1)       # mean,median,variance,std_dev,percentile_25,percentile_75
        tag2 = np.array(tag2) 
        tag3 = np.array(tag3)''' 

        filename = os.path.basename(source_path1)
        file_path = f"excels/{a}/{filename}_color_space.xlsx"        # excel 儲存位址
        column = ["name",'tag1','tag2','tag3']
        data = pd.DataFrame({'name':name, 'tag1':tag1, 'tag2':tag2, 'tag3':tag3})       # 所有資料變成dataframe
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:     # 設定？
            data.to_excel(writer, index=False)       # 將資料寫入excel
            print(f"{b}{a} Excel file saved.")

    # main
    # 宣告各項list    
    #target_list = ['PD','SP','GA']

    excels = ['group', 'pieces']
    for a in target_list :
        for b in excels:
            target = f'stage1_data/{b}{a}' #'PD','SP',
            name = []       
            tag1 = []      # mean,median,variance,std_dev,percentile_25,percentile_75
            tag2 = []
            tag3 = []
            count = 0     # 計數幾張照片
            # 讀取資料夾內的照片
            source_path1 = target       # 讀取資料源第一個資料夾
            dirs1 = os.listdir( source_path1 )      # image下有哪些資料夾 
            for picture in tqdm(dirs1, desc='pictures', unit='items' ):     # 處理 第二層下的照片（照片）
                if picture == '.DS_Store' : continue        # macos資料夾錯誤
                path2 = os.path.join(source_path1, picture)     # 結合路徑 (資料源資料夾＋物種資料夾)＋照片
                count += 1      # 計算照片數量
                #圖片處理

                hsv_image = find_ROI(path2)       # 讀取相片選取出ROI 輸入相片路徑 回傳ROI圖片 原始圖像
                statistical_indicator_processing(hsv_image,a)       # 轉換顏色空間 儲存所有通道的統計指標到list 輸入ROI圖片
                save_name(picture)       # 照片名稱、面積 加入list 輸入圖片名稱 原始圖片面積
            time.sleep(0.1)  # 模拟操作耗时
            # 儲存所有值到excel檔案當中的個別種類工作表中
            save_excel_data(name,tag1,tag2,tag3)         
            print(count)    #   图片個数
