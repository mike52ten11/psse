import re
import logging
import datetime


from .base.check_encoding_type_from_psse import check_encoding_type
from .Log.LogConfig import Setlog
from . import fileprocess

def run_pyfile_by_execmd(python_location: str, pyfile: str, args: str) -> str:

    return f"{python_location} {pyfile} {args}"


def powerFlow_result_process(result: dict,
                            #   loop_times: int,
                            #   convergence_threshold: float,  # 修改為正確的英文拼寫
                              user_folder: str,  # 遵循小寫命名規則
                              savfile: str,
                              return_value: int,
                              logger_powerflow_function: logging.Logger
                              ,logfilepath: str):
    # logfilepath = f"{user_folder}/PowerFlow/{savfile}/{savfile}.txt"
    if not result.get("error"):
        #確定Psse回傳資料的編碼格式
        encoding_type = check_encoding_type(result['return_value'])

        #找Psse回傳資料裡有沒有 ERROR
        pat1 = 'ERROR: (.*)'
        print(f"**************************************\n")
        print("解碼開始")
        try:
            error_mismatch = re.search(pat1, result["return_value"].decode('ansi'))
        except:
            error_mismatch = re.search(pat1, result["return_value"].decode("ISO-8859-1"))    

        print('error_mismatch -->',error_mismatch)
        if error_mismatch:
            error_mismatch = error_mismatch.group(1)    
        if error_mismatch is not None:
            print('*'*40)
            # print(f'loop_times = {loop_times+1}')
            try:
                error_mismatch = re.search(pat1, result["return_value"].decode('ansi'))
            except:
                error_mismatch = re.search(pat1, result["return_value"].decode("ISO-8859-1"))              
            # print(result["return_value"].decode("ISO-8859-1"))
            print('*'*40)
            
            fileprocess.writeFile(logfilepath, result["return_value"])
            return_value.append({"content":f"{savfile}: psse執行成功，回傳error，請下載log","errorcode": 1 })
            return {
                    'need_break':1
                    ,"return_value":return_value
                    ,"break_from_where":'找Psse回傳資料裡有沒有 ERROR 的block'
                    }
        #==========================================================================    
        else:    
            #找Psse回傳資料裡的mistach
            pat1 = 'System total absolute mismatch:\s*\w*.\w*\s*\w*'
            pat2 = 'Reached tolerance in\s*\w*\s*iterations'
            try:
                mismatch = re.findall(pat1, result["return_value"].decode("ansi"))
            except:
                mismatch = re.findall(pat1, result["return_value"].decode("ISO-8859-1"))
                 
            try:
                iterations = re.findall(pat2, result["return_value"].decode("ansi"))
            except:
                iterations = re.findall(pat2, result["return_value"].decode("ISO-8859-1"))


            print("mismatch >> ",mismatch )
            print("iterations >> ",iterations)
            if mismatch!=[] and iterations!=[]:

                mismatch_value = re.findall(r"\d+\.?\d*", mismatch[-1])
                                
                # print(loop_times)
                print('*'*40)
                print(float(mismatch_value[0]))
                # if float(mismatch_value[0])< convergence_threshold:
                print('yesstart')
                print('mismatch:',mismatch)

                #寫入psee回傳的 log
                iferror = fileprocess.writeFile(logfilepath, result["return_value"])
                
                if iferror["error"]:
                    return_value.append({"content":f"PowerFlow-{savfile}.sav執行成功，但寫入log失敗: mismatch: {mismatch_value[0]} MVA, ",
                                    "errorcode": 0 }) 
                    print("ERROR:" ,iferror["return_value"]["backend_message"])                
                    logger_powerflow_function.warning('sav檔案:%s 錯誤訊息:\n %s',savfile,iferror["return_value"]["backend_message"])                 
                    return {
                            'need_break':1
                            ,"return_value":return_value
                            ,"break_from_where":'寫入psee回傳的 log 的block'
                            }    
                else:
                    #執行沒任何問題的block

                    print('end')
                    return_value.append({"content":f"PowerFlow-{savfile}: mismatch: {mismatch_value[0]} MVA",
                                        "errorcode": 0 }) 
                    
                    
                    # fileprocess.writeFile(f"{UserFolder}PowerFlow/{savfile}/{savfile}_log.txt", result["return_value"])
                    return {
                            'need_break':1
                            ,"return_value":return_value
                            ,"break_from_where":' 執行沒任何問題的block'
                            }  


                # else:
                #     #還未收斂    
                #     logger_powerflow_function.warning(
                #             'sav檔案:%s 執行次數:%s Powerflow回傳:\n %s'
                #             ,savfile,loop_times,result["return_value"]) 

                #     return {
                #             'need_break':0
                #             ,"return_value":return_value
                #             ,"break_from_where":'還未收斂'
                #             }  
            else:
                #找不到 mismatch 和 iterations 的block    
                logger_powerflow_function.warning(
                        'sav檔案:%s 執行次數:%s Powerflow回傳:\n %s'
                        ,savfile,result["return_value"].decode("ansi")) 

                return {
                        'need_break':0
                        ,"return_value":return_value
                        ,"break_from_where":'找不到 mismatch 和 iterations 的block'
                        }  


    else:
        #run_pyfile_by_execmd有Error的block
        
        logger_powerflow_function.warning('sav檔案:%s 錯誤訊息:\n %s',savfile,result["return_value"]["backend_message"].decode("ansi"))
        return_value.append({"content":f"PowerFlow-{savfile}.sav 執行失敗( run_pyfile_by_execmd 執行有Error)",
                                "errorcode": 1 })            
        return {
                'need_break':1
                ,"return_value":return_value
                ,"break_from_where":'run_pyfile_by_execmd有Error的block'
        }  


def RUN_PowerFlow_for_many_saveFile(    UserFolder
                                        ,TargetFolder
                                        ,user
                                        ,yearlist
                                        # ,convergence_thread_hold
                                        ,area
                                        ,zone
                                        ,minbasekv
                                        ,maxbasekv
                                        ,confile_type):
    '''
        Return:
            Mis = {"error":0,"return_value":return_value}
            Mis = {"error":1,'which_log':"....","return_value":return_value}
            其中，return_value = {"content":"xxx.sav: 執行失敗","errorcode": 1 }
    '''
    today = datetime.date.today()


    savfilelocation = UserFolder+'SavFile/Powerflow/'
    Sav_File_list = yearlist

   
    Mis = {}
    logger_PowerflowFunction = Setlog(logfolder = f"../Log/{user}/System/Powerflow_Log/"
                                    , level = logging.INFO
                                    , logger_name = f'Powerflow_Log_{today}')
    
    RUN_PowerFlow_for_many_savFile_Exception_error = 0
    return_value=[]
    area_and_zone = f"area={'+'.join(area)},zone={'+'.join(zone)}"
    
    for savfile in Sav_File_list:
        targetdir = f"{TargetFolder}/{savfile}/{confile_type}/{area_and_zone}"
        result = Batch_RUN_Psse_for_rawFile(savfile = savfile
                                            , UserFolder = UserFolder
                                            ,TargetFolder = targetdir
                                            ,user = user
                                            # , convergence = '0' 
                                            ,area=area
                                            ,zone=zone
                                            ,minbasekv=minbasekv
                                            ,maxbasekv=maxbasekv
                                            ,confile_type=confile_type)

        logger_PowerflowFunction.info(f"FUNCTION: webinterface/src/run_powerflow.py，MESSAGE:執行結果log，請到{today}的log，PROCESS: 使用 Batch_RUN_Psse_for_rawFile 函式")
        

        #處理psse回傳結果
        processed_result = powerFlow_result_process(result
                                                # ,loop_times
                                                # ,convergence_thread_hold
                                                ,UserFolder
                                                ,savfile
                                                ,return_value
                                                ,logger_PowerflowFunction
                                                ,logfilepath = f"{targetdir}/{savfile}.txt"
                                            )
        '''
            processed_result格式:
            {
                'need_break':1
                ,"return_value":return_value
                ,"break_from_where":' 執行沒任何問題的block'
            }  
        '''

        logger_PowerflowFunction.info(f"FUNCTION: webinterface/src/run_powerflow.py，MESSAGE:{processed_result} ，PROCESS: 處理psse回傳結果，使用 powerFlow_result_process 函式")
        
        return_value = processed_result['return_value']
        # if loop_times==4:
        #     #跑4次還是未收斂
            
        #     fileprocess.writeFile(f"{UserFolder}PowerFlow/{savfile}/{savfile}_log.txt", result["return_value"])
        #     return_value.append({"content":f"PowerFlow-{savfile}.sav: 未收斂",
        #                         "errorcode": 0 })         

        # except Exception as error:
        #     logger_PowerflowFunction.error('%s',f"PowerFlow-{savfile}.sav: {error}")       
        #     RUN_PowerFlow_for_many_savFile_Exception_error = 1 
        #     fileprocess.writeFile(f"{UserFolder}PowerFlow/{savfile}/{savfile}_log.txt", result["return_value"])
        #     return_value.append({"content":f"PowerFlow-{savfile}.sav: 執行失敗，系統錯誤",
        #                          "errorcode": 1 })
           

    if RUN_PowerFlow_for_many_savFile_Exception_error:      
        Mis= {"error":1,'which_log':"Powerflow_Log","return_value":return_value}
    else:    
        Mis = {"error":0,"return_value":return_value}

    return Mis


def Batch_RUN_Psse_for_rawFile( savfile
                                , UserFolder
                                ,TargetFolder
                                , user
                                # ,convergence                                                
                                ,area                                
                                ,zone
                                ,minbasekv
                                ,maxbasekv
                                ,confile_type):
    print(savfile, ' ' ,UserFolder, ' ', user, ' ')


    Choose_how_much_Zone_Num = str(len(zone))    
    if Choose_how_much_Zone_Num=='0':
        Zone_Num = '0' 
    else:
        Zone_Num = ",".join(zone)     

    Choose_how_much_Area_Num = str(len(area))    
    if Choose_how_much_Area_Num=='0':
        Area_Num = '0' 
    else:
        Area_Num = ",".join(area)
        
    args =  f" --Sav_File {savfile}"\
        f" --User_Folder {UserFolder}"\
        f" --Target_Folder {TargetFolder}"\
        f" --User_Name {user}"\
        f" --Zone_Num {Zone_Num}"\
        f" --Choose_how_much_Zone_Num {Choose_how_much_Zone_Num}"\
        f" --MinBaseKV {minbasekv}"\
        f" --MaxBaseKV {maxbasekv}"\
        f" --confile_type {confile_type}"\
        f" --Area_Num {Area_Num}"\
        f" --Choose_how_much_Area_Num {Choose_how_much_Area_Num}"
    cmd = run_pyfile_by_execmd(python_location='python'
                                ,pyfile='webinterface/src/PowerFlow.py'
                                ,args=args)    

    result = fileprocess.execCmd(cmd)


    return result


def RUN_PowerFlow(  username
                    ,yearlist
                    ,TargetFolder
                    # ,convergence_thread_hold
                    ,area
                    ,zone
                    ,minbasekv
                    ,maxbasekv
                    ,confile_type):

    UserFolder = f'../Data/User/{username}'     
    
    mis = RUN_PowerFlow_for_many_saveFile(UserFolder=UserFolder
                                        ,TargetFolder = TargetFolder
                                        , user=username
                                        ,yearlist=yearlist
                                        # ,convergence_thread_hold=float(convergence_thread_hold)
                                        ,area=area
                                        ,zone=zone
                                        ,minbasekv=minbasekv
                                        ,maxbasekv=maxbasekv
                                        ,confile_type=confile_type)
    
    return mis
