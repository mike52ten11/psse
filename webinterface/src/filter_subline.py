import numpy as np
import sys,os
import shutil
import logging       
from Log.LogConfig import Setlog   
import chardet


def check_encoding_type(checked_data):
     
    return chardet.detect(checked_data)['encoding']

def writeFile(filename, data, encodingtype='ansi'):  
    with open(filename, "w", encoding=encodingtype) as file:
        file.write(data)




def Filter_by_BusName(labeltype,Source_File,userName,target,zonenum, areanum, minbasekv, maxbasekv,filterfile):



    if labeltype=='bus':
        os.makedirs(target,exist_ok=True)

        psspy.case(r"%s" %Source_File) 

        # psspy.dfax_2([1,1,0],r"%s" %subfilename,r"%s" %monfilename
        #     ,r"%s" %confilename, r"%s" %ResultPath+rawfile)   
         
        busnum_and_name_from_filterfile = np.load(filterfile) 
        print(areanum)
        if zonenum==[]:
            IERR = psspy.bsys(1,1,[ minbasekv, maxbasekv],1,areanum,0,[],0,[],0,[])
        else:
            IERR = psspy.bsys(1,1,[ minbasekv, maxbasekv],0,[],0,[],0,[],1,[zonenum])
        

        # psspy.find('*分歧','161')
        
        # ierr, carray = psspy.abuschar(1, 1, 'NAME') 

        ierr, subline_busnumber_list = psspy.abusint(1, 1, 'NUMBER')
        print(subline_busnumber_list)

        
        subline_busname_list = [] 
        if subline_busnumber_list!=None:
               
            for busnum in subline_busnumber_list[0]:
                index = np.where(busnum_and_name_from_filterfile["num"].astype(int)==busnum)
                subline_busname_list.append(busnum_and_name_from_filterfile["name"][index][0])
            
            np.savez(f'{target}/分歧線的BusName與BusNum.npz', busname=subline_busname_list
                            , busnum = subline_busnumber_list[0]) 

        else:
            np.savez(f'{target}/分歧線的BusName與BusNum.npz', busname=subline_busname_list
                            , busnum = [])
        print(subline_busname_list)

        # logger_filter_busname.info(f'FUNCTION:psspy.bsys(1,1,[ {minbasekv}, {maxbasekv}],0,[],0,[],0,[],1,{zonenum})，MESSAGE:找到的分歧線{name}')

        writeFile(f'{target}/分歧線的BusName.txt', ','.join(subline_busname_list))

        


    
    elif labeltype=='zone': 
        ierr, carray = psspy.abuschar(1, 1, 'NAME') 
        ierr, iarray = psspy.azoneint(1, 1, 'NUMBER')


    else:
        pass
    # return (carray[0],iarray[0])



def ParseConfig():
    import argparse
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-LabelT', '--Label_type', default="BUS", type=str, help='哪個Label')
    parser.add_argument('-SavF', '--Sav_File', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-user', '--User_name', default="User/621882/", type=str, help='使用者名稱')
    parser.add_argument('-source', '--source_Folder', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-target', '--target_Folder', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    
    parser.add_argument('-zonenum', '--ZoneNum', default=0,nargs='+', type=int, help='選哪個區域')
    parser.add_argument('-areanum', '--AreaNum', default=0,nargs='+', type=int, help='選哪個區域')
        
    parser.add_argument('-maxbasekv', '--MaxBaseKV', default="345", type=str, help='Raw檔檔名')
    parser.add_argument('-minbasekv', '--MinBaseKV', default="0", type=str, help='Raw檔檔名')
    
    args = parser.parse_args()

    labeltype = args.Label_type
    savfile = args.Sav_File
    username =   args.User_name
    sourcefolder = args.source_Folder
    targetfolder = args.target_Folder
    zonenum = args.ZoneNum    


    areanum = args.AreaNum

    maxbasekv = float(args.MaxBaseKV)
    minbasekv = float(args.MinBaseKV)  


    return labeltype, savfile, username, sourcefolder,targetfolder, zonenum, areanum, minbasekv, maxbasekv


if __name__ == '__main__':

    labeltype, savfile, username, sourcefolder,targetfolder, zonenum, areanum, minbasekv, maxbasekv= ParseConfig()
    
    logger_filter_busname = Setlog(logfolder= f'../Log/{username}/PSSELog/Powerflow_Subline/'
                        , level=logging.INFO,logger_name='filter_busname')    
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

        logger_filter_busname.error('filter faild occur %s',str(error))
        
        
        raise ImportError(error) 
#######==================  解碼   args ================== ####### 
    encode_type = 'utf-8'
    # logger = Setlog(logfolder = 'Log/'+str_dict.get('userName')+'/PSSELog/',logname='psse')
    filterfile= f'../Data/User/AnonymousUser/filter/PowerFlow/bus/bus_{savfile}.npz'
    Source_File = f'{sourcefolder}/{savfile}'

    if  zonenum!=0: 
        target = f"{targetfolder}/close/Zone_{zonenum[0]}"
    elif  areanum!=0: 
        target = f"{targetfolder}/close/Area_{areanum[0]}"
    else:
        pass    
#######==================  解碼     ================== #######  

    Filter_by_BusName(labeltype
                    ,Source_File,username
                    ,target
                    , zonenum
                    , areanum
                    , minbasekv, maxbasekv
                    ,filterfile)




