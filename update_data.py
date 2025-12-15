import pandas as pd
import json
import os
# 移除 deep_translator 避免呼叫問題
# import requests # 移除 requests 避免不必要的依賴

# =================================================================
# ⚠️ 1. 設定檔案名稱與關鍵欄位名稱 (新增英文欄位定義)
# =================================================================
csv_file_name = '食品營養成分資料庫2024UPDATE2.xlsx - 工作表1.csv'
FOOD_NAME_COLUMN = '樣品名稱' 
CALORIE_COLUMN = '熱量(kcal)'
# 🚨 假設您的英文品名欄位名為 'English Name'
ENGLISH_NAME_COLUMN = 'English Name' 
# =================================================================


# 存檔路徑設定
target_folder = 'Sedentary_Lifestyle_Management'
filename = os.path.join(target_folder, 'food_database.json')
backup_filename = os.path.join(target_folder, 'food_database.backup.json')

# 確保資料夾存在
if not os.path.exists(target_folder):
    os.makedirs(target_folder, exist_ok=True)
    
print(f"正在讀取預先翻譯好的本地數據: {csv_file_name}...")

try:
    # 1. 讀取本機 CSV 檔案 (跳過非標題行)
    df = pd.read_csv(csv_file_name, encoding='utf-8-sig', skiprows=1)
    
    # 2. 不再需要讀取舊的 JSON 資料進行比對或翻譯，直接生成新的
    
    new_database_list = []
    
    # 3. 遍歷 CSV 數據，生成新的 JSON 列表
    for index, row in df.iterrows():
        # === 讀取中英雙欄位 ===
        zh_name = str(row.get(FOOD_NAME_COLUMN, '')).strip()
        en_name = str(row.get(ENGLISH_NAME_COLUMN, '')).strip()
        new_cal = str(row.get(CALORIE_COLUMN, '0')).strip()
        # =======================

        if pd.isna(zh_name) or zh_name == '': continue
        if new_cal == 'nan': new_cal = '0'
        
        new_database_list.append({
            "zh": zh_name,
            # 🚨 直接使用 CSV 中的英文名稱
            "en": en_name, 
            "cal": new_cal
        })

    # 4. 存檔與備份機制 (保持不變)
    if os.path.exists(filename):
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        os.rename(filename, backup_filename)
        print(f"已備份舊資料為 {backup_filename}")

    # 寫入最新的資料
    with open(filename, 'w', encoding='utf-8') as f:
        # 使用 ensure_ascii=False 確保中文不會變成 \uXXXX
        json.dump(new_database_list, f, ensure_ascii=False, indent=4)

    print(f"處理完成！資料已寫入: {filename}")
    print(f"- 總共處理了 {len(new_database_list)} 筆中英對照食物數據。")

except Exception as e:
    print(f"發生錯誤: {e}")
    if not os.path.exists(csv_file_name):
         print(f"錯誤提示：找不到檔案 {csv_file_name}，請確認它已在根目錄。")
    # 如果是欄位名稱錯誤，例如找不到 'English Name'
    elif ENGLISH_NAME_COLUMN not in df.columns or FOOD_NAME_COLUMN not in df.columns or CALORIE_COLUMN not in df.columns:
        print("錯誤提示：請檢查 Python 腳本中的欄位名稱是否與您的 CSV 標題列完全一致！")