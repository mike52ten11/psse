

import os

import numpy as np

import re
import logging

from .Log.LogConfig import Setlog
from . import fileprocess
from .base.check_encoding_type_from_psse import check_encoding_type


def run_pyfile_by_execmd(python_location,pyfile,args):

    return f"{python_location} {pyfile} {args}"



def RUN_dynamic(username
                    ,resultdir
                    ,savfile_Folder
                    ,savfilename
                    ,dv_file
                    ,dll_file
                    ,co_gen_file
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

    selected_machine_busnumber = ' '.join(selected_machine_busnumber) 
    selected_machine_busid = ' '.join(selected_machine_busid)
    
    args =  f" --User_Name {username}"\
            f" --resultdir {resultdir}"\
            f" --savfile_Folder {savfile_Folder}"\
            f" --Sav_FileName {savfilename}"\
            f" --dv_file {dv_file}"\
            f" --dll_file {dll_file}"\
            f" --co_gen_file {co_gen_file}"\
            f" --selected_machine_busnumber {selected_machine_busnumber}"\
            f" --selected_machine_busid {selected_machine_busid}"\
            f" --dynamic_bus_fault_num {dynamic_bus_fault_num}"\
            f" --selected_dynamic_trip_line_num {selected_dynamic_trip_line_num}"\
            f" --circuit_id_for_elected_dynamic_trip_line {circuit_id_for_elected_dynamic_trip_line}"\
            f" --initial_time {initial_time}"\
            f" --bus_fault_time {bus_fault_time}"\
            f" --trip_line_time {trip_line_time}"\
            f" --clear_fault_time {clear_fault_time}"
    # print(args)
    cmd = run_pyfile_by_execmd(python_location='python'
                                ,pyfile='pssefunctionsrc/src/Dynamic.py'
                                ,args=args)    
    print(cmd)
    result = fileprocess.execCmd(cmd)
    # print('result -- >',result)
    if result['error']:
        return {"error":1,"return_value":f'{savfilename} 執行失敗'}
    else:   
        return {"error":0,"return_value":f'{savfilename} 執行成功'}




  
