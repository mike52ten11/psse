# -*- coding: utf-8 -*-
from pssepyfinctions_of_writing_areadata_convert_to_idv  import  psspy_to_idv
import numpy as np

def write_area(Source_File,target_file,idvpath,args):
        
    
    AREA_Number = int(args.get('AREANumber'))
    AREA_Name = args.get('AREAName')

    # psspy.case(r"%s" %Source_File)   

    # psspy.area_data(AREA_Number,0,[0, 10.0],AREA_Name)
 
    # psspy.save(r"%s" %target_file)
 

    psspycommand =  {   'function':'area_data',
                        'data':[f"{AREA_Number}" 
                                ," "
                                ," "
                                ," "
                                ,f"'{AREA_Name}'"],
                        'labeltype':'area'
                    }
    psspy_to_idv(psspycommand=psspycommand, idvpath=idvpath) 

     



def ParseConfig():

    parser = argparse.ArgumentParser(description="路徑")
    # parser.add_argument('-LabelT', '--Label_type', default="BUS", type=str, help='哪個Label')
    parser.add_argument('-SavF', '--Sav_File', default="112P-11109", type=str, help='sav檔檔名')
    # parser.add_argument('-user', '--User_Folder', default="User/621882/", type=str, help='使用者資料夾路徑')
    parser.add_argument('-source', '--source_dir', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-target', '--target_dir', default="User/621882/", type=str, help='檔案目的地資料夾路徑')
    parser.add_argument('-idv', '--idv_dir', default="User/621882/", type=str, help='使用者要輸入的資料')
    parser.add_argument('-WriteData', '--Write_Data', nargs='+' ,type=str, help='使用者要輸入的資料')


    args = parser.parse_args()

    # labeltype = args.Label_type
    savfile = args.Sav_File
    # userfolder =   args.User_Folder  
    source_dir = args.source_dir
    target_dir = args.target_dir
    writedata = args.Write_Data
    idv_dir = args.idv_dir


    return savfile, idv_dir, source_dir, target_dir, writedata

if __name__ == '__main__':
    import sys, os
    import base64
    import json
    import argparse
    import logging
        
    
    # from Log.LogConfig import Setlog

    savfile, idv_dir, source_dir, target_dir, writedata = ParseConfig()
    

#######==================  解碼   args ================== ####### 
    encode_type = 'utf-8'
    writedata = writedata[0][2:-1]#因為b'編碼後的資料'，其中b'與最後的'被當成是str所以才解碼不出來

    print(writedata)
    str_dict = base64.b64decode(writedata).decode(encode_type)
    str_dict = json.loads(str_dict)
    # logger = Setlog(logfolder= 'Log/'+str_dict.get('userName')+'/PSSELog/', level=logging.INFO,logger_name='psse')
    # logger = Setlog(logfolder = 'Log/'+str_dict.get('userName')+'/PSSELog/',logname='psse')

    Source_File = f"{source_dir}/{savfile}"
    target_file = f"{target_dir}/{savfile}"

    savfilename = savfile.split('.')[0][0:4]
    idvpath = f"{idv_dir}/{savfilename}.idv"

    # logger.info('type(str_dict) = %s',type(str_dict))
    # logger.info('user = %s, labeltype = %s',
    #                     str_dict.get('userName'),
    #                                     str_dict.get('labeltype'))
    # logger.info('Source_File = %s',Source_File)
    # logger.info('target_file = %s',target_file)    
    # logger.info('str_dict = %s',str_dict)
#######==================  解碼     ================== #######  

    print('os.getcwd() --> ',os.getcwd())
    from Config.Load_PSSE_Location import Load_PSSE_Path
    
    Load_PSSE_Path()
    try:    
        import psse35
        psse35.set_minor(3)
        import psspy
        psspy.psseinit()
        # import pssexcel

    except Exception as error: 
        
        print(error)
        
        raise ImportError(error) 
    
    



    repeat = write_area( Source_File = Source_File
                            ,target_file = target_file
                            ,idvpath = idvpath
                            ,args = str_dict)
    print(repeat)
  