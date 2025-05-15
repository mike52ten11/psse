

import os
from pathlib import Path
import numpy as np

import re
import logging
from icecream import ic
ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='debug > ')

from .Log.LogConfig import Setlog
from . import fileprocess
from .base.check_encoding_type_from_psse import check_encoding_type
from .base.plot_outfile import read_out_file, plot_channels, datatoexcel

def run_pyfile_by_execmd(python_location,pyfile,args):

    return f"{python_location} {pyfile} {args}"



def RUN_dynamic(username
                    ,resultdir
                    ,savfile_Folder
                    ,savfilename
                    ,dv_file
                    ,dll_file
                    ,co_gen_file
                    ,renewable_energy_69kV_file
                    ,selected_machine_busnumber
                    ,selected_machine_busid
                    ,dynamic_bus_fault_num
                    ,selected_dynamic_trip_line_num
                    ,circuit_id_for_elected_dynamic_trip_line
                    ,initial_time
                    ,bus_fault_time
                    ,trip_line_time
                    ,clear_fault_time                    
                ):

    # selected_machine_busnumber = ' '.join(selected_machine_busnumber) 
    # selected_machine_busid = ' '.join(selected_machine_busid)


    # 獲取當前工作目錄的上一層目錄
    BASE_DIR = os.path.dirname(os.getcwd()).replace('\\', '/')
    ic('BASE_DIR -- >',BASE_DIR)

    # 將相對路徑轉為絕對路徑
    resultdir = f"{BASE_DIR}{resultdir.split('..')[-1]}"
    savfile_Folder = f"{BASE_DIR}{savfile_Folder.split('..')[-1]}"
    dv_file = f"{BASE_DIR}{dv_file.split('..')[-1]}"
    dll_file = f"{BASE_DIR}{dll_file.split('..')[-1]}"
    co_gen_file = f"{BASE_DIR}{co_gen_file.split('..')[-1]}"
    renewable_energy_69kV_file = f"{BASE_DIR}{renewable_energy_69kV_file.split('..')[-1]}"

    selected_machine_busnumber = [int(x) for x in selected_machine_busnumber]
    selected_dynamic_trip_line_num = int(selected_dynamic_trip_line_num)

    parameter = {
        "dv_file":dv_file,
        "dll_file":dll_file,
        "co_gen_file":co_gen_file,
        "renewable_energy_69kV_file":renewable_energy_69kV_file,

        "selected_machine_busnumber":selected_machine_busnumber,
        "selected_machine_busid":selected_machine_busid,
        "dynamic_bus_fault_num":dynamic_bus_fault_num,
        "selected_dynamic_trip_line_num":selected_dynamic_trip_line_num,    
        "circuit_id_for_elected_dynamic_trip_line":circuit_id_for_elected_dynamic_trip_line,
        
        "initial_time": float(initial_time),
        "bus_fault_time": float(bus_fault_time),
        "trip_line_time": float(trip_line_time),
        "clear_fault_time": float(clear_fault_time)

    }
    ic(parameter)
    idvfile, outfilename = create_dynamic_idvfile(savfilename, savfile_Folder ,resultdir, username, parameter)
    # args =  f" --User_Name {username}"\
    #         f" --resultdir {resultdir}"\
    #         f" --savfile_Folder {savfile_Folder}"\
    #         f" --Sav_FileName {savfilename}"\
    #         f" --dv_file {dv_file}"\
    #         f" --dll_file {dll_file}"\
    #         f" --co_gen_file {co_gen_file}"\
    #         f" --renewable_energy_69kV_file {renewable_energy_69kV_file}"\
    #         f" --selected_machine_busnumber {selected_machine_busnumber}"\
    #         f" --selected_machine_busid {selected_machine_busid}"\
    #         f" --dynamic_bus_fault_num {dynamic_bus_fault_num}"\
    #         f" --selected_dynamic_trip_line_num {selected_dynamic_trip_line_num}"\
    #         f" --circuit_id_for_elected_dynamic_trip_line {circuit_id_for_elected_dynamic_trip_line}"\
    #         f" --initial_time {initial_time}"\
    #         f" --bus_fault_time {bus_fault_time}"\
    #         f" --trip_line_time {trip_line_time}"\
    #         f" --clear_fault_time {clear_fault_time}"
    # print(args)
    args = f" --idv_file {idvfile}"
    cmd = run_pyfile_by_execmd(python_location='python'
                                ,pyfile='webinterface/src/run_idvfile.py'
                                ,args=args)    
    print(cmd)
    result = fileprocess.execCmd(cmd)
    # ic('result -- >',result)
    if result['error']:
        return {"error":1,"return_value":f'{savfilename} 執行失敗 Error:{result["return_value"]["backend_message"]}'}
    else:   
        time_data, channel_data, channel_ids = read_out_file(f"{outfilename}.out")
        if time_data is not None:
            busdata = np.load(f"../Data/User/{username}/filter/PowerFlow/bus/bus_{savfilename}.npz")
            try:
                plot_channels(time_data, channel_data, channel_ids, busdata, f"{outfilename}.jpg")
            except Exception as e:
                return {"error":1,"return_value":f'{savfilename} 執行成功但畫圖失敗，畫圖程式有錯誤:錯誤訊息-->{e}'}
            try:
                datatoexcel(time_data, channel_data, channel_ids, f"{outfilename}.xlsx")
            except Exception as e:
                return {"error":1,"return_value":f'{savfilename} 執行成功，畫圖成功，但數據保存成excel失敗，保存為xlsx的程式有錯誤:錯誤訊息-->{e}'}
            
            with open(f'{resultdir}/dynamic_log_for_psse_result.txt', 'w', encoding='ansi') as file:
                file.write(result["return_value"].decode('ansi', errors='ignore')) 

            return {"error":0,"return_value":f'{savfilename} 執行、畫圖、保存數據 皆成功'}
        else:
            return {"error":1,"return_value":f'{savfilename} 執行成功，但out檔無法讀取導致畫圖失敗'}        
        



def create_dynamic_idvfile(savfilename, savfileFolder ,resultdir, username, parameter):
    tempdir = f"TempFile/dynamic/{username}"
    os.makedirs(tempdir,exist_ok=True)
    os.makedirs(f'{resultdir}',exist_ok=True)
    source_savfile = f"{savfileFolder}/{savfilename}.sav"  

    cont=f'''BAT_CASE,'{source_savfile}'\n'''


    files = fileprocess.How_many_rawfile(f"{resultdir}" , fileextension = r'.out')
    ic(len(files))
    if len(files)>0:
        outfilename = f"{resultdir}/{savfilename}({len(files)})"
    else:
        outfilename = f"{resultdir}/{savfilename}"

    ic(outfilename)
    #匯入69kV再生能源idv
    with open(parameter["renewable_energy_69kV_file"], 'r', encoding='utf-8') as file:
        content = file.readlines()
    content = '\n'.join(content)    
    cont = f"{cont}{content}\n"
    #匯入con-gen檔
    with open(parameter["co_gen_file"], 'r', encoding='ansi') as file:
        content = file.readlines()
    content = '\n'.join(content)    
    cont = f"{cont}{content}\n"
    #跑 powerflow
    cont =  f"""{cont}BAT_FNSL,1,0,0,1,1,1,-1,0\n
BAT_FNSL,1,0,0,1,1,0,0,0\n
BAT_FNSL,1,0,0,1,1,0,0,0\n
"""
    #跑 convert
    cont = f"""{cont}BAT_CONG,0\n
BAT_CONL,0,1,1,0,0, 100.0,0.0,0.0, 100.0\n
BAT_CONL,0,1,2,0,0, 100.0,0.0,0.0, 100.0\n
BAT_CONL,0,1,3,0,0, 100.0,0.0,0.0, 100.0\n
"""
    #ORDR
    cont =f"""{cont}BAT_ORDR,0\n"""
    #FACT
    cont =f"""{cont}BAT_FACT\n
BAT_FACT,;\n
"""
    #TYSL
    cont = f"""{cont}BAT_TYSL,0\n"""
    #匯dyr、建cc、ct、cp
    cont = f"""{cont}BAT_DYRE_NEW,1,1,1,1,'{parameter["dv_file"]}','{resultdir}/CC2','{resultdir}/CT2','{resultdir}/CP2'\n"""
    #匯dll
    cont = f"""{cont}BAT_ADDMODELLIBRARY,'{parameter["dll_file"]}'\n"""
    #調parameter
    cont = f"""{cont}BAT_DYNAMICS_SOLUTION_PARAM_2,,,,,,,,,,, 0.000333,,,,,,;\n"""
    #建立out檔
    cont = f"""{cont}BAT_CHANGE_CHANNEL_OUT_FILE,'{outfilename}'\n"""
    #設machine angle
    cont = f"""{cont}BAT_SET_RELANG,1,-1,' '\n"""
    #選觀測bus(選擇machine bus)
    for look_bus, look_bus_id in zip(parameter["selected_machine_busnumber"], parameter["selected_machine_busid"]):#[221,532,1077]

        cont = f"{cont}BAT_MACHINE_ARRAY_CHANNEL,-1,1,{look_bus},'{look_bus_id}',''\n"
    #執行dynamic
    cont = f"""{cont}BAT_STRT_2,0,0,'{outfilename}.out'\n"""
    #跑到1sec (initial time固定1s)   
    cont = f"""{cont}BAT_RUN,0, 1.0,100,5,5\n"""  
    #對 parameter['dynamic_bus_fault_num'] 進行bus fault (選擇bus fault)
    cont = f"""{cont}BAT_DIST_3PHASE_BUS_FAULT,{parameter['dynamic_bus_fault_num']},0,1, 345.0,0.0,-0.2E+10\n"""
    # 跑到1.0667sec (trip line time)(對應到parameter['bus_fault_time'])
    cont = f"""{cont}BAT_RUN,0, {parameter['bus_fault_time']},100,5,5\n"""
    # 選trip line (選擇trip line)
    # for i in range(len(parameter['selected_dynamic_trip_line_num'])):
        
    cont = f"""{cont}BAT_DIST_BRANCH_TRIP,{parameter['dynamic_bus_fault_num']},{parameter['selected_dynamic_trip_line_num']},'{parameter['circuit_id_for_elected_dynamic_trip_line']}'\n"""
    # 跑到1.0833sec (clear fault time)(對應到parameter['trip_line_time'])
    cont = f"""{cont}BAT_RUN,0, {parameter['trip_line_time']},100,5,5\n"""
    cont = f"""{cont}BAT_DIST_CLEAR_FAULT,1\n"""    
    
    #跑到10sec (模擬時間)
    cont = f"""{cont}BAT_RUN,0, {parameter['clear_fault_time']},100,5,5\n"""   
    # print(f'{cont}'.format('ansi')) 
    with open(f'{tempdir}/dynamic_temp.idv', 'w', encoding='ansi') as file:
        file.write(cont)

  
    return f'{tempdir}/dynamic_temp.idv', outfilename