
import chardet
import numpy as np
import pandas as pd
import os


from webinterface.src.base.get_error import error_handler
@error_handler
def branch(raw_data, rawfilepath, npzfilepath,filter_dir, bus_data_dict):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################AREA DATA#################################

    from_branch_number = []
    to_branch_number = []
    from_branch_name = []
    to_branch_name = []
    branch_id = []
    recording_branch = False  # 標記是否開始記錄 branch 資料

    for line in text.splitlines():
        if 'BEGIN BRANCH DATA' in line:  # 找到 BRANCH 資料的開始
            recording_branch = True  # 開始記錄 branch 資料
            continue
        if recording_branch:
            if '0 / END OF BRANCH DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:  # 遇到結尾標記
                continue                
            row_value = line.split(',')   

            from_number  = row_value[0].strip()
            to_number  = row_value[1].strip()
            BranchId  = row_value[2].strip()[1:-1]
            # 只保留第一列的資料，並加上逗號
            from_branch_number.append(from_number)# 取出 from number    
            to_branch_number.append(to_number)# 取出 to number 
            from_branch_name.append(bus_data_dict.get(
                                                from_number, ''
                                            ) 
                            ) # 根據 from branch_number 查找 bus 名稱
            to_branch_name.append(bus_data_dict.get(
                                                to_number, ''
                                            ) 
                            ) # 根據 to branch_number 查找 bus 名稱

            branch_id.append(BranchId)
    np.savez(f'{npzfilepath}', fromnum=from_branch_number, fromname=from_branch_name
                            , tonum=to_branch_number, toname=to_branch_name
                            ,id=branch_id) 


    # 將 BRANCH 資料的對應 bus 名稱寫入 branch_data.txt
    with open(f'{filter_dir}/branch_data.txt', 'w', encoding='utf-8') as f:
        for from_number, from_name, to_number, to_name, branchid in zip(from_branch_number, from_branch_name, to_branch_number, to_branch_name, branch_id):
            f.write(f"{from_number},{from_name},{to_number},{to_name},{branchid}\n")  # 寫入每行資料