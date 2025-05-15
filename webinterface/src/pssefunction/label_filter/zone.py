
import chardet
import numpy as np
import pandas as pd
import os


from webinterface.src.base.get_error import error_handler
@error_handler
def zone(raw_data, rawfilepath, npzfilepath,filter_dir):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################zone DATA#################################
    # 提取 AREA 資料並保留 bus 數字和名稱
    zone_data_dict = {}
    zone_data = []
    zone_num = []
    zone_name = []
    recording_zone = False  # 標記是否開始記錄 area 資料

    for line in text.splitlines():
        if 'BEGIN ZONE DATA' in line:  # 找到 AREA 資料的開始
            recording_zone = True  # 開始記錄 area 資料
            continue
        if recording_zone:
            if '0 / END OF ZONE DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:
                continue    
            # 分割行並提取所需的列
            columns = line.split(',')
            if len(columns) >= 2:  # 確保有足夠的列
                num = columns[0].strip()  # 取出 bus 數字
                name = columns[1].strip()[1:-1]  # 取出名稱
                # zone_data.append(f"{num},{name}")  # 添加格式化後的資料
                zone_data_dict[num] = name
                zone_name.append(name)
                zone_num.append(num)

    np.savez(f'{npzfilepath}', name=zone_name, num=zone_num) 
    # data = {"number":zone_num, "name": zone_name}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/zone_data.xlsx', index=False, encoding='ansi')
    # 將 AREA 資料寫入 area_data.txt
    with open(f'{filter_dir}/zone_data.txt', 'w', encoding='utf-8') as f:
        for num,name in zip(zone_num,zone_name):
            f.write(f"{num},{name}\n")  # 寫入每行資料    
    return zone_data_dict            