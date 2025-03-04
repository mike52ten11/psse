
# -*- coding: utf-8 -*-

def writeFile(filename, data):  
    f = open(filename, "a")  
    f.write(data)  
    f.close()  

def getconfig():
    config = configparser.ConfigParser()
    config.read(file_path)
    profile = get_profile()
    return config[profile]


import sys, os


from Config.Load_PSSE_Location import Load_PSSE_Path


Load_PSSE_Path()

try:    
    import psse35
    psse35.set_minor(3)
    import psspy
    psspy.psseinit()
    # import pssexcel
    import argparse
    import logging
except Exception as error: 
    print(error)
    writeFile('errorlog.txt', str(error)+'\n')
    raise ImportError(error)  
     
    # print("An error occurred:", str(error))



def run_idv(Source_savFilename, Target_savFilename, userfolder, idvpath):

    psspy.case(r"%s" %Source_savFilename)
    psspy.runrspnsfile(idvpath)
    psspy.save(r"%s" %Target_savFilename)
    os.remove(idvpath)

def ParseConfig():
    
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-source_savfile', '--Source_SavFileName', default="", type=str, help='sav檔檔名')
    parser.add_argument('-target_savfile', '--Target_SavFileName', default="", type=str, help='sav檔檔名')
    parser.add_argument('-UserFolder', '--User_Folder', default="User/621882/", type=str, help='使用者資料夾路徑')
    parser.add_argument('-UserName', '--User_name', default="", type=str, help='sav檔檔名')
    
    parser.add_argument('-IDV', '--IDV_Path', default="1", type=str, help='idv檔位置')

    args = parser.parse_args()
    source_savfFilename = args.Source_SavFileName
    target_savfFilename = args.Target_SavFileName

    userfolder =   args.User_Folder
    username = args.User_name

    idvpath = args.IDV_Path


    return  source_savfFilename, target_savfFilename, userfolder, username, idvpath



if __name__ == '__main__':

    import argparse
    import logging
    from Log.LogConfig import Setlog 
    source_savfFilename, target_savfFilename, userfolder, username, idvpath = ParseConfig()   
    logger = Setlog(logfolder= f'Log/{username}/PSSELog/', level=logging.INFO,logger_name='errorcircuit')

    try:

        run_idv(Source_savFilename=source_savfFilename
                , Target_savFilename=target_savfFilename
                , userfolder=userfolder
                , idvpath=idvpath)
    except Exception as e:
        logger.error(str(e))
        raise e


