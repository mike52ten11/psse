import re
import os
import threading
import datetime
import logging
import numpy as np

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

from .Log.LogConfig import Setlog
from . import fileprocess
from .base.get_subline_num_name import create_subline_npz

class PowerFlowSubThread(threading.Thread):
    def __init__(self, busnumber: int, busname: str, savfile_name: str, 
                 user: str, powerflow_folder: str, source_Folder: str, 
                 target_Folder: str, contxt: str, return_value: List[Dict], log_dir: str, systemlog: logging.Logger):
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
        self.lock = threading.Lock()  # 用于同步写入 return_value
        self.systemlog = systemlog

    def run(self):
        try:
            # 构建命令参数
            args = (f" --Sav_File {self.savfile_name}"
                    f" --User_name {self.user}"
                    f" --powerflow_Folder {self.powerflow_folder}"
                    f" --source_Folder {self.source_Folder}"
                    f" --target_Folder {self.target_Folder}"
                    f" --busnumber {self.busnumber}")

            cmd = Run_pyfile_by_execmd(
                python_location='python',
                pyfile='webinterface/src/Powerflow_of_subline_161n1.py',
                args=args
            )

            result = fileprocess.execCmd(cmd)

            # 使用 Lock 来确保 return_value 的写入是线程安全的
            with self.lock:
                if not result["error"]:
                    # 建立日志目录
                    os.makedirs(self.log_dir, exist_ok=True)

                    # 写入日志文件
                    log_file = f'{self.log_dir}limit_{self.busnumber}_{self.busname}.txt'
                    fileprocess.writeFile(log_file, result["return_value"])
                    print(f"{self.target_Folder}/{self.savfile_name}_{self.busnumber}.acc")
                    if os.path.exists(f"{self.target_Folder}/{self.busnumber}.acc"):
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
                    self.systemlog.info(result["backend_message"])
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

def run_powerflow_threads(busnum: List[int], busname: List[str], 
                         savfile_name: str, user: str, powerflow_folder: str,
                         source_Folder: str, target_Folder: str, contxt: str, log_dir: str, systemlog: logging.Logger) -> List[Dict]:
    return_value = []
    threads = []

    # 使用线程池来管理线程
    with ThreadPoolExecutor(max_workers=5) as executor:  # 根据需要调整 max_workers
        futures = []
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
                log_dir=log_dir,
                systemlog=systemlog
            )
            threads.append(thread)
            futures.append(executor.submit(thread.run))

        # 等待所有线程完成
        for future in futures:
            future.result()

    return return_value

def Run_pyfile_by_execmd(python_location: str, pyfile: str, args: str) -> str:
    return f"{python_location} {pyfile} {args}"

def find_subline_in_busname(cmdline_messages: str, filtervalue: Dict) -> List[int]:
    patternlist = [r'分', r'A', r'B']
    other_conditionlist = [r'1', r'2']
    busnum = []
    busname = []
    for busnumindex, busnameindex in zip(filtervalue["busnum"], filtervalue['busname']):
        if (busnumindex > 7269 or busnumindex == 7269) and (busnumindex < 7999 or busnumindex == 7999):
            for other_condition in other_conditionlist:
                if re.search(other_condition, busnameindex):
                    busnum.append(busnumindex)
                    busname.append(busnameindex)
                    break
        else:
            for pattern in patternlist:
                if re.search(pattern, busnameindex):
                    busnum.append(busnumindex)
                    busname.append(busnameindex)
                    break

    return busnum, busname

def match_Powerflow_of_subline_output(content: str) -> str:
    start_index = content.find('X----------- FROM BUS ------------X X------------ TO BUS -------------X')
    if start_index != -1:
        end_index = content.find('Output completed', start_index)
        if end_index != -1:
            target_content = content[start_index:end_index]
            return target_content
        else:
            return "未找到 'Output completed' 字串"
    else:
        return "未找到 'X----------- FROM BUS ------------X X------------ TO BUS -------------X' 字串"



def Run_Powerflow_of_subline(source_Folder: str,
                             powerflow_folder: str,
                             user: str,
                             Sav_File: List[str],
                             zone_num: List[int],
                             area_num: List[int],
                             maxbasekv: int,
                             minbasekv: int,
                             confile_type: str) -> Dict:
    today = datetime.date.today()
    logger_powerflow_subline = Setlog(
        logfolder=f"../Log/{user}/System/Powerflow_Subline_Log/",
        level=logging.INFO,
        logger_name=f'Powerflow_Subline_Log_{today}'
    )

    return_value = []
    iferror = 0

    for savfile in Sav_File:
        savfile_name = savfile.split('.')[0]
        area_and_zone = f"area={'+'.join(map(str, area_num))},zone={'+'.join(map(str, zone_num))}"
        target_Folder = (f"../Data/User/{user}/PowerFlowSub/{savfile_name}/161KV_N-1/close/"
                         f"{area_and_zone}")
        os.makedirs(target_Folder, exist_ok=True)

        create_subline_npz(
            target=target_Folder,
            zonenum=zone_num,
            areanum=area_num,
            minbasekv=minbasekv,
            maxbasekv=maxbasekv,
            filterfile=f'../Data/User/AnonymousUser/filter/PowerFlow/bus/bus_{savfile_name}.npz'
        )

        myArch = np.load(f"{target_Folder}/分歧線的BusName與BusNum.npz")
        busnum = myArch['busnum']
        busname = myArch['busname']

        if len(busnum) > 0:
            results = run_powerflow_threads(
                busnum=busnum,
                busname=busname,
                savfile_name=savfile_name,
                user=user,
                powerflow_folder=f"{powerflow_folder}/{savfile_name}/{confile_type}/{area_and_zone}",
                source_Folder=source_Folder,
                target_Folder=target_Folder,
                contxt=f"{savfile_name}:",
                log_dir=f'{target_Folder}/log/',
                systemlog=logger_powerflow_subline
            )
            return_value.extend(results)
        else:
            logger_powerflow_subline.info(f'PowerFlow-{savfile} 沒有分歧')
            return_value.append([{"content": f'PowerFlow-{savfile}  沒有分歧', "errorcode": 0}])

    bus_dict = {"error": iferror, "which_log": "Powerflow_Subline_Log", "return_value": return_value}
    return bus_dict
