import pandas as pd

# 讀取 Excel 檔案
input_file_path = 'excels/PD/groupPD_color_space.xlsx'
df = pd.read_excel(input_file_path)

# 根據第 0 欄的前三個字元分組
df['group'] = df.iloc[:, 0].str[:2]

# 過濾出數字列
numeric_cols = df.select_dtypes(include='number').columns.tolist()

# 加入 'group' 列到數字列
cols_to_average = ['group'] + numeric_cols

# 計算第 1、2 和 3 欄的平均值
grouped_df = df[cols_to_average].groupby('group').mean()

# 重設索引，將 'group' 列作為新的第 0 欄
grouped_df.reset_index(inplace=True)

# 重新命名列
grouped_df.columns = ['name'] + [f'column{i+1}_mean' for i in range(len(numeric_cols))]

# 將結果寫入新的 Excel 檔案
output_file_path = 'your_output_file.xlsx'
grouped_df.to_excel(output_file_path, index=False)

print("新的 Excel 檔案已儲存。")
