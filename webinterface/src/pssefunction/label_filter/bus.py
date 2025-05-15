
import chardet
import numpy as np
import pandas as pd
import os


from webinterface.src.base.get_error import error_handler
@error_handler
def bus(raw_data, rawfilepath, npzfilepath,filter_dir,zone_data_dict, area_data_dict):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################AREA DATA#################################
    bus_data_dict = {}
    bus_number = []
    bus_name = []

    area_number = []
    area_name = []

    zone_number = []
    zone_name = []
    recording_bus = False  # 標記是否開始記錄 bus 資料

    for line in text.splitlines():
        if 'BEGIN BUS DATA' in line:  # 找到負載比例的行
            recording_bus = True  # 開始記錄
            continue
        if recording_bus:
            if '0 / END OF BUS DATA' in line:  # 遇到結尾標記
                break  # 停止記錄

            if '@!' in line:  # 遇到結尾標記
                continue
                
            # 分割行並保留所需的列
            columns = line.split(',')
            if len(columns) >= 4:  # 確保有足夠的列
                num = columns[0].strip()
                name = columns[1].strip()[1:-1]
                bus_number.append(num)
                bus_name.append(name)
                bus_data_dict[num] = name  # 將 bus 數字和名稱存入字典

                num = columns[4].strip()
                area_number.append(num)
                area_name.append(area_data_dict.get(num, ''))

                num = columns[5].strip()
                zone_number.append(num)
                zone_name.append(zone_data_dict.get(num, ''))

    np.savez(f'{npzfilepath}', name=bus_name, num=bus_number
                                ,zonenum=zone_number,zonename=zone_name
                                ,areanum=area_number,areaname=area_name) 
    # data = {"number":bus_number, "name": bus_name}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/bus_data.xlsx', index=False, encoding='ansi')
    # 將結果寫入 bus_data.txt
    with open(f'{filter_dir}/bus_data.txt', 'w', encoding='utf-8') as f:
        for bnum, bname,znum,zname,anum,aname in zip(bus_number,bus_name,zone_number,zone_name,area_number,area_name):
            f.write(f"{bnum},{bname},{znum},{zname},{anum},{aname}\n")
    return  bus_data_dict       