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
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)      # 將圖像轉換為HSV色彩空間
        return  hsv_image     # 回傳ROI、原始圖片

    def Statistical(channel):       # 讀取單一個通道的所有數值 並計算所有統計指標 輸入通道值 回傳所有統計指標
        copied_list = copy.deepcopy(channel)        # deepcopy傳入的通道 以免影響原本的資料
        arr = copied_list[copied_list != 0]     # 去除為0的像素
        mean = np.mean(arr)     # 計算通道所有數值的平均值
        median = np.median(arr)     # 計算通道所有數值的中位數
        variance = np.var(arr)      # 計算通道所有數值的變異數
        std_dev = np.std(arr)       # 計算通道所有數值的標準差
        percentile_25 = np.percentile(arr, 25)      # 計算通道所有數值的25百分位數
        percentile_75 = np.percentile(arr, 75)      # 計算通道所有數值的75百分位數
        all = [mean, median, variance, std_dev, percentile_25, percentile_75]
        return all      # 回傳所有統計指標

    def statistical_indicator_processing(result):      # 轉換顏色空間 儲存所有通道的統計指標到list 輸入ROI圖片
        # 讀取個通道值
        channel1 = result[:, :, 0]       # 第一個通道
        channel2 = result[:, :, 1]        # 第二個通道
        channel3 = result[:, :, 2]     # 第三個通道
        # 計算通道各項統計指標
        Statistical1 = Statistical(channel1)        # 計算第一個通道的統計指標
        Statistical2 = Statistical(channel2)     # 計算第二個通道的統計指標
        Statistical3 = Statistical(channel3)      # 計算第三個通道的統計指標
        #將各項統計指標儲存到個別的list
        hsv_h.append(Statistical1)        # 第一個通道平均值加入lsit
        hsv_s.append(Statistical2)        # 第二個通道平均值加入lsit
        hsv_v.append(Statistical3)        # 第三個通道平均值加入lsit
        
    def excel_data(picture):      # 照片名稱、面積 加入list 輸入圖片名稱 原始圖片面積
        picture_name = os.path.splitext(picture)      # 取出照片名稱（不含位址）
        name.append(picture_name[0])        # 將名稱加入 name list

    def save_excel_data(name,hsv_h,hsv_s,hsv_v):       
        # 儲存所有值到excel檔案當中的個別種類工作表中
        # excel column 名稱
        hsv_h = np.array(hsv_h)       # mean,median,variance,std_dev,percentile_25,percentile_75      # mean,median,variance,std_dev,percentile_25,percentile_75
        hsv_s = np.array(hsv_s) 
        hsv_v = np.array(hsv_v) 

        filename = os.path.basename(source_path1)
        file_path = f"stage1_excels/{a}/{filename}_color_space.xlsx"        # excel 儲存位址
        column = ["name",
                "hsv_h_mean","hsv_h_median","hsv_h_variance","hsv_h_std_dev","hsv_h_percentile_25","hsv_h_percentile_75",
                "hsv_s_mean","hsv_s_median","hsv_s_variance","hsv_s_std_dev","hsv_s_percentile_25","hsv_s_percentile_75",
                "hsv_v_mean","hsv_v_median","hsv_v_variance","hsv_v_std_dev","hsv_v_percentile_25","hsv_v_percentile_75"]
        data = pd.DataFrame({column[0] : name,
                            column[1]: hsv_h[:,0], column[2]: hsv_h[:,1], column[3]: hsv_h[:,2], column[4]: hsv_h[:,3], column[5]: hsv_h[:,4], column[6]: hsv_h[:,5],
                            column[7]: hsv_s[:,0], column[8]: hsv_s[:,1], column[9]: hsv_s[:,2], column[10]: hsv_s[:,3], column[11]: hsv_s[:,4], column[12]: hsv_s[:,5],
                            column[13]: hsv_v[:,0], column[14]: hsv_v[:,1], column[15]: hsv_v[:,2], column[16]: hsv_v[:,3], column[17]: hsv_v[:,4], column[18]: hsv_v[:,5]})       # 所有資料變成dataframe
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
            hsv_h = []      # mean,median,variance,std_dev,percentile_25,percentile_75
            hsv_s = []
            hsv_v = []
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
                statistical_indicator_processing(hsv_image)       # 轉換顏色空間 儲存所有通道的統計指標到list 輸入ROI圖片
                excel_data(picture)       # 照片名稱、面積 加入list 輸入圖片名稱 原始圖片面積
            time.sleep(0.1)  # 模拟操作耗时
            # 儲存所有值到excel檔案當中的個別種類工作表中
            save_excel_data(name,hsv_h,hsv_s,hsv_v)         
            print(count)    #   图片個数
