
import chardet
import numpy as np
import pandas as pd
import os

from webinterface.src.base.get_error import error_handler
@error_handler
def owner(raw_data, rawfilepath, npzfilepath,filter_dir):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################AREA DATA#################################
    # 提取  資料並保留 bus 數字和名稱

    owner_num = []
    owner_name = []
    recording_owner = False  # 標記是否開始記錄 area 資料

    for line in text.splitlines():
        if 'BEGIN OWNER DATA' in line:  # 找到 AREA 資料的開始
            recording_owner = True  # 開始記錄 area 資料
            continue
        if recording_owner:
            if '0 / END OF OWNER DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:
                continue                 
            # 分割行並提取所需的列
            columns = line.split(',')
            owner_num.append(columns[0].strip())
            owner_name.append(columns[1].strip()[1:-1])

    np.savez(f'{npzfilepath}', num=owner_num, name=owner_name) 
    # data = {"number":area_num, "name": area_name}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/area_data.xlsx', index=False, encoding='ansi')
    # 將 AREA 資料寫入 area_data.txt
    with open(f'{filter_dir}/owner_data.txt', 'w', encoding='utf-8') as f:
        for number, name in zip(owner_num, owner_name):
            f.write(f"{number},{name}\n")  # 寫入每行資料    