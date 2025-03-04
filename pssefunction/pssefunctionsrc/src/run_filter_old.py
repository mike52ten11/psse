
import re
import subprocess
import numpy as np
import chardet
from base.run_pyfile_by_execmd import Run_pyfile_by_execmd
import pandas as pd
def writeFile(filename, data):

    with open(filename, "wb")  as f:
        f.write(data)

def get_saved_case_text(byte_text):
    marker = b"The Saved Case in file"
    if marker in byte_text:
        after_marker = byte_text[byte_text.index(marker):]
        print("第一部分 - The Saved Case in file 之後的文字:")
        # print(after_marker)
    else:
        after_marker = ''    
    return after_marker

def get_area_info(byte_text):
    number =[]
    name = []
    
    pattern = rb'^\s*(\d+)\s+([^\d].*?)(?:\s{2,}|$)'
    matches = re.finditer(pattern, byte_text, re.MULTILINE)
    for match in matches:
        number.append(match.group(1).decode('ansi'))
        name.append(match.group(2).strip().decode('ansi'))
        # print('number-->',number)
        # print('name-->',name)
    return number,name

def get_zone_info(byte_text):
    number =[]
    name = []
    
    pattern = rb'^\s*(\d+)\s+([^\d].*?)(?:\s{2,}|$)'
    matches = re.finditer(pattern, byte_text, re.MULTILINE)
    for match in matches:
        number.append(match.group(1).decode('ansi'))
        name.append(match.group(2).strip().decode('ansi'))

    return number,name

def get_owner_info(byte_text):
    lines = byte_text.split(b'\n')
    
    # Initialize lists to store data
    number =[]
    name = []
    
    for line in lines:
        # Skip empty lines and header lines
        if not line.strip() or b'OWNER' in line or b'PSS' in line or b'#' in line:
            if b'Sets PSSE environment' in line:
                pass
            else:    
                continue
            

        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit() and not parts[1].isdigit():
            number.append(int(parts[0]))
            # Join the remaining parts as the name (handling multi-word names)
            # if not parts[1].isdigit():
            name.append(parts[1].decode('ansi'))

    # print('number-->',len(number))
    # print('name-->',len(name))
    return number,name

def get_machine_info(byte_text):
    lines = byte_text.split(b'\n')
    
    # Initialize lists to store data
    number =[]
    name = []
    machine_id = []
    for line in lines:
            

        parts = line.split()


        # print('parts', parts)
        if len(parts) >= 2 and parts[0].isdigit():
    
            if  '.' not in parts[4].decode('ansi'):
                # print('==========================================================')
                number.append(int(parts[0].decode('ansi')))

                name.append(parts[1].decode('ansi'))
                machine_id.append(parts[4].decode('ansi'))



    return number,name, machine_id   

def get_load_info(byte_text):
    lines = byte_text.split(b'\n')
    
    # Initialize lists to store data
    number =[]
    name = []
    for line in lines:
            

        parts = line.split()


        # print('parts', parts)
        if len(parts) >= 2 and parts[0].isdigit() :
            if  '.' not in parts[4].decode('ansi'):
                # print('==========================================================')
                number.append(int(parts[0].decode('ansi')))

                name.append(parts[1].decode('ansi'))
                # machine_id.append(parts[4].decode('ansi'))

    # data = {"number":number, "name": name}
    # df = pd.DataFrame(data)
    # df.to_excel('load_115P.xlsx', index=False, encoding='ansi')
    
    return number,name

def get_branch_info(byte_text):
    data = []
    from_bus_of_npy = []
    from_name_of_npy = []
    to_bus_of_npy = [] 
    to_name_of_npy = []  
    circuit_id_of_npy = []    
    lines = byte_text.split(b'\n')
    # 處理每一行
    for line in lines:
        
        # 跳過空行和包含特定字串的標題行
        if not line.strip() or b"BUS POWER SYSTEM" in line or b"PSS(R)E" in line or b"Copyright" in line:
            continue
        
        # 分割行並清理空白
        parts = line.split(b'.')
        
        if len(parts) >= 2:
                        

            if parts[0][0:7].strip().isdigit():
                try:
                    # 嘗試轉換第一個部分為數字
                    from_bus = int(parts[0][0:7].strip())
                    # 第二個部分為名稱
                    from_name = parts[0][7:]
                    to_bus = int(parts[1][5:11].strip())
                    to_name = parts[1][11:]
                    circuit_id = parts[2].split()[1].strip()
                    if not to_name==b'':
                        from_bus_of_npy.append(from_bus)
                        from_name_of_npy.append(from_name.decode('ansi'))
                        to_bus_of_npy.append(to_bus)
                        to_name_of_npy.append(to_name.decode('ansi'))
                        circuit_id_of_npy.append(circuit_id.decode('ansi'))
                except Exception as e:
                    pass
                    # print('error parts error --> ', e)
                    # print('==================================')
            else:
                pass
                # 如果轉換失敗，跳過該行
                # print('error parts --> ', parts)
                # print('==========================================================') 

    return from_bus_of_npy, from_name_of_npy, to_bus_of_npy, to_name_of_npy, circuit_id_of_npy

def process_psse_data(input_text):
    # 使用正則表達式來分割數據
    # 這個正則表達式會嘗試找出每一筆記錄的模式
    pattern = r'(\d+)\s+([^\d]+?)(?=\d+\s|$)'
    
    # 找出所有匹配的記錄
    matches = re.findall(pattern, input_text, re.DOTALL)
    
    # 創建DataFrame
    df = pd.DataFrame(matches, columns=['number', 'name'])
    
    # 去除每個欄位的多餘空白
    # df['number'] = df['number'].str.strip()
    # df['name'] = df['name'].str.strip()
    # df.to_excel('../Data/User/621882/filter/transformer_data_test.xlsx', index=False)
    return df

def get_twowinding_info(byte_text):


    # 使用範例
    
    result = process_psse_data(byte_text.decode("ISO-8859-1"))
    print(result)


    from_bus_of_npy = []
    from_name_of_npy = []
    to_bus_of_npy = [] 
    to_name_of_npy = []  
    circuit_id_of_npy = []    
    lines = byte_text.split(b'\n')
    # 處理每一行
    for line in lines:
        
        # 跳過空行和包含特定字串的標題行
        if not line.strip() or b"BUS POWER SYSTEM" in line or b"PSS(R)E" in line or b"Copyright" in line:
            continue
        
        # 分割行並清理空白
        parts = line.split(b'.')
        
        if len(parts) >= 2:
                        

            if parts[0][0:7].strip().isdigit():
                try:
                    # 嘗試轉換第一個部分為數字
                    from_bus = int(parts[0][0:7].strip())
                    # 第二個部分為名稱
                    from_name = parts[0][7:]
                    to_bus = int(parts[1][5:11].strip())
                    to_name = parts[1][11:]
                    circuit_id = parts[2].split()[1].strip()
                    if not to_name==b'':
                        from_bus_of_npy.append(from_bus)
                        from_name_of_npy.append(from_name.decode('ansi'))
                        to_bus_of_npy.append(to_bus)
                        to_name_of_npy.append(to_name.decode('ansi'))
                        circuit_id_of_npy.append(circuit_id.decode('ansi'))
                except Exception as e:
                    print('error parts error --> ', e)
                    print('==================================')
            else:
                # 如果轉換失敗，跳過該行
                print('error parts --> ', parts)
                print('==========================================================') 
    
    # data = {"from_bus":from_bus_of_npy, 
    #         "from_name": from_name_of_npy, 
    #         "to_bus": to_bus_of_npy, 
    #         "to_name": to_name_of_npy, 
    #         "circuit_id": circuit_id_of_npy
    #         }
    # df = pd.DataFrame(data)
    # df.to_excel('../Data/User/621882/filter/transformer_data_test.xlsx', index=False)

    return from_bus_of_npy, from_name_of_npy, to_bus_of_npy, to_name_of_npy, circuit_id_of_npy


def check_encoding_type(checked_data):
     
    return chardet.detect(checked_data)['encoding']           

def run_filter_by_label(labeltype 
                        ,savfile_name 
                        ,userName 
                        ,savfiledir
                        ,targetdir ):

    cmd = Run_pyfile_by_execmd(python_location= "python"
                                        ,pyfile= "pssefunctionsrc/src/filter.py"
                                        ,args= f"--Label_type {labeltype} "\
                                            f"--Sav_File {savfile_name} "
                                            f"--User_name {userName} " 
                                            f"--savfiledir {savfiledir} "\
                                            f"--target_dir {targetdir}")    
    
    # writeFile(f'{targetdir}/{labeltype}/cmd.txt', f'{cmd}'.encode())

    r = subprocess.run(cmd,capture_output=True, shell=True)
    if r.returncode == 0:
        if labeltype == 'area' :
            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)

            saved_case_text = get_saved_case_text(r.stdout)
            print(saved_case_text)
            if saved_case_text:
                number,name = get_area_info(saved_case_text)
                number = np.array(number)  # 'S' dtype 用於 byte strings
                name = np.array(name)            
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz',name=name, num=number) 
        
        elif labeltype == 'zone':

            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)

            saved_case_text = get_saved_case_text(r.stdout)
            if saved_case_text:
                number, name = get_zone_info(saved_case_text)
                number = np.array(number)  # 'S' dtype 用於 byte strings
                name = np.array(name)
                           
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz',name=name, num=number) 

        elif labeltype == 'owner':

            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)

            saved_case_text = get_saved_case_text(r.stdout)
            # print(saved_case_text)
            if saved_case_text:
                number,name = get_owner_info(saved_case_text)
                number = np.array(number)  # 'S' dtype 用於 byte strings
                name = np.array(name)            
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz',name=name, num=number) 
        elif labeltype == 'machine':

            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)

            saved_case_text = get_saved_case_text(r.stdout)
            # print(saved_case_text)
            if saved_case_text:
                number,name, machine_id = get_machine_info(saved_case_text)
                number = np.array(number)  # 'S' dtype 用於 byte strings
                name = np.array(name)
                machine_id = np.array(machine_id)    
                # print('number', number)  
                # print('name', name)           
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz',name=name, num=number,id=machine_id)         
        
        elif labeltype == 'load':
            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)

            saved_case_text = get_saved_case_text(r.stdout)
            # print(saved_case_text)
            if saved_case_text:
                number, name = get_load_info(saved_case_text)
                number = np.array(number)  # 'S' dtype 用於 byte strings
                name = np.array(name)         
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz',name=name, num=number)         
        
        elif labeltype == 'twowinding':
            
            
            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)

            saved_case_text = get_saved_case_text(r.stdout)
            # print(saved_case_text)
            if saved_case_text:
                from_bus_of_npy, from_name_of_npy, to_bus_of_npy, to_name_of_npy, circuit_id_of_npy = get_twowinding_info(saved_case_text)        
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz'
                , fromnum = from_bus_of_npy,fromname = from_name_of_npy
                , tonum = to_bus_of_npy,toname = to_name_of_npy
                ,circuit_id = circuit_id_of_npy)                

        elif labeltype == 'branch' or labeltype == 'tripline':

            writeFile(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.txt', r.stdout)
                                    
            saved_case_text = get_saved_case_text(r.stdout)
            if saved_case_text:
                from_bus_of_npy, from_name_of_npy, to_bus_of_npy, to_name_of_npy, circuit_id_of_npy = get_branch_info(saved_case_text)        
                np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz'
                , fromnum = from_bus_of_npy,fromname = from_name_of_npy
                , tonum = to_bus_of_npy,toname = to_name_of_npy
                ,circuit_id = circuit_id_of_npy)
        else:
            pass        

        
    else:
        encoding_type = check_encoding_type(r.stderr)
        print(encoding_type)
        error_message = r.stderr.decode(encoding_type).strip()          
        # error_message = r.stderr.decode().strip()
        print(f"Error occurred: {error_message}")        

def ParseConfig():
    import argparse
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-LabelT', '--Label_type', default="BUS", type=str, help='哪個Label')
    parser.add_argument('-SavF', '--Sav_FileName', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-user', '--User_name', default="User/621882/", type=str, help='使用者名稱')
    parser.add_argument('-sourcesavfile', '--savfiledir', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-TargetDir', '--target_dir', default="User/621882/", type=str, help='檔案來源資料夾路徑')

    args = parser.parse_args()

    labeltype = args.Label_type
    savfile_name = args.Sav_FileName
    username =   args.User_name
    savfiledir = args.savfiledir
    # source_savfile = f"{savfiledir}/{savfile_name}.sav"
    targetdir = args.target_dir

    return labeltype, savfile_name, username, savfiledir, targetdir

if __name__ == '__main__':

    labeltype, savfile_name, username, savfiledir, targetdir = ParseConfig()
    
    run_filter_by_label(labeltype = labeltype
                        ,savfile_name = savfile_name 
                        ,userName = username
                        ,savfiledir = savfiledir
                        ,targetdir = targetdir )    

    # with open(r'D:\Mike\Work_space\業務\電力室合作\改寫\Data\User\621882\filter\area\area_115Pnam.txt') as f:
    #     print(f.read())