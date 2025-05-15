
# -*- coding: utf-8 -*-

def writeFile(filename, data):  
    f = open(filename, "wb")  
    f.write(data)  
    f.close()  

import subprocess
import shutil
import sys, os
import re
import struct
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
# from Config.Load_PSSE_Location import Load_PSSE_Path
# Load_PSSE_Path()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
# pssepy_PATH=(r"""C:\Program Files\PTI\PSSE35\35.3\PSSPY37""")
# sys.path.append(pssepy_PATH)
try:    
    pssepy_PATH = os.environ.get('PSSE') 
    sys.path.append(pssepy_PATH)    
    import psse35
    # psse35.set_minor(3)
    import psspy
    psspy.psseinit()
    # import pssexcel
    import argparse
    import logging
    # import dyntools 
except Exception as error: 
    print('error')
    writeFile('C:\server\project\AutoPsse\Backend\myweb\errorlog.txt', str(error)+'\n')
    raise ImportError(error)  

def read_out_file(filename):
    # 初始化結果
    time_data = []
    channel_data = {}  # 通道數據，鍵為通道編號，值為數據列表
    channel_ids = {}  # 通道 ID，鍵為通道編號，值為名稱

    try:
        with open(filename, "rb") as binfobj:
            # Step 1: 讀取檔案頭（12 字節）
            header = binfobj.read(12)
            if not header.startswith(b"FuP_pHyS"):
                print("錯誤：檔案不是有效的 .out 檔案")
                return None, None, None

            # 檢查字節序
            platform = header[-4:].decode('utf-8', errors='ignore')
            littlebyteorder = ["PCD%", "PCS%", "DEC%", "AXP%"]
            bigbyteorder = ["SUN%", "HPU%", "HPA%", "IBM%"]
            if platform in littlebyteorder:
                byteorder = "little"
                fmt = "<f"  # 小端序浮點數
            elif platform in bigbyteorder:
                byteorder = "big"
                fmt = ">f"  # 大端序浮點數
            else:
                print("錯誤：無法識別檔案的字節序")
                return None, None, None

            # Step 2: 讀取通道數量（4 字節）
            chunk = binfobj.read(4)
            nchannels = int(struct.unpack(fmt, chunk)[0])
            if nchannels <= 0:
                print("錯誤：檔案不包含通道數據")
                return None, None, None

            # Step 3: 讀取版本號（4 字節）
            chunk = binfobj.read(4)
            version = struct.unpack(fmt, chunk)[0]
            if version != 2.0:
                print(f"錯誤：檔案版本為 {version}，僅支援 2.0")
                return None, None, None

            # Step 4: 讀取通道 ID（32 字節 × 通道數量）
            channel_ids["time"] = "Time(s)"
            for ch in range(1, nchannels + 1):
                chname = binfobj.read(32).decode('utf-8', errors='ignore').strip()
                chname = chname.replace("  ", " ")  # 清理多餘空格
                channel_ids[ch] = chname

            # Step 5: 讀取短標題（60 字節 × 2）
            short_title = ""
            ln1 = binfobj.read(60).decode('utf-8', errors='ignore').strip()
            ln2 = binfobj.read(60).decode('utf-8', errors='ignore').strip()
            if ln1:
                short_title += ln1
            if ln2:
                short_title += "\n" + ln2
            print("短標題:", short_title)

            # Step 6: 計算數據部分的行數
            total_bytes = os.path.getsize(filename)
            begin_nondata_bytes = 12 + 4 + 4 + 32 * nchannels + 60 * 2
            end_nondata_bytes = 8
            databytes = total_bytes - begin_nondata_bytes - end_nondata_bytes
            ncols = nchannels + 2  # 通道數 + 時間 + 通道計數
            nrows = int(databytes / (ncols * 4))  # 每值 4 字節

            # Step 7: 讀取數據部分
            for _ in range(nrows):
                # 讀取通道數（4 字節，忽略或驗證）
                chunk = binfobj.read(4)
                if not chunk:
                    break
                # 讀取時間（4 字節）
                chunk = binfobj.read(4)
                if not chunk:
                    break
                time_val = struct.unpack(fmt, chunk)[0]
                time_data.append(time_val)
                # 讀取通道數據（4 字節 × 通道數）
                for ch in range(1, nchannels + 1):
                    chunk = binfobj.read(4)
                    if not chunk:
                        break
                    val = struct.unpack(fmt, chunk)[0]
                    if ch not in channel_data:
                        channel_data[ch] = []
                    channel_data[ch].append(val)

    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return None, None, None

    return time_data, channel_data, channel_ids

# def to_excel(excel_data,excel_path):
#     df = pd.DataFrame(excel_data)
#     df.to_excel(excel_path, index=False, encoding='ansi')
def get_channel_id_name(busdata,channel_id):   

    # 使用正則表達式匹配
    # [A-Z]{4} 匹配 4 個大寫字母 (ANGL)
    # \d+ 匹配一個或多個數字 (1131)
    # \d{2}\.\d{3} 匹配 xx.xxx 格式的小數 (25.000)
    pattern = r'([A-Z]{4})\s+(\d+)\[.*?\s+(\d{2}\.\d{3})\]'
    match = re.match(pattern, channel_id)

    # 提取結果
    if match:
        angl = match.group(1)  # ANGL
        number = match.group(2)  # 1131
        decimal = match.group(3)  # 25.000
        print(f"ANGL: {angl}, Number: {number}, Decimal: {decimal}")
    else:
        print("No match found")

    print(f"type(number)--> {type(number)}")
    name = busdata["name"][np.where(busdata["num"]==number)][0]
    
    return f"{angl} {number} [{name}] {decimal}"


    # name = {busdata["name"][np.where(busdata["num"]==part2)][0]}
    # # print(f"提取到的第二部分: {part2}")
    # return f"{part1} {part2} [{name}] {part3}"


def plot_channels(time_data, channel_data, channel_ids, busdata, jpg_file_path):
    font_path = '../Data/PlotFont/font/SimHei.ttf'  # 替換成你的字體路徑
    fm.fontManager.addfont(font_path)
    # 設置默認字體
    plt.rcParams['font.family'] = ['SimHei']  # 替換成你的字體名稱

    # 設置圖表大小和周邊背景顏色（灰色）
    plt.figure(figsize=(10, 6), facecolor='lightgray')
    ax = plt.gca()
    
    # 設置繪圖區域背景為白色
    ax.set_facecolor('white')

    # 調整圖表右側邊距，為圖例留出空間
    plt.subplots_adjust(right=0.75)

    # 定義線條顏色，與圖片匹配
    colors = ['green', 'red', 'blue', 'gray', 'yellow']
    color_idx = 0

    # 繪製每條通道的線條
    for ch_num, ch_data in channel_data.items():
        if ch_num in channel_ids and ch_num != "time":  # 跳過時間通道
            labelname = get_channel_id_name(busdata,channel_ids[ch_num])
            plt.plot(time_data, ch_data, label=labelname, color=colors[color_idx % len(colors)])
            color_idx += 1
    
    # 設置 X 和 Y 軸標籤
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Voltage", fontsize=12)

    # 設置 Y 軸範圍，與圖片一致
    # plt.ylim(25, 50)

    # 設置圖例，放置在圖表右側外部
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderpad=0.5, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10, frameon=False)

    # 啟用格線
    plt.grid(True)

    # 保存圖表
    plt.savefig(f'{jpg_file_path}', dpi=100, bbox_inches='tight')
    plt.close()

def datatoexcel(time_data, channel_data, channel_ids, excel_path):
    # --- 保存 Excel 部分 ---
    # 創建數據字典，第一列為 Time
    data = {"Time": time_data}

    # 添加每個通道的數據，標頭為 channel_ids
    for ch_num, ch_data in channel_data.items():
        if ch_num in channel_ids and ch_num != "time":  # 跳過時間通道
            data[channel_ids[ch_num]] = ch_data

    # 創建 DataFrame
    df = pd.DataFrame(data)
    df.to_excel(f'{excel_path}', index=False)

def plot_results(dynamic_out_files,busdata,excel_path, jpg_file_path):
    # chnfobj = dyntools.CHNF(dynamic_out_files)
    # short_title, chanid, chandata = chnfobj.get_data()
    # print('short_title --> ',short_title)
    # print('chanid -->',len(chanid))
    # t = chandata['time']
    time_data, channel_data, channel_ids = read_out_file(dynamic_out_files)
    plot_channels(time_data, channel_data, channel_ids, busdata, jpg_file_path)
    # excel_data = {"time":t}  

    # color = ['green','red','blue']
    # for i in range(1,len(chanid)):
    #     excel_data[chanid[i]] = chandata[i] 
    #     plt.plot(t,chandata[i],linestyle='-', linewidth=1, color=color[i-1],label=chanid[i])
    # # plt.plot(t,value2,linestyle='-', linewidth=1, color='red',label=chanid[2])
    # # plt.plot(t,value3,linestyle='-', linewidth=1, color='blue',label=chanid[3])
    datatoexcel(time_data, channel_data, channel_ids, excel_path)
 
    

    # plt.grid(linestyle='--', color='grey',linewidth=0.5)
    # plt.xlabel("Time")
    # plt.ylabel("Voltage")
    # plt.legend()
    # fig = plt.gcf()
    # plt.savefig(jpg_file_path,dpi=fig.dpi,facecolor='0.8')    

def whatfunction(psspycommand, laod_type):

    if psspycommand["function"]=='purgmac':
        parameter1 = psspycommand["data"][1]
        print(parameter1)
        print(type(parameter1))
        parameter2 = psspycommand["data"][2].split('\n')[0]
        # psspy.purgmac(int(parameter1),parameter2)
        return f"psspy.purgmac({parameter1},{parameter2})"

    elif psspycommand["function"]=='shunt_data':
        parameter1 = psspycommand["data"][1]
        parameter2 = psspycommand["data"][2]
        if laod_type=="P":
            parameter3 = 1
        elif laod_type=="L":
            parameter3 = 0
        else:
            parameter3 = psspycommand["data"][3]    
        # if psspycommand["data"][3] ==  '':
        #     parameter3 = 1
        # else:
        #     parameter4 = psspycommand["data"][3]    

        if psspycommand["data"][4] ==  '': 
            parameter4 = 0.0
        else:
            parameter4 = psspycommand["data"][4]    

        if psspycommand["data"][5] ==  '':     
            parameter5 = 0.0
        else:
            parameter4 = psspycommand["data"][5]
        # psspy.shunt_data(int(parameter1),parameter2,parameter3,[float(parameter4),parameter5])    
        return f"psspy.shunt_data({parameter1},{parameter2},{parameter3},[{parameter4},{parameter5}])"

    else:
        return None
    


def import_cogenfile(userName,file_path):
    import logging       
    from Log.LogConfig import Setlog   

    logger_idv_to_psspy = Setlog(logfolder= f'Log/{userName}/convert_psspy_Log/', level=logging.INFO,logger_name='convert_psspy_Log')
    
    with open(file_path, 'r', encoding='ansi') as file:
        content = file.readlines()
    # print(content)

    processed_lines = []
    for line in content:
        # 如果行不是以@!開頭
        if not line.strip().startswith('@!'):
            # 替換BAT_XXXX(oo, yy)為psspy.XXXX(oo, yy)
            if line.strip().startswith('BAT_'):                
                parts = line.split('(')
                # print(parts)
                parts = line.split(',')
                
                # func_name = 'psspy.' + parts[0][4:].lower()  # 去掉BAT_

                psspycommand={  'function':parts[0][4:].lower()
                                ,'data':parts}
                            
                function_string = whatfunction(psspycommand = psspycommand)

def dynamic(savfilename,savfileFolder ,resultdir, username,parameter,logger):
    #因為直接手動key psse的function和用python function解析idv後匯入結果會不一樣
    # resultdir = f"{userfolder}/Dynamic/{savfilename}"
    os.makedirs(f"pssefunctionsrc/src/temp/{username}",exist_ok=True)

    # shutil.copytree("web/src/pssefunction/Config", "web/src/pssefunction/temp/Config", symlinks=False, ignore=None)
    

    
    cont=f'''
# -*- coding: utf-8 -*-   


import sys, os
import configparser
import sys
print('現在位置-->',os.getcwd())


import numpy as np


try:    
    pssepy_PATH = os.environ.get('PSSE') 
    sys.path.append(pssepy_PATH)     
    import psse35
    # psse35.set_minor(3)
    import psspy
    psspy.psseinit()
    # import pssexcel
    import argparse
    import logging
except Exception as error: 
    print('error')
   
    raise ImportError(error)    


  
os.makedirs('{resultdir}',exist_ok=True)





Source_rawFilename = f"{savfileFolder}/{savfilename}.sav"
print(Source_rawFilename)


psspy.case(r"%s" %Source_rawFilename)

a = psspy.fnsl([1,0,0,1,1,1,-1,0])#第一次    
b = psspy.fnsl([1,0,0,1,1,0,0,0])#第二次[1,0,0,1,1,0,0,0]
c = psspy.fnsl([1,0,0,1,1,0,0,0])
# convert
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])
# ORDR
psspy.ordr(0)
# FACT
psspy.fact()
psspy.fact()
# TYSL
psspy.tysl(0)
'''
    logger.info(parameter)
    with open(parameter["renewable_energy_69kV_file"], 'r', encoding='ansi') as file:
        content = file.readlines()
    print('content = ',content)
    print("================================================")
    processed_lines = []
    laod_type = savfilename[-1]
    logger.info('load_type = %s',laod_type)
    # psspy.case(r"%s" %"test_new.sav")
    for line in content:
        # 如果行不是以@!開頭
        if not line.strip().startswith('@!'):
            # 替換BAT_XXXX(oo, yy)為psspy.XXXX(oo, yy)
            if line.strip().startswith('BAT_'):                
                parts = line.split('(')
                
                parts = line.split(',')

                psspycommand={  'function':parts[0][4:].lower()
                                ,'data':parts}
                        
                function_string = whatfunction(psspycommand = psspycommand,laod_type=laod_type)
                cont = cont + f"\n{function_string}"

    with open(parameter["co_gen_file"], 'r', encoding='ansi') as file:
        content = file.readlines()
    print('content = ',content)
    print("================================================")
    processed_lines = []
    laod_type = savfilename[-1]
    logger.info('laod_type = %s',laod_type)
    # psspy.case(r"%s" %"test_new.sav")
    for line in content:
        # 如果行不是以@!開頭
        if not line.strip().startswith('@!'):
            # 替換BAT_XXXX(oo, yy)為psspy.XXXX(oo, yy)
            if line.strip().startswith('BAT_'):                
                parts = line.split('(')
                
                parts = line.split(',')

                psspycommand={  'function':parts[0][4:].lower()
                                ,'data':parts}
                        
                function_string = whatfunction(psspycommand = psspycommand,laod_type=laod_type)
                cont = cont + f"\n{function_string}"
    cont = cont+f"""\n
psspy.dyre_new([1,1,1,1],f'{parameter["dv_file"]}',f"{resultdir}/CC2",f"{resultdir}/CT2",
f"{resultdir}/CP2")
# 匯dll
psspy.addmodellibrary(f'{parameter["dll_file"]}')
# 調parameter
psspy.dynamics_solution_param_2([25,0,0,18807,7594,2461,1418,1],[1.000000,0.0001, 0.000333,0.033333,0.05,0.11667,1.000000,0.0005])
#建立out檔
psspy.change_channel_out_file(f"{resultdir}/{savfilename}")"""

# 選觀測bus

    for look_bus, look_bus_id in zip(parameter["selected_machine_busnumber"], parameter["selected_machine_busid"]):#[221,532,1077]
        
        
        # print(np.where(machinedata['num']==look_bus))
        # look_bus_id = machinedata['id'][np.where(machinedata['num']==look_bus)][0]
        cont = cont+f"\npsspy.machine_array_channel([-1,1,{look_bus}],'{look_bus_id}','')"



# 選觀測bus
# err1 = psspy.machine_array_channel([-1,1,221],"1","")
# err2 = psspy.machine_array_channel([-1,1,532],"2","")
# err3 = psspy.machine_array_channel([-1,1,1077],"1","")
    cont = cont+f"""\n      
# # initial、Run to 1.0 sec
psspy.strt_2([0,0],f"{resultdir}/{savfilename}.out")
psspy.run(0, {parameter['initial_time']},5,5,5)
# 對1500進行Bus fault
psspy.dist_3phase_bus_fault({parameter['dynamic_bus_fault_num']},0,1,0.0,[0.0,-0.2E+10])
# Run to 1.0667 sec
psspy.change_channel_out_file(f"{resultdir}/{savfilename}.out")
psspy.run(0, {parameter['bus_fault_time']},5,5,5)"""

    # cont = cont + f"\npsspy.dist_branch_trip({parameter['dynamic_bus_fault_num']},{parameter['selected_dynamic_trip_line_num'][0]},'{parameter['circuit_id_for_elected_dynamic_trip_line'][0]}')"
    
    for i in range(len(parameter['selected_dynamic_trip_line_num'])):
    # 對1500連接的某一條(1500-1650)做trip line
        cont = cont + f"\npsspy.dist_branch_trip({parameter['dynamic_bus_fault_num']},{parameter['selected_dynamic_trip_line_num'][i]},'{parameter['circuit_id_for_elected_dynamic_trip_line'][i]}')"

    cont = cont+f"""\n
# Run to 1.075 sec
psspy.change_channel_out_file(f"{resultdir}/{savfilename}.out")
psspy.run(0, {parameter['trip_line_time']},5,5,5)
# Clear fault
psspy.dist_clear_fault(1)
# Run to 15 sec
psspy.run(0, {parameter['clear_fault_time']},5,5,5)    
"""
    print(cont) 
    with open(f'pssefunctionsrc/src/temp/{username}/temp.py', 'w', encoding='utf-8') as file:
        file.write(cont)
    cmd = f'python  pssefunctionsrc/src/temp/{username}/temp.py'    
    r = subprocess.run(cmd,capture_output=True)
    if r.returncode == 0:
        
        
        logger.info('USER: %s ACTION: %s  MESSAGE: %s',
            username,   '執行暫態暫存檔', f'PSSE 暫態執行結果 \n輸出資料夾位置{resultdir}/{savfilename}.out')     
            # 將PSSE執行結果寫入log
        if os.path.exists(f"{resultdir}/dynamic_log_for_psse_result.txt"):
            os.remove(f"{resultdir}/dynamic_log_for_psse_result.txt")  
        writeFile(f"{resultdir}/dynamic_log_for_psse_result.txt", r.stdout)

        print(f"{resultdir}/{savfilename}.out")
        busdata = np.load(f"../Data/User/{username}/filter/PowerFlow/bus/bus_{savfilename}.npz")
        plot_results(dynamic_out_files=f"{resultdir}/{savfilename}.out"
                    ,busdata = busdata
                    ,excel_path=f"{resultdir}/{savfilename}.xlsx"
                    ,jpg_file_path=f"{resultdir}/{savfilename}.jpg")

        # os.remove(f'web/src/pssefunction/temp/{username}/temp.py')
        # print(r.stdout)
         
       
    else:
        error_message = r.stderr          
        # error_message = r.stderr.decode().strip()
        print(f"Error occurred: {error_message}")
        logger.error('USER: %s ACTION: %s 暫存檔內容: %s MESSAGE: %s ',
        username,   '執行暫態暫存檔',cont, f'error_message:{error_message}') 



def ParseConfig():
    parser = argparse.ArgumentParser(description="路徑")
   
    parser.add_argument('-savfilename', '--Sav_FileName', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-ResultDir', '--resultdir', default="User/621882/", type=str, help='使用者資料夾路徑')
    parser.add_argument('-username', '--User_Name', default='621882', type=str, help='使用者名稱')
    
    parser.add_argument('-savfileFolder', '--savfile_Folder', default="112P-11109", type=str, help='sav檔路徑')
    
    parser.add_argument('-dvfile', '--dv_file', default='User/621882', type=str, help='dv檔路徑')
    parser.add_argument('-dllfile', '--dll_file', default='User/621882', type=str, help='dll檔路徑')
    parser.add_argument('-cogenfile', '--co_gen_file', default='User/621882', type=str, help='gen檔路徑')
    parser.add_argument('-reenergy_69kV_file', '--renewable_energy_69kV_file', default='User/621882', type=str, help='69KV再生能源轉-L.idv檔路徑')
            
            
    parser.add_argument('-selectedMachineBusnum', '--selected_machine_busnumber', default="10",nargs='+', type=str, help='選bus')
    parser.add_argument('-selectedMachineId', '--selected_machine_busid', default="10",nargs='+', type=str, help='選bus')

    parser.add_argument('-dynamicBusFault', '--dynamic_bus_fault_num', default="10", type=int, help='使用者資料夾路徑')
    parser.add_argument('-dynamicTripLinenum', '--selected_dynamic_trip_line_num', default='10', nargs='+',type=str, help='使用者名稱')
    parser.add_argument('-circuit_id_of_trip_line', '--circuit_id_for_elected_dynamic_trip_line', default='10', nargs='+',type=str, help='使用者名稱')

    parser.add_argument('-initialtime', '--initial_time', default="10", type=str, help='initial_time')
    parser.add_argument('-busfaulttime', '--bus_fault_time', default="10", type=str, help='bus_fault_time')
    parser.add_argument('-triplinetime', '--trip_line_time', default='10',type=str, help='trip_line_time')
    parser.add_argument('-clearfaulttime', '--clear_fault_time', default='10',type=str, help='clear_fault_time')


    args = parser.parse_args()
    
    savfilename = args.Sav_FileName
    savfileFolder = args.savfile_Folder

    resultdir =   args.resultdir
    username = args.User_Name

    dvfile = args.dv_file
    dllfile = args.dll_file
    cogenfile = args.co_gen_file   
    renewable_energy69kVfile = args.renewable_energy_69kV_file

    selected_machine_busnumber = args.selected_machine_busnumber
    selected_machine_busid = args.selected_machine_busid

    selected_machine_busnumber = [int(x) for x in selected_machine_busnumber]

    dynamic_Bus_Fault_num = args.dynamic_bus_fault_num

    selected_dynamic_trip_line_num = args.selected_dynamic_trip_line_num 
    selected_dynamic_trip_line_num = [int(x) for x in selected_dynamic_trip_line_num]
    
    
    initial_time = args.initial_time
    bus_fault_time = args.bus_fault_time
    trip_line_time = args.trip_line_time
    clear_fault_time = args.clear_fault_time


    circuit_id_for_elected_dynamic_trip_line = args.circuit_id_for_elected_dynamic_trip_line


    Pssps_bsys_Function_Parameter = {
        "dv_file":dvfile,
        "dll_file":dllfile,
        "co_gen_file":cogenfile,
        "renewable_energy_69kV_file":renewable_energy69kVfile,

        "selected_machine_busnumber":selected_machine_busnumber,
        "selected_machine_busid":selected_machine_busid,
        "dynamic_bus_fault_num":dynamic_Bus_Fault_num,
        "selected_dynamic_trip_line_num":selected_dynamic_trip_line_num,    
        "circuit_id_for_elected_dynamic_trip_line":circuit_id_for_elected_dynamic_trip_line,
        
        "initial_time": initial_time,
        "bus_fault_time": bus_fault_time,
        "trip_line_time": trip_line_time,
        "clear_fault_time": clear_fault_time

    }    
    
    return  savfilename,savfileFolder, resultdir, username, Pssps_bsys_Function_Parameter


if __name__ == '__main__':
    from Log.LogConfig import Setlog 
        
    savfilename,savfileFolder, resultdir, username, Pssps_bsys_Function_Parameter = ParseConfig()
    logger = Setlog(logfolder= f'../Log/{username}/PSSELog/', level=logging.INFO,logger_name='dynamic')
    
        
    dynamic(  savfilename= savfilename
            , savfileFolder = savfileFolder
            , resultdir=resultdir
            , username = username
            , parameter=Pssps_bsys_Function_Parameter
            ,logger=logger)
 



