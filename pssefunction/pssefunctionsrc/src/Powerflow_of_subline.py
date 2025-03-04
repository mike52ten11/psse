import numpy as np
import sys,os
import shutil
import logging       
from Log.LogConfig import Setlog   



def powerflow_sub_flow(username,savfile,powerflow_folder,Source_File,target,busnum):
    
    


    os.makedirs(target,exist_ok=True)

   

    psspy.case(Source_File)
    psspy.dscn(busnum) #關busnum
    
    a = psspy.fnsl([1,0,0,1,1,1,-1,0])#第一次    
    b = psspy.fnsl([1,0,0,1,1,0,0,0])#第二次[1,0,0,1,1,0,0,0]
    
    psspy.dfax_2(   [1,1,0]
                    ,r"%s" %f"{powerflow_folder}/{savfile}/{savfile}.sub"
                    ,r"%s" %f"{powerflow_folder}/{savfile}/{savfile}.mon"
                    ,r"%s" %f"{powerflow_folder}/{savfile}/{savfile}.con"
                    ,r"%s" %f"{target}/{busnum}"
                    )    
    psspy.accc_with_dsp_3( 0.5,[1,0,0,1,0,1,0,0,0,0,0]
                            ,r"""%s"""%f"{busnum}",r"%s" %r"%s" %f"{target}/{busnum}.dfx"
                            , r"%s" %f"{target}/{busnum}.acc"
                            ,"","","")

    # psspy.rate_2(0,1,1,1,1,0, 100.0)#看limit有沒有>100
    psspy.save(f'{target}/close_{busnum}.sav')
    psspy.recn(busnum)#開busnum
    print(f"{powerflow_folder}/{savfile}/{savfile}.sub")
    print(f"{powerflow_folder}/{savfile}/{savfile}.mon")
    print(f"{powerflow_folder}/{savfile}/{savfile}.con")
    print(f"{target}/{busnum}")


def ParseConfig():
    import argparse
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-SavF', '--Sav_File', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-user', '--User_name', default="User/621882/", type=str, help='使用者名稱')
    parser.add_argument('-powerflowdir', '--powerflow_Folder', default="User/621882/Powerflow/", type=str, help='潮流資料夾路徑')      
    parser.add_argument('-source', '--source_Folder', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-target', '--target_Folder', default="User/621882/", type=str, help='目標資料夾路徑')
    parser.add_argument('-busnum', '--busnumber', default="User/621882/", type=str, help='bus 編號')
    args = parser.parse_args()

    
    savfile = args.Sav_File
    username =   args.User_name
    sourcefolder = args.source_Folder
    powerflow_folder = args.powerflow_Folder

    targetfolder = args.target_Folder
    busnum = int(args.busnumber)

    return savfile, username, powerflow_folder,sourcefolder,targetfolder, busnum


if __name__ == '__main__':

    savfile, username,powerflow_folder ,sourcefolder,targetfolder, busnum = ParseConfig()
    
    logger_filter_busname = Setlog(logfolder= 'Log/'+username+'/PSSELog/Powerflow_Subline/', level=logging.INFO,logger_name='filter_busname')    
    # pssepy_PATH=(r"""C:\Program Files\PTI\PSSE35\35.3\PSSPY37""")
    # sys.path.append(pssepy_PATH)
    # from Config.Load_PSSE_Location import Load_PSSE_Path
    # Load_PSSE_Path()    
    try:    
        pssepy_PATH = os.environ.get('PSSE') 
        sys.path.append(pssepy_PATH)
        import psse35
        # psse35.set_minor(3)
        import psspy
        psspy.psseinit()
        
        logger_filter_busname.info('import package sucess')
        
    except Exception as error: 

        logger_filter_busname.error('filter faild occur %s',str(e))
        
        
        raise ImportError(error) 

    encode_type = 'utf-8'
    # logger = Setlog(logfolder = 'Log/'+str_dict.get('userName')+'/PSSELog/',logname='psse')

    Source_File = f"{sourcefolder}/Powerflow/{savfile}.sav"
    target = f"{targetfolder}"

    powerflow_sub_flow(username = username
                    ,savfile=savfile
                    ,powerflow_folder=powerflow_folder
                    ,Source_File=Source_File
                    ,target=target
                    ,busnum=busnum)




