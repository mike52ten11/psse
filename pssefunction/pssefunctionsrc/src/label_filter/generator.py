
import chardet
import numpy as np
import pandas as pd
import os


from ..base.get_error import error_handler
@error_handler
def generator(raw_data, rawfilepath, npzfilepath,filter_dir, bus_data_dict):
    os.makedirs(filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ##################GENERATOR DATA#################################

    generator_number = []
    generator_name = []
    generator_id = []
    recording_generator = False  # 標記是否開始記錄 branch 資料

    for line in text.splitlines():
        if 'BEGIN GENERATOR DATA' in line:  # 找到 BRANCH 資料的開始
            recording_generator = True  # 開始記錄 branch 資料
            continue
        if recording_generator:
            if '0 / END OF GENERATOR DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line: 
                continue                
            row_value = line.split(',')   

            number  = row_value[0].strip()
            GeneratorId  = row_value[1].strip()[1:-1]
            # 只保留第一列的資料，並加上逗號
            generator_number.append(number)# 取出 from number   
            generator_name.append(bus_data_dict.get(
                                                number, ''
                                            ) 
                            ) # 根據 from branch_number 查找 bus 名稱             
            generator_id.append(GeneratorId)# 取出 to number 


    np.savez(f'{npzfilepath}', num = generator_number, name = generator_name
                            ,machine_id = generator_id) 

    # data = {"fromnum":from_branch_number, "fromname": from_branch_name
    #         ,"tonum":to_branch_number, "toname": to_branch_name
    #         ,"branch_id":branch_id}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/branch_data.xlsx', index=False, encoding='ansi')

    # 將 BRANCH 資料的對應 bus 名稱寫入 branch_data.txt
    with open(f'{filter_dir}/machine_data.txt', 'w', encoding='utf-8') as f:
        for number, name, machineid in zip(generator_number, generator_name, generator_id):
            f.write(f"{number},{name},{machineid}\n")  # 寫入每行資料
    return 'generator'        