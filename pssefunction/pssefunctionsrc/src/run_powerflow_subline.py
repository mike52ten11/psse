import re
import os

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
                 target_Folder: str, zonenum: str, return_value: List[Dict]):
        super().__init__()
        self.busnumber = busnumber
        self.busname = busname
        self.savfile_name = savfile_name
        self.user = user
        self.powerflow_folder = powerflow_folder
        self.source_Folder = source_Folder
        self.target_Folder = target_Folder
        self.zonenum = zonenum
        self.return_value = return_value
        self.lock = threading.Lock()  # 用於同步寫入 return_value

    def run(self):
        try:
            # 構建命令參數
            args = (f" --Sav_File {self.savfile_name}"
                   f" --User_name {self.user}"
                   f" --powerflow_Folder {self.powerflow_folder}"
                   f" --source_Folder {self.source_Folder}"
                   f" --target_Folder {self.target_Folder}/close/{self.zonenum}"
                   f" --busnumber {self.busnumber}")

            cmd = Run_pyfile_by_execmd(
                python_location='python',
                pyfile='pssefunctionsrc/src/Powerflow_of_subline.py',
                args=args
            )

            print('看limit\n', cmd)
            result = fileprocess.execCmd(cmd)

            # 使用 Lock 來確保 return_value 的寫入是執行緒安全的
            with self.lock:
                if not result["error"]:
                    # 建立日誌目錄
                    log_dir = f'../Data/User/{self.user}/PowerFlowSub/{self.savfile_name}/close/{self.zonenum}/log/'
                    os.makedirs(log_dir, exist_ok=True)

                    # 寫入日誌檔案
                    log_file = f'{log_dir}limit_{self.busnumber}_{self.busname}.txt'
                    sublogfile = fileprocess.writeFile(log_file, result["return_value"])
                    print(sublogfile)

                    self.return_value.append({
                        "content": f"{self.savfile_name}: Zone = {self.zonenum} ---關{self.busnumber}_{self.busname}完成:已產出{self.busnumber}.acc",
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
                         source_Folder: str, target_Folder: str, zonenum: str) -> List[Dict]:
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
            zonenum=zonenum,
            return_value=return_value
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
    busnum = []
    busname = []
    for pattern in patternlist:
        # pattern = r'分'
        for busnumindex, busnameindex in zip(filtervalue["busnum"],filtervalue['busname']):
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
            

def Run_Powerflow_of_subline(source_Folder,powerflow_folder,user,Sav_File,zone_num,maxbasekv,minbasekv,):
    print(zone_num)
    # zone_num = [11]
    '''
        Return:
            Mis = {"error":0,"return_value":return_value}
            其中，return_value = {"content":"xxx.sav: 執行成功","errorcode": 0 }
            Mis = {"error":1,'which_log':"....","return_value":return_value}
            其中，return_value = {"content":"xxx.sav: 執行失敗","errorcode": 1 }
    ''' 

    logger_powerflow_subline = Setlog(logfolder= f"Log/{user}/Powerflow_Subline_Log/", level=logging.INFO,logger_name='Powerflow_Subline_Log')
    


    return_value = []
    iferror = 0
    for savfile in Sav_File:
        print('zone_num -->' ,zone_num,'\n')
        for zonenum in zone_num: 
            savfile_name = savfile.split('.')[0]
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
                                        ,pyfile='pssefunctionsrc/src/filter_subline.py'
                                        ,args=args)


            print("找分歧\n",cmd)
            result = fileprocess.execCmd(cmd)
            # print('result1 >> ',result)
            if not result["error"]:

                result_test = result["return_value"].decode("mbcs",errors='ignore').split('\n')
                # print("找分歧",result_test)            
                
                

                myArch = np.load(f"../Data/User/{user}/PowerFlowSub/"\
                                f"{savfile_name}/close/{zonenum}/"\
                                f"分歧線的BusName與BusNum.npz")
                busnum, busname = find_subline_in_busname(cmdline_messages=result_test
                                                        ,filtervalue=myArch)
                print('zonenum -->' ,zonenum,'\n')                                        
                print('busnum -- >',busnum,'busname -- >',busname)                                        
                if  busnum==[]:
                    print('沒有分歧')    
                    return_value.append({"content":f'PowerFlow-{savfile} Zone: {zonenum} 沒有分歧',"errorcode": 0})               
                    # break
                # print(zip(busnum,busname))
                # fileprocess.writeFile(f'User/{user}/PowerFlowSub/{savfile_name}/close/{area_num}/分歧線的BusName與BusNum.txt', result["return_value"])

                results = run_powerflow_threads(    busnum=busnum,
                            busname=busname,
                            savfile_name=savfile_name,
                            user=user,
                            powerflow_folder=powerflow_folder,
                            source_Folder=source_Folder,
                            target_Folder=f"{target_Folder}/close/{zonenum}",
                            zonenum=zonenum)
                return_value.append(results)            
                # for busnumber, busname_of_sub  in  zip(busnum,busname):  
                #     print( busnumber, busname_of_sub)                                
                #     args =  f" --Sav_File {savfile_name}"\
                #             f" --User_name {user}"\
                #             f" --powerflow_Folder {powerflow_folder}"\
                #             f" --source_Folder {source_Folder}"\
                #             f" --target_Folder {target_Folder}/close/{zonenum}"\
                #             f" --busnumber {busnumber}"
                #     cmd = Run_pyfile_by_execmd(python_location='python'
                #                                     ,pyfile='pssefunctionsrc/src/Powerflow_of_subline.py'
                #                                     ,args=args)
                #     # cmd = cmd.split(' ') 
                #     print('看limit\n',cmd)                                           
                #     result = fileprocess.execCmd(cmd)
                    
                #     if not result["error"]:
                #         os.makedirs(f'../Data/User/{user}/PowerFlowSub/{savfile_name}/close/{zonenum}/log/', exist_ok=True)
                #         # print(result["return_value"].decode("mbcs",errors='ignore'))
                #         # sublogfile = fileprocess.writeFile(f'User/{user}/PowerFlowSub/{savfile_name}/close/{zonenum}/log/limit_{busnumber}_{busname_of_sub}.txt', result["return_value"].decode("mbcs",errors='ignore'))
                #         sublogfile = fileprocess.writeFile(f'../Data/User/{user}/PowerFlowSub/{savfile_name}/close/{zonenum}/log/limit_{busnumber}_{busname_of_sub}.txt', result["return_value"])
                #         print(sublogfile)
                #         return_value.append({"content":f"{savfile}: Zone = {zonenum} ---關{busnumber}_{busname_of_sub}完成:已產出{busnumber}.acc","errorcode": 0})

                #     else:
                #         return_value.append({"content":f"PowerFlow-{savfile}: 錯誤"})
                #         print('result ==>',result)
                #         logger_powerflow_subline.info(result["backend_message"])
                        
                #         return_value.append({"content": result["front_message"],"errorcode": 1})                   
                    
                          
  
            else:
                return_value.append([{"content":f"PowerFlow-{savfile}: 錯誤"}])
                iferror=1

    bus_dict = {"error":iferror,"which_log":"Powerflow_Subline_Log","return_value":return_value}
    return bus_dict




    print(cmd)
    
    result = fileprocess.execCmd(cmd)   
    logger_Filter_savefile_by_labeltype.info('%s %s的num和name取得成功\n',savfile_name,label_type) 
    return  1      
