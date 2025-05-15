

import os

import numpy as np

import re
import logging

from .Log.LogConfig import Setlog
from . import fileprocess
from .base.check_encoding_type_from_psse import check_encoding_type
from .convert.convert_program import convert_rel_to_excelFile

def run_pyfile_by_execmd(python_location,pyfile,args):

    return f"{python_location} {pyfile} {args}"



def RUN_ErrorCircuit(username
                    ,savfiledir
                    ,savefiles
                    ,errorcircuitdir
                    ,area
                    ,zone
                    ,owner
                    ,minbasekv,maxbasekv
                    ,logpath):


    # UserFolder = f"User/{username}/"  

    mis = RUN_ErrorCircuit_for_many_savFile(username = username
                                            ,savfiledir=savfiledir
                                            ,savefiles=savefiles
                                            ,errorcircuitdir=errorcircuitdir
                                            ,area=area
                                            ,zone=zone
                                            ,owner=owner
                                            ,minbasekv=minbasekv,maxbasekv=maxbasekv
                                            ,logpath=logpath)

    return mis

def errorcircuit_result_process(result: dict,
                              errorcircuitdir: str,  # 遵循小寫命名規則
                              savfilename: str,
                              return_value: int,
                              logger_ErrorCircuitFunction: logging.Logger):
        # logfilepath = f"{user_folder}ErrorCircuit/{savfile}/{savfile}_log.txt"
        logfilepath = f"{errorcircuitdir}/{savfilename}/{savfilename}.txt"
        encoding_type = check_encoding_type(result['return_value'])
        if result.get("error"):
            # run_pyfile_by_execmd有 ERROR 的block'
            # RUN_ErrorCircuit_for_many_savFile_Exception_error = 1 
            return_value.append({"content":f"{savfilename}.sav: 執行失敗","errorcode": 1 })

            Mis = {"error":1,'which_log':"ErrorCircuitFunction_log","return_value":return_value}
            logger_ErrorCircuitFunction.error('FUNCTION: %s MESSAGE: %s',result["function"],result["backend_message"])   
            return {
                    'need_break':1
                    ,"return_value":return_value
                    ,"break_from_where":'run_pyfile_by_execmd有 ERROR 的block'
                    }

        else:
            # '找Psse回傳資料裡有沒有 ERROR 的block'
            pat1 = 'ERROR: (.*)'
            try:
                mismatch = re.search(pat1, result["return_value"].decode(encoding_type))
            except:
                mismatch = re.search(pat1, result["return_value"].decode("ISO-8859-1"))     
            print(mismatch)
            if mismatch:
                mismatch = mismatch.group(1)    
            if mismatch is not None:
                # RUN_ErrorCircuit_for_many_savFile_Exception_error = 1

                Function_Return = fileprocess.writeFile(logfilepath, result["return_value"]) 
                if Function_Return["error"]:
                    logger_ErrorCircuitFunction.error(Function_Return["return_value"]["backend_message"])
                    return_value.append({"content":f"{savfilename}.sav: psse執行成功，回傳error，寫入log失敗","errorcode": 1 })                    
                else:
                    return_value.append({"content":f"{savfilename}.sav: psse執行成功，回傳error，請下載log","errorcode": 1 })
                return {
                        'need_break':1
                        ,"return_value":return_value
                        ,"break_from_where":'psse執行成功，回傳error 的block'
                        }
            else:     

                Function_Return = fileprocess.writeFile(logfilepath, result["return_value"])    

                if Function_Return["error"]:
                    # RUN_ErrorCircuit_for_many_savFile_Exception_error = 1
                    logger_ErrorCircuitFunction.error(Function_Return["return_value"]["backend_message"])
                    return_value.append({"content":f"{savfilename}.sav: psse執行成功，寫入log失敗，{Function_Return['return_value']['front_message']}","errorcode": 1 })
                    
                else:
                    return_value.append({"content":f"{savfilename}.sav: 執行成功","errorcode": 0 })
            
                return_from_convert = convert_rel_to_excelFile(relfile = f"{errorcircuitdir}/{savfilename}/{savfilename}.rel"
                                                            ,outputpath = f"{errorcircuitdir}/{savfilename}/Excel/{savfilename}.csv")
                if return_from_convert["error"]:
                    return_value.append({"content":f"{savfilename}.rel: 轉csv檔失敗","errorcode": 0 })
                else:
                    return_value.append({"content":f"{savfilename}.rel: 轉csv檔成功","errorcode": 0 })
                return {
                    'need_break':0
                    ,"return_value":return_value
                    ,"break_from_where":'psse執行成功的block'
                    }                   






def RUN_ErrorCircuit_for_many_savFile(  username
                                        ,savfiledir
                                        ,savefiles
                                        ,errorcircuitdir
                                        ,area
                                        ,zone
                                        ,owner
                                        ,minbasekv,maxbasekv,
                                        logpath):
    '''
        Return:
            Mis = {"error":0,"return_value":return_value}
            Mis = {"error":1,'which_log':"....","return_value":return_value}
            其中，return_value = {"content":"xxx.sav: 執行失敗","errorcode": 1 }
    '''    
    


    logger_ErrorCircuitFunction = Setlog(logfolder= logpath, level=logging.ERROR,logger_name='ErrorCircuitFunction_log')

    return_value=[]

    for savfile in savefiles:
        savfilename =  savfile.split('.')[0]
        result = Batch_RUN_ErrorCircuit_for_savFile(username = username,
                                                    savefile = f"{savfiledir}/{savfile}"
                                                    ,savfilename = savfilename
                                                    ,targetdir = f"{errorcircuitdir}/{savfilename}"
                                                    ,area = area
                                                    ,zone = zone
                                                    ,owner = owner
                                                    ,minbasekv = minbasekv
                                                    ,maxbasekv = maxbasekv)
        processed_result = errorcircuit_result_process(result = result,
                                    errorcircuitdir = errorcircuitdir,
                                    savfilename = savfilename,
                                    return_value = return_value,
                                    logger_ErrorCircuitFunction = logger_ErrorCircuitFunction)
        print(savfile,'-->',processed_result)                                    
        if processed_result['need_break']:
            break

        return_value = processed_result['return_value']                                  

    if result["error"]:
        
        Mis= {"error":1,'which_log':"ErrorCircuitFunction_log","return_value":return_value}
    else:
        Mis =  {"error":0,"return_value":return_value}
       
    return Mis

def Batch_RUN_ErrorCircuit_for_savFile( username
                                        ,savefile
                                        ,savfilename
                                        ,targetdir
                                        ,area
                                        ,zone
                                        ,owner
                                        ,minbasekv,maxbasekv):
    
    
    
    Choose_how_much_Area_Num = str(len(area))
    # Area_Num = ",".join(area)
    if Choose_how_much_Area_Num=='0':
        Area_Num = '0' 
    else:
        Area_Num = ",".join(area)

    Choose_how_much_Zone_Num = str(len(zone))    
    if Choose_how_much_Zone_Num=='0':
        Zone_Num = '0' 
    else:
        Zone_Num = ",".join(zone)    
    

    Choose_how_much_owner_Num = str(len(owner))
    if Choose_how_much_owner_Num=='0':
        Owner_Num = '0' 
    else:
        Owner_Num = ",".join(owner)        
    

    args =  f" --username {username}"\
        f" --savefile {savefile}"\
        f" --Sav_FileName {savfilename}"\
        f" --targetdir {targetdir}"\
        f" --Area_Num {Area_Num}"\
        f" --Choose_how_much_Area_Num {Choose_how_much_Area_Num}"\
        f" --Zone_Num {Zone_Num}"\
        f" --Choose_how_much_Zone_Num {Choose_how_much_Zone_Num}"\
        f" --Owner_Num {Owner_Num}"\
        f" --Choose_how_much_owner_Num {Choose_how_much_owner_Num}"\
        f" --MinBaseKV {minbasekv}"\
        f" --MaxBaseKV {maxbasekv}"
    # python_location = "C:/server/project/AutoPsse/Scripts/python.exe"
    cmd = run_pyfile_by_execmd(python_location='python'
                                ,pyfile='webinterface/src/ErrorCircuit.py'
                                ,args=args)

    print(cmd)
    result = fileprocess.execCmd(cmd)

    
    return result





  
