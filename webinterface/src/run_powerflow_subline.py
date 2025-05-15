import re
import os
import datetime
import logging

import numpy as np

from .Log.LogConfig import Setlog
from . import fileprocess

import threading
from typing import List, Dict
import os

class PowerFlowSubThread(threading.Thread):
    def __init__(self, busnumber: int, busname: str, savfile_name: str, 
                 user: str, powerflow_folder: str, source_Folder: str, 
                 target_Folder: str, contxt: str, return_value: List[Dict],log_dir:str):
        super().__init__()
        self.busnumber = busnumber
        self.busname = busname
        self.savfile_name = savfile_name
        self.user = user
        self.powerflow_folder = powerflow_folder
        self.source_Folder = source_Folder
        self.target_Folder = target_Folder
        self.contxt = contxt
        self.log_dir = log_dir
        self.return_value = return_value
        self.lock = threading.Lock()  # 用於同步寫入 return_value

    def run(self):
        try:
            # 構建命令參數
            args = (f" --Sav_File {self.savfile_name}"
                   f" --User_name {self.user}"
                   f" --powerflow_Folder {self.powerflow_folder}"
                   f" --source_Folder {self.source_Folder}"
                   f" --target_Folder {self.target_Folder}"
                   f" --busnumber {self.busnumber}")

            cmd = Run_pyfile_by_execmd(
                python_location='python',
                pyfile='webinterface/src/Powerflow_of_subline.py',
                args=args
            )

            
            result = fileprocess.execCmd(cmd)

            # 使用 Lock 來確保 return_value 的寫入是執行緒安全的
            with self.lock:
                if not result["error"]:
                    # 建立日誌目錄
                    
                    os.makedirs(self.log_dir, exist_ok=True)

                    # 寫入日誌檔案
                    log_file = f'{self.log_dir}limit_{self.busnumber}_{self.busname}.txt'
                    sublogfile = fileprocess.writeFile(log_file, result["return_value"])
                    print(f"{self.target_Folder}/{self.savfile_name}_{self.busnumber}.acc")
                    if os.path.exists(f"{self.target_Folder}/{self.savfile_name}_{self.busnumber}.acc"):

                        self.return_value.append({
                            "content": f"{self.contxt} ---關{self.busnumber}_{self.busname}完成:已產出{self.busnumber}.acc",
                            "errorcode": 0
                        })
                    else:
                        self.return_value.append({
                            "content": f"{self.contxt} ---關{self.busnumber}_{self.busname}成功:psse 產生acc檔失敗，請下載log，未產出{self.busnumber}.acc",
                            "errorcode": 0
                        })                           
                else:
                    self.return_value.append({"content": f"PowerFlow-{self.savfile_name}: 錯誤"})
                    print('result ==>', result)
                    logger_powerflow_subline.info(result["backend_message"])
                    self.return_value.append({
                        "content": result["front_message"],
                        "errorcode": 1
                    })
        except Exception as e:
            with self.lock:
                self.return_value.append({
                    "content": f"執行緒錯誤: {str(e)}",
                    "errorcode": 1
                })
        # print('class裡的',self.return_value)            

def run_powerflow_threads(busnum: List[int], busname: List[str], 
                         savfile_name: str, user: str, powerflow_folder: str,
                         source_Folder: str, target_Folder: str, contxt: str, log_dir:str) -> List[Dict]:
    return_value = []
    threads = []

    # 創建並啟動所有執行緒
    for busnumber, busname_of_sub in zip(busnum, busname):
        thread = PowerFlowSubThread(
            busnumber=busnumber,
            busname=busname_of_sub,
            savfile_name=savfile_name,
            user=user,
            powerflow_folder=powerflow_folder,
            source_Folder=source_Folder,
            target_Folder=target_Folder,
            contxt=contxt,
            return_value=return_value,
            log_dir=log_dir
        )
        threads.append(thread)
        thread.start()
    print(thread)
    # 等待所有執行緒完成
    for thread in threads:
        thread.join()
    print("執行序的", return_value)
    return return_value

def Run_pyfile_by_execmd(python_location,pyfile,args):

    return f"{python_location} {pyfile} {args}"
    

def find_subline_in_busname(cmdline_messages,filtervalue):
    patternlist = [r'分',r'A',r'B']
    other_conditionlist = [r'1',r'2']
    busnum = []
    busname = []
    for busnumindex, busnameindex in zip(filtervalue["busnum"],filtervalue['busname']):

        if (busnum>7269 or busnum==7269) and (busnum<7999 or busnum==7999):
            for other_condition in other_conditionlist:
                if re.search(other_condition, busnameindex):
                    busnum.append(busnumindex)
                    busname.append(busnameindex)                
        else:
            for pattern in patternlist:
                if re.search(pattern, busnameindex):
                    busnum.append(busnumindex)
                    busname.append(busnameindex)
    
    return (busnum,busname)

def match_Powerflow_of_subline_output(content):
    # with open(r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\PowerFlowSub\112P\close\11\test.txt', 'r') as file:
    #     content = file.read()

    start_index = content.find('X----------- FROM BUS ------------X X------------ TO BUS -------------X')
    if start_index != -1:
        end_index = content.find('Output completed', start_index)
        if end_index != -1:
            target_content = content[start_index:end_index]
            print(start_index,end_index)
            return target_content
        else:
            return "未找到 'Output completed' 字串"
    else:
        return "未找到 'X----------- FROM BUS ------------X X------------ TO BUS -------------X' 字串"
        
def find_powerflow_subline_limit_flow(content):
    # pattern = r'X----------- FROM BUS ------------X X------------ TO BUS -------------X RATING SET 1 RATING SET 2 RATING SET 3\r\n BUS#-SCT X-- NAME --X BASKV AREA BUS#-SCT X-- NAME --X BASKV AREA CKT LOADING RATE1 PERCENT RATE2 PERCENT RATE3 PERCENT\r\n\r\n * NONE *\r\n\r\n'
    # match = re.search(pattern, content, re.DOTALL)
    start_index = content.find('\r\n\r\n') + 4
    end_index = content.find('\r\n\r\n', start_index)
    result = content[start_index:end_index]

    print(result)
    if result:
        
        return result
        
    else:
        return 0
            

def Run_Powerflow_of_subline(source_Folder
                                ,powerflow_folder
                                ,user
                                ,Sav_File
                                ,zone_num
                                ,area_num
                                ,maxbasekv
                                ,minbasekv
                                ,confile_type
                            ):
    print(zone_num)
    today = datetime.date.today()
    # zone_num = [11]
    '''
        Return:
            Mis = {"error":0,"return_value":return_value}
            其中，return_value = {"content":"xxx.sav: 執行成功","errorcode": 0 }
            Mis = {"error":1,'which_log':"....","return_value":return_value}
            其中，return_value = {"content":"xxx.sav: 執行失敗","errorcode": 1 }
    ''' 

    logger_powerflow_subline = Setlog(
                                logfolder = f"../Log/{user}/System/Powerflow_Subline_Log/"
                                , level = logging.INFO
                                , logger_name = f'Powerflow_Subline_Log_{today}')
    


    return_value = []
    iferror = 0
    for savfile in Sav_File:
        savfile_name = savfile.split('.')[0]
        print('areanum -->' ,area_num,'\n')
        for areanum in area_num:            
            target_Folder = f"../Data/User/{user}/PowerFlowSub/{savfile_name}"
            args =  f"--Label_type bus"\
                f" --Sav_File {savfile_name}"\
                f" --User_name {user}"\
                f" --source_Folder {source_Folder}"\
                f" --AreaNum {areanum}"\
                f" --MaxBaseKV {maxbasekv}"\
                f" --MinBaseKV {minbasekv}"

            #找分歧    
            cmd = Run_pyfile_by_execmd(python_location='python'
                                        ,pyfile='webinterface/src/filter_subline.py'
                                        ,args=args)

            print(cmd)
            logger_powerflow_subline.info(f"FUNCTION: webinterface/src/Run_Powerflow_of_subline，MESSAGE:找 {areanum} in {area_num}的所有bus ，PROCESS: {cmd}")
            result = fileprocess.execCmd(cmd)

            if result["error"]:
                return_value.append([{"content":f"PowerFlow-{savfile}: 錯誤"}])
                iferror=1                
                logger_powerflow_subline.error(f"FUNCTION: webinterface/src/Run_Powerflow_of_subline，MESSAGE:ERROR Ocurred: {result['return_value']} ，PROCESS: {cmd}")
             
  
            else:
                logger_powerflow_subline.info(f"FUNCTION: webinterface/src/Run_Powerflow_of_subline，MESSAGE:執行成功結果 ，PROCESS: {cmd}")
                result_test = result["return_value"].decode("ansi",errors='ignore').split('\n')

                myArch = np.load(f"../Data/User/{user}/PowerFlowSub/"\
                                f"{savfile_name}/close/Area_{areanum}/"\
                                f"分歧線的BusName與BusNum.npz")
                busnum, busname = find_subline_in_busname(cmdline_messages=result_test
                                                        ,filtervalue=myArch)
                                      
                if  busnum==[]:
                    print('沒有分歧')    
                    return_value.append([{"content":f'PowerFlow-{savfile} Zone: {zonenum} 沒有分歧',"errorcode": 0}])               
                else:
                    results = run_powerflow_threads(    busnum=busnum,
                                busname=busname,
                                savfile_name=savfile_name,
                                user=user,
                                powerflow_folder=powerflow_folder,
                                source_Folder=source_Folder,
                                target_Folder=f"{target_Folder}/close/Area_{areanum}",
                                contxt = f"{savfile_name}: Area = {areanum}",
                                log_dir = f'../Data/User/{user}/PowerFlowSub/{savfile_name}/close/Area_{areanum}/log/')
                    return_value.append(results)              
        for zonenum in zone_num: 
            
            target_Folder = f"../Data/User/{user}/PowerFlowSub/{savfile_name}"
            args =  f"--Label_type bus"\
                f" --Sav_File {savfile_name}"\
                f" --User_name {user}"\
                f" --source_Folder {source_Folder}"\
                f" --ZoneNum {zonenum}"\
                f" --MaxBaseKV {maxbasekv}"\
                f" --MinBaseKV {minbasekv}"

            #找分歧    
            cmd = Run_pyfile_by_execmd(python_location='python'
                                        ,pyfile='webinterface/src/filter_subline.py'
                                        ,args=args)

            print(cmd)
            logger_powerflow_subline.info(f"FUNCTION: webinterface/src/Run_Powerflow_of_subline，MESSAGE:找 {zonenum} in {zone_num}的所有bus ，PROCESS: {cmd}")
            result = fileprocess.execCmd(cmd)

            if result["error"]:
                return_value.append([{"content":f"PowerFlow-{savfile}: 錯誤"}])
                iferror=1                
                logger_powerflow_subline.error(f"FUNCTION: webinterface/src/Run_Powerflow_of_subline，MESSAGE:ERROR Ocurred: {result['return_value']} ，PROCESS: {cmd}")
             
  
            else:
                logger_powerflow_subline.info(f"FUNCTION: webinterface/src/Run_Powerflow_of_subline，MESSAGE:執行成功結果 ，PROCESS: {cmd}")
                result_test = result["return_value"].decode("ansi",errors='ignore').split('\n')

                myArch = np.load(f"../Data/User/{user}/PowerFlowSub/"\
                                f"{savfile_name}/close/Zone_{zonenum}/"\
                                f"分歧線的BusName與BusNum.npz")
                                
                if  maxbasekv==161.0 and confile_type=='N1':
                    busnum, busname = find_subline_in_busname(cmdline_messages=result_test
                                                            ,filtervalue=myArch)
                elif  maxbasekv==345.0 and confile_type=='N1':
                    busnum, busname = find_subline_in_busname(cmdline_messages=result_test
                                                            ,filtervalue=myArch) 
                else:
                    busnum, busname = find_subline_in_busname(cmdline_messages=result_test
                                                            ,filtervalue=myArch) 

                if  busnum==[]:
                    print('沒有分歧')    
                    return_value.append([{"content":f'PowerFlow-{savfile} Zone: {zonenum} 沒有分歧',"errorcode": 0}])               
                else:
                    results = run_powerflow_threads(    busnum=busnum,
                                busname=busname,
                                savfile_name=savfile_name,
                                user=user,
                                powerflow_folder=powerflow_folder,
                                source_Folder=source_Folder,
                                target_Folder=f"{target_Folder}/close/Zone_{zonenum}",
                                contxt = f"{savfile_name}: Zone = {zonenum}",
                                log_dir = f'../Data/User/{user}/PowerFlowSub/{savfile_name}/close/Zone_{zonenum}/log/')
                    return_value.append(results)   

    bus_dict = {"error":iferror,"which_log":"Powerflow_Subline_Log","return_value":return_value}
    return bus_dict




    print(cmd)
    
    result = fileprocess.execCmd(cmd)   
    logger_Filter_savefile_by_labeltype.info('%s %s的num和name取得成功\n',savfile_name,label_type) 
    return  1      
