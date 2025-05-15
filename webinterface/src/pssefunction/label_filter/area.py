
import chardet
import numpy as np
import pandas as pd
import os

from webinterface.src.base.get_error import error_handler
@error_handler
def area(raw_data, rawfilepath, npzfilepath,filter_dir):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################AREA DATA#################################
    # 提取 AREA 資料並保留 bus 數字和名稱
    area_data_dict = {}
    area_data = []
    area_num = []
    area_name = []
    recording_area = False  # 標記是否開始記錄 area 資料

    for line in text.splitlines():
        if 'BEGIN AREA DATA' in line:  # 找到 AREA 資料的開始
            recording_area = True  # 開始記錄 area 資料
            continue
        if recording_area:
            if '0 / END OF AREA DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:
                continue                 
            # 分割行並提取所需的列
            columns = line.split(',')
            if len(columns) >= 5:  # 確保有足夠的列
                bus_num = columns[0].strip()  # 取出 bus 數字
                bus_name = columns[4].strip()[1:-1]  # 取出名稱
                area_data.append(f"{bus_num},{bus_name}")  # 添加格式化後的資料
                area_data_dict[bus_num] = bus_name

                area_name.append(bus_name)
                area_num.append(bus_num)

    np.savez(f'{npzfilepath}', name=area_name, num=area_num) 
    # data = {"number":area_num, "name": area_name}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/area_data.xlsx', index=False, encoding='ansi')
    # 將 AREA 資料寫入 area_data.txt
    with open(f'{filter_dir}/area_data.txt', 'w', encoding='utf-8') as f:
        for area_line in area_data:
            f.write(area_line + '\n')  # 寫入每行資料    
    return area_data_dict            