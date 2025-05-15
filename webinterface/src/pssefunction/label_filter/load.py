
import chardet
import numpy as np
import pandas as pd
import os


from webinterface.src.base.get_error import error_handler
@error_handler
def load(raw_data, rawfilepath, npzfilepath,filter_dir, bus_data_dict):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################GENERATOR DATA#################################

    load_number = []
    load_name = []
    recording_load = False  # 標記是否開始記錄 branch 資料

    for line in text.splitlines():
        if 'BEGIN LOAD DATA' in line:  # 找到 BRANCH 資料的開始
            recording_load = True  # 開始記錄 branch 資料
            continue
        if recording_load:
            if '0 / END OF LOAD DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:  # 遇到結尾標記
                continue                
            row_value = line.split(',')   

            number  = row_value[0].strip()
            # 只保留第一列的資料，並加上逗號
            load_number.append(number)# 取出 number   
            load_name.append(bus_data_dict.get(
                                                number, ''
                                            ) 
                            ) # 根據 number 查找 bus 名稱             

    np.savez(f'{npzfilepath}', num = load_number, name = load_name) 

    # data = {"fromnum":from_branch_number, "fromname": from_branch_name
    #         ,"tonum":to_branch_number, "toname": to_branch_name
    #         ,"branch_id":branch_id}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/branch_data.xlsx', index=False, encoding='ansi')

    # 將 BRANCH 資料的對應 bus 名稱寫入 branch_data.txt
    with open(f'{filter_dir}/load_data.txt', 'w', encoding='utf-8') as f:
        for number, name in zip(load_number, load_name):
            f.write(f"{number},{name}\n")  # 寫入每行資料
    return 'load'        