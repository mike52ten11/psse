import sys, os


def Filter_by_BusName(labeltype,Source_File,userName,savfile_name, targetdir):
    import numpy as np
    
    import logging       
    from Log.LogConfig import Setlog   
    # from Config.Load_PSSE_Location import Load_PSSE_Path


    logger_filter_busname = Setlog(logfolder= 'Log/'+userName+'/filter/', level=logging.INFO,logger_name='filter_busname')
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
    # store_location = f"../Data/User/{username}/filter/{labeltype}/"
    os.makedirs(f'{targetdir}/{labeltype}',exist_ok=True)

    if labeltype=='bus':
        psspy.case(r"%s" %Source_File)         
        ierr, carray = psspy.abuschar(-1, 1, 'NAME')
        # print("ierr >> ", ierr) 
        ierr, iarray = psspy.abusint(-1, 1, 'NUMBER')
        # print("ierr >> ",ierr) 
        # print(carray)
        # print(iarray)
        np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz', name=carray[0], num=iarray[0]) 
    
    elif labeltype=='zone': 
        # print(Source_File)
        psspy.case(r"%s" %Source_File)
        result = psspy.list(0, 1, 16, 0)  # 指定所有參數

        # ierr, carray = psspy.azonechar(-1, 1, 'ZONENAME') 
        # ierr, iarray = psspy.azoneint(-1, 1, 'NUMBER')
        # print(carray)
        # print(iarray)
        # np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz', name=carray[0], num=iarray[0]) 
    
    elif labeltype=='owner': 
        # print(Source_File)
        psspy.case(r"%s" %Source_File)
        result = psspy.list(0, 1, 19, 0)  # 指定owner 包括沒有被assign的
        # ierr, carray = psspy.aownerchar(-1, 1, 'OWNERNAME') 
        # ierr, iarray = psspy.aownerint(-1, 1, 'NUMBER')
        # print(carray)
        # print(iarray)
        # np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz', name=carray[0], num=iarray[0]) 
    
    elif labeltype=='area':
        # print(Source_File)
        psspy.case(r"%s" %Source_File)
        result = psspy.list(0, 1, 11, 0)  # 指定所有參數

               
        # ierr, carray = psspy.aareachar(-1, 2, 'AREANAME')#找連接的
        # ierr, iarray = psspy.aareaint(-1, 2, 'NUMBER')#找連接的
        # print('AREANAME --> ', carray)
        # print('NUMBER --> ', iarray)

        # np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz', name=carray[0], num=iarray[0]) 

        
    elif labeltype=='machine':
        psspy.case(r"%s" %Source_File)
        # psspy.list(0,1,5,0)
        ierr, carray = psspy.amachchar(-1, 1, 'NAME')       
        ierr, iarray = psspy.amachint(-1, 1, 'NUMBER')
        ierr, machinid = psspy.amachchar(-1, 1, 'ID')  
        # print(iarray)
        # print(carray)
        np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz', name=carray[0], num=iarray[0],id=machinid[0]) 

    # elif labeltype=='twowinding':
    #     psspy.case(r"%s" %Source_File)
    #     ierr, carray = psspy.atrnchar(-1, 1, 1, 1, 1, "FROMNAME")
    #     # print(carray)
    #     # print('有幾個 name  carray -->',len(carray[0]))
    elif labeltype=='twowinding':
        psspy.case(r"%s" %Source_File)  
        psspy.list(0,1,21,0) 

    elif labeltype=='threewinding':
        psspy.case(r"%s" %Source_File)  
        psspy.list(0,1,25,0)   

    elif labeltype=='fixedshunt':
        psspy.case(r"%s" %Source_File)  
        psspy.list(0,1,28,0) 

    elif labeltype == 'branch' or  labeltype=='tripline':
        psspy.case(r"%s" %Source_File)
        psspy.list(0,1,6,0)
        # ierr, fromnum = psspy.aflowint(-1, 1, 1, 1, "FROMNUMBER")
        # ierr, toname = psspy.aflowchar(-1, 1, 1, 1, "TONAME")
        # ierr, tonum = psspy.aflowint(-1, 1, 1, 1, "TONUMBER")
        # ierr, circuit_id = psspy.aflowchar(-1, 1, 1, 1, "ID")
        # # print(circuit_id)
        # np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz', fromnum=fromnum[0], name=toname[0],num=tonum[0],circuit_id=circuit_id[0])         
    
    elif labeltype=='load':
        psspy.case(r"%s" %Source_File)    
        psspy.list(0,1,18,0)
        # ierr, carray = psspy.aloadchar(-1, 1, 'NAME')
        # ierr, iarray = psspy.aloadint(-1, 1, 'NUMBER')
        # ierr, loadid = psspy.aloadchar(-1, 1, 'ID')  
        # print(iarray)
        
        # np.savez(f'{targetdir}/{labeltype}/{labeltype}_{savfile_name}.npz',name=carray[0], num=iarray[0], id=loadid[0]) 

    else:
        psspy.case(r"%s" %Source_File)
        result = psspy.list(0, 1, 16, 0)  # 指定所有參數
 
        # ierr = psspy.list(0, 1, 11, 0) #會列出所有的 area，但是只會打印在cmd
        
        # ierr = psspy.check_powerflow_data(0,1,18)#可以檢查 哪些 area 沒有被assign 但是只會打印在cmd

 
        # pass
    # return ierr, carray

def ParseConfig():
    import argparse
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-LabelT', '--Label_type', default="BUS", type=str, help='哪個Label')
    parser.add_argument('-SavF', '--Sav_FileName', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-user', '--User_name', default="User/621882/", type=str, help='使用者名稱')
    parser.add_argument('-sourcesavfile', '--savfiledir', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-TargetDir', '--target_dir', default="User/621882/", type=str, help='檔案來源資料夾路徑')

    args = parser.parse_args()

    labeltype = args.Label_type
    savfile_name = args.Sav_FileName
    username =   args.User_name
    savfiledir = args.savfiledir
    source_savfile = f"{savfiledir}/{savfile_name}.sav"
    targetdir = args.target_dir

    return labeltype, savfile_name, username, source_savfile, targetdir


if __name__ == '__main__':

    labeltype, savfile_name, username, source_savfile, targetdir = ParseConfig()
    
    Filter_by_BusName(labeltype = labeltype
                        ,Source_File = source_savfile 
                        ,userName = username
                        ,savfile_name = savfile_name
                        ,targetdir = targetdir )






