
import chardet
import numpy as np
import pandas as pd
import os
from webinterface.src.base.get_error import error_handler
@error_handler
def fixedshunt(raw_data, rawfilepath, npzfilepath,filter_dir, bus_data_dict):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################AREA DATA#################################

    fixedshunt_number = []
    fixedshunt_status = []
    fixedshunt_id = []
    fixedshunt_name = []

    recording_fixedshunt = False  # 標記是否開始記錄 branch 資料

    for line in text.splitlines():
        if 'BEGIN FIXED SHUNT DATA' in line:  # 找到 FIXEDSHUNT 資料的開始
            recording_fixedshunt = True  # 開始記錄 fixedshunt 資料
            continue
        if recording_fixedshunt:
            if '0 / END OF FIXED SHUNT DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:  # 遇到結尾標記
                continue                
            row_value = line.split(',')   

            number  = row_value[0].strip()            
            FixedshuntId  = row_value[1].strip()
            status = row_value[2].strip()
            # 只保留第一列的資料，並加上逗號
            fixedshunt_number.append(number)# 取出 number    
            fixedshunt_status.append(status)# 取出 status 
            fixedshunt_name.append(bus_data_dict.get(
                                                number, ''
                                            ) 
                            ) # 根據 number 查找 bus 名稱

            fixedshunt_id.append(FixedshuntId)

    np.savez(f'{npzfilepath}', num=fixedshunt_number, fixedshunt_name=fixedshunt_name
                            , status=fixedshunt_status, fixedshunt_id=fixedshunt_id) 

    # data = {"number":fixedshunt_number, "name": fixedshunt_name
    #         ,'fixedshunt_status':fixedshunt_status
    #         ,"fixedshunt_id":fixedshunt_id}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/fixedshunt_data.xlsx', index=False, encoding='ansi')

    # 將 BRANCH 資料的對應 bus 名稱寫入 branch_data.txt
    with open(f'{filter_dir}/fixedshunt_data.txt', 'w', encoding='utf-8') as f:
        for number, name, status, fixedshuntid in zip(fixedshunt_number, fixedshunt_name, fixedshunt_status, fixedshunt_id):
            f.write(f"{number},{name},{status},{fixedshuntid}\n")  # 寫入每行資料