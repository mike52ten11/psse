
import chardet
import numpy as np
import pandas as pd
import os


from ..base.get_error import error_handler
@error_handler
def transformer(raw_data, rawfilepath
                            , three_winding_npzfilepath
                            ,three_winding_filter_dir
                            , two_winding_npzfilepath
                            ,two_winding_filter_dir
                            , bus_data_dict):
    os.makedirs(three_winding_filter_dir, exist_ok=True)
    os.makedirs(two_winding_filter_dir, exist_ok=True)
    # 偵測編碼
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # 轉換為正確的編碼
    text = raw_data.decode(encoding)    
    ################## Transformer DATA#################################
    two_winding_transformer_data = []
    three_winding_transformer_data = []

    two_winding_from_bus_number = []
    two_winding_from_bus_name = []
    two_winding_to_bus_number = []
    two_winding_to_bus_name = []
    two_winding_transformer_id = []
    two_winding_transformer_name = []

    three_winding_from_bus_number = []
    three_winding_from_bus_name = []
    three_winding_to_bus_number = []
    three_winding_to_bus_name = []
    three_winding_last_bus_number = []
    three_winding_last_bus_name = []
    three_winding_transformer_id = []
    three_winding_transformer_name = []

    recording_transformer = False  # 標記是否開始記錄 branch 資料

    for line in text.splitlines():
        if 'BEGIN TRANSFORMER DATA' in line:  # 找到 BRANCH 資料的開始
            recording_transformer = True  # 開始記錄 branch 資料
            continue
        if recording_transformer:
            if '0 / END OF TRANSFORMER DATA' in line:  # 遇到結尾標記
                break  # 停止記錄
            if '@!' in line:  # 遇到標頭標記
                continue             
        if line.strip():  # 確保行不為空
            # 檢查是否為變壓器的主資料行
            columns = line.split(',')

            if len(columns) >= 11 and "'" in columns[3]:  
                bus_num1 = columns[0].strip()
                bus_num2 = columns[1].strip()
                bus_num3 = columns[2].strip()
                transformer_id = columns[3].strip()[1:-1]
                transformer_name = columns[10].strip()[1:-1]  # 提取名稱

                 # 獲取 bus 名稱
                bus_name1 = bus_data_dict.get(bus_num1, '')
                bus_name2 = bus_data_dict.get(bus_num2, '')
                bus_name3 = bus_data_dict.get(bus_num3, '')

                # 判斷變壓器類型
                if bus_num3 == '0':  # 雙向變壓器      
                    two_winding_from_bus_number.append(bus_num1)
                    two_winding_from_bus_name.append(bus_name1)
                    two_winding_to_bus_number.append(bus_num2)
                    two_winding_to_bus_name.append(bus_name2)
                    two_winding_transformer_id.append(transformer_id)
                    two_winding_transformer_name.append(transformer_name)     
                                   
                    two_winding_transformer_data.append(f"{bus_num1}, {bus_name1}, {bus_num2}, {bus_name2}, {transformer_id}, '{transformer_name}'")
                else:  # 三相變壓器
                    three_winding_from_bus_number.append(bus_num1)
                    three_winding_from_bus_name.append(bus_name1)
                    three_winding_to_bus_number.append(bus_num2)
                    three_winding_to_bus_name.append(bus_name2)
                    three_winding_last_bus_number.append(bus_num3)
                    three_winding_last_bus_name.append(bus_name3)
                    three_winding_transformer_id.append(transformer_id)
                    three_winding_transformer_name.append(transformer_name)                   


                    three_winding_transformer_data.append(f"{bus_num1}, {bus_name1}, {bus_num2}, {bus_name2}, {bus_num3}, {bus_name3},{transformer_id}, '{transformer_name}'")                                                        

    np.savez(f'{two_winding_npzfilepath}', fromnum = two_winding_from_bus_number, fromname = two_winding_from_bus_name
                                        , tonum = two_winding_to_bus_number, toname = two_winding_to_bus_name
                                        ,transformer_id = two_winding_transformer_id
                                        ,transformer_name= two_winding_transformer_name)  

    np.savez(f'{three_winding_npzfilepath}', fromnum = three_winding_from_bus_number, fromname = three_winding_from_bus_name
                                        , tonum = three_winding_to_bus_number, toname = three_winding_to_bus_name
                                        , lastnum = three_winding_last_bus_number, lastname = three_winding_last_bus_name
                                        ,transformer_id = three_winding_transformer_id
                                        ,transformer_name= three_winding_transformer_name) 
    with open(f'{two_winding_filter_dir}/two_winding_transformer.txt', 'w', encoding='utf-8') as f:
        for transformer_line in two_winding_transformer_data:
            f.write(transformer_line + '\n')

    with open(f'{three_winding_filter_dir}/three_winding_transformer.txt', 'w', encoding='utf-8') as f:
        for transformer_line in three_winding_transformer_data:
            f.write(transformer_line + '\n')            
    # data = {"fromnum":from_branch_number, "fromname": from_branch_name
    #         ,"tonum":to_branch_number, "toname": to_branch_name
    #         ,"branch_id":branch_id}
    # df = pd.DataFrame(data)
    # df.to_excel(f'{filter_dir}/branch_data.xlsx', index=False, encoding='ansi')

    # 將 BRANCH 資料的對應 bus 名稱寫入 branch_data.txt

    return 'transformer'        