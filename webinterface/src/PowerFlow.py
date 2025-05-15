
# -*- coding: utf-8 -*-

def writeFile(filename, data):  
    f = open(filename, "a")  
    f.write(data)  
    f.close()  


import sys, os
import datetime
# from Config.Load_PSSE_Location import Load_PSSE_Path

import numpy as np

# pssepy_PATH=(r"""C:\Program Files\PTI\PSSE35\35.3\PSSPY37""")
# sys.path.append(pssepy_PATH)
try:    
    pssepy_PATH = os.environ.get('PSSE') 
    sys.path.append(pssepy_PATH)    
    import psse35
    # psse35.set_minor(3)
    import psspy
    psspy.psseinit()
    # import pssexcel
    import argparse
    import logging
    import shutil
except Exception as error: 
    print('error')
    writeFile('../Log/errorlog.txt', str(error)+'\n')
    raise ImportError(error)  
     
    # print("An error occurred:", str(error))



def accc(accfile='savnw.acc', outpath=None, show=True, cosep=True):
    import pssexcel

    if not os.path.exists(accfile):
        prgmsg = " Error: Input accfile '{0}' does not exist".format(accfile)
        print(prgmsg)
        return

    # Change these values as required.
    string  = ['s','e','b','i','v','l','g','p']
    colabel = [] #'base case', 'trip1nuclear', 'trip2nuclear']

    p, nx = os.path.split(accfile)
    n, x  = os.path.splitext(nx)

    # xlsfile = get_output_filename(outpath, 'pssexcel_demo_accc_' + n)
    xlsfile = outpath
    sheet = n + '_accc'
    overwritesheet = True

    baseflowvio = False
    basevoltvio = False
    flowlimit   = 0.0
    flowchange  = 0.0
    voltchange  = 0.0

    pssexcel.accc(accfile,string,colabel=colabel,xlsfile=xlsfile,sheet=sheet,overwritesheet=overwritesheet,show=show,
                  baseflowvio=baseflowvio, basevoltvio=basevoltvio, flowlimit=flowlimit,
                  flowchange=flowchange, voltchange=voltchange, cosep=cosep)

def read_rawFile_and_export_to_savFile(rawFilename = r"112P-11109"):
    psspy.read(0,r"%s" %rawFilename+".raw")
    psspy.save(r"%s" %rawFilename+".sav")

class  create_X_file:
    
    def __init__(self,userfolder,savfile,parameter):
        self.source_savfile = savfile


        self.num_area = parameter["NUMAREA"]
        self.areas = parameter["AREAS"]

        self.num_zone = parameter["NUMZONE"]
        self.zones = parameter["ZONES"]

        self.max_basekv = parameter["MaxBaseKV"]
        self.min_basekv = parameter["MinBaseKV"]

        self.userfolder = userfolder
        self.data = []   
        
    def create_sub_file(self, filename):

        
        # areas = np.load(f'{self.userfolder}/filter/area/area_{self.source_savfile}.npz')
        print(f'{userfolder}/filter/area/area_{self.source_savfile}.npz')
        content_for_sub = ""
        if self.num_area>0:
            
            for area_number in self.areas:
                print(area_number)                
                content_for_sub = f"{content_for_sub}"\
                                f"   AREA {area_number}\r\n"
        if self.num_zone>0:
           
            for zone_number in self.zones:
                print(zone_number)                
                content_for_sub = f"{content_for_sub}"\
                                f"   ZONE {zone_number}\r\n"

        self.filename = filename
        self.data = f"COM\r\n"\
                f"COM SUBSYSTEM description file entry created by PSS(R)E Config File Builder\r\n"\
                f"COM\r\n"\
                f"SUBSYSTEM 'RUN_FIRST_FLOW'\r\n"\
                f" JOIN 'GROUP_1'\r\n"\
                f"{content_for_sub}"\
                f"   KVRANGE {self.min_basekv} {self.max_basekv}\r\n"\
                f" END\r\n"\
                f"END\r\n" \
                f"END\r\n"
                # f"   AREA 1\r\n"\
                # f"   AREA 2\r\n"\
                # f"   AREA 3\r\n"\
                # f"   AREA 4\r\n"\               
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)
                
    def create_N0_con_file(self, filename):
        
        self.filename = filename        
        self.data =    f"COM\r\n"\
                    f"COM CONTINGENCY description file entry created by PSS(R)E Config File Builder\r\n"\
                    f"COM\r\n"\
                    f"END"

                
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)         
    
    def create_N1_con_file(self, filename):
        
        self.filename = filename        
        self.data =    f"COM\r\n"\
                    f"COM CONTINGENCY description file entry created by PSS(R)E Config File Builder\r\n"\
                    f"COM\r\n"\
                    f"SINGLE BRANCH IN SUBSYSTEM 'RUN_FIRST_FLOW'\r\n"\
                    f"END"

                
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)
                 
    def create_N2_con_file(self, filename):
        
        self.filename = filename        
        self.data =    f"COM\r\n"\
                    f"COM CONTINGENCY description file entry created by PSS(R)E Config File Builder\r\n"\
                    f"COM\r\n"\
                    f"DOUBLE BRANCH IN SUBSYSTEM  'RUN_FIRST_FLOW'\r\n"\
                    f"END"

                
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)         

    def create_N1_N2_con_file(self, filename):
        
        self.filename = filename        
        self.data =    f"COM\r\n"\
                    f"COM CONTINGENCY description file entry created by PSS(R)E Config File Builder\r\n"\
                    f"COM\r\n"\
                    f"SINGLE BRANCH IN SUBSYSTEM 'RUN_FIRST_FLOW'\r\n"\
                    f"DOUBLE BRANCH IN SUBSYSTEM  'RUN_FIRST_FLOW'\r\n"\
                    f"END"

                
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)

    def create_mon_file(self, filename):
        self.filename = filename
        self.data =  f"COM\r\n"\
                    f"COM MONITORED element file entry created by PSS(R)E Config File Builder\r\n"\
                    f"COM\r\n"\
                    f"MONITOR BRANCHES IN SUBSYSTEM 'RUN_FIRST_FLOW'\r\n"\
                    f"END"



        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)
                
def powerflow_workflow(savfile, userfolder,targetfolder, parameter):
    powerflow(savfile, userfolder,targetfolder,parameter)
    # if not convergence:
    #     powerflow(savfile, userfolder,parameter)
    # else:
    #     pass
        # print('excel')
        # ResultPath = userfolder+'PowerFlow/'+rawfile+'/'
        # ExcelFolderpath = ResultPath+'Excel_Files/'
        # accc(accfile=ResultPath+rawfile+".acc", outpath=ExcelFolderpath+rawfile , show=False, cosep=True)

def create_sub_mon_con_file(filename,userfolder,savfile,parameter):
    Create_File = create_X_file(userfolder=userfolder,savfile=savfile,parameter=parameter)
    
    Create_File.create_sub_file(filename= f"{filename}.sub")

    
    if parameter["ConfileType"]=="N1":
        Create_File.create_N1_con_file(filename= f"{filename}.con")       

    else:
        Create_File.create_N1_con_file(filename= f"{filename}_n1.con")
        Create_File.create_N2_con_file(filename= f"{filename}.con")

    # if parameter["ConfileType"]=="N0":
    #     Create_File.create_N0_con_file(filename= f"{filename}.con")

    # elif parameter["ConfileType"]=="N1":
    #     Create_File.create_N1_con_file(filename= f"{filename}.con")

    # elif parameter["ConfileType"]=="N2":
    #     Create_File.create_N2_con_file(filename= f"{filename}.con")

    # else:  
    #     Create_File.create_N1_N2_con_file(filename= f"{filename}.con")
    
       
    
    Create_File.create_mon_file(filename= f"{filename}.mon")    


def powerflow(savfile, userfolder,targetfolder,parameter):    



    # print(ResultPath)
    #清powerflow資料夾
    # shutil.rmtree(targetfolder,ignore_errors=True)
    # #清powerflow sub資料夾
    # shutil.rmtree(f"{userfolder}/PowerFlowSub/",ignore_errors=True)

    os.makedirs(targetfolder,exist_ok=True)
    
    create_sub_mon_con_file(filename = f"{targetfolder}/{savfile}"
                            ,userfolder=userfolder
                            , savfile =savfile
                            ,parameter=parameter)


    # ExcelFolderpath = f"{ResultPath}/Excel_Files/"
    # os.makedirs(ExcelFolderpath,exist_ok=True)

    # SourcePath = userfolder
    
    Source_rawFilename = f"{userfolder}/SavFile/Powerflow/{savfile}"
    print(Source_rawFilename)

    # read_rawFile_and_export_to_savFile(r"%s" %Source_rawFilename)
    
    psspy.case(r"%s" %f"{Source_rawFilename}.sav")
    # print('Largest mismatch start')
    # if mismatch >xx:#1MW
    a = psspy.fnsl([1,0,0,1,1,1,-1,0])#第一次    
    b = psspy.fnsl([1,0,0,1,1,0,0,0])#第二次[1,0,0,1,1,0,0,0]

    psspy.dfax_2([1,1,0],r"%s" %f"{targetfolder}/{savfile}.sub",r"%s" %f"{targetfolder}/{savfile}.mon"
        ,r"%s" %f"{targetfolder}/{savfile}.con", r"%s" %f"{targetfolder}/{savfile}")    
    psspy.accc_with_dsp_3( 0.5,[1,0,0,1,1,1,0,0,0,0,0]
                            ,r"""345""",r"%s" %r"%s" %f'{targetfolder}/{savfile}.dfx'
                            , r"%s" %f'{targetfolder}/{savfile}.acc'
                            ,"","","")

    


if __name__ == '__main__':
    from Log.LogConfig import Setlog 
    
    parser = argparse.ArgumentParser(description="路徑")
   
    parser.add_argument('-savfile', '--Sav_File', default="112P-11109", type=str, help='Raw檔檔名')
    parser.add_argument('-userfolder', '--User_Folder', default="User/621882/", type=str, help='使用者資料夾路徑')
    parser.add_argument('-target', '--Target_Folder', default="User/621882/", type=str, help='使用者資料夾路徑')
    # parser.add_argument('-convg', '--convergence', default='0', type=str, help='是否收斂')
    parser.add_argument('-username', '--User_Name', default='621882', type=str, help='使用者名稱')
    
    parser.add_argument('-AreaNum', '--Area_Num', default="1",nargs='+', type=str, help='array that contains the areas to set (input).')
    parser.add_argument('-ChooseHowMuchAreaNum', '--Choose_how_much_Area_Num', default="1", type=str, help='number of areas to set (input)')
    
    parser.add_argument('-ZoneNum', '--Zone_Num', default="1",nargs='+', type=str, help='array that contains the areas to set (input).')
    parser.add_argument('-ChooseHowMuchZoneNum', '--Choose_how_much_Zone_Num', default="1", type=str, help='number of areas to set (input)')
    
    parser.add_argument('-OwnerNum', '--Owner_Num', default="1",nargs='+', type=str, help='array that contains the areas to set (input).')
    parser.add_argument('-ChoosehowmuchownerNum', '--Choose_how_much_owner_Num', default="1", type=str, help='number of areas to set (input)')

    parser.add_argument('-maxbasekv', '--MaxBaseKV', default="345", type=str, help='Raw檔檔名')
    parser.add_argument('-minbasekv', '--MinBaseKV', default="0", type=str, help='Raw檔檔名')

    parser.add_argument('-confiletype', '--confile_type', default="0", type=str, help='選擇N0,N1,N2或多選')
    
    args = parser.parse_args()
    
    savfile = args.Sav_File
    userfolder =   args.User_Folder
    targetfolder =   args.Target_Folder 
    # convergence = int(args.convergence)

    username = args.User_Name

    maxbasekv = float(args.MaxBaseKV)
    minbasekv = float(args.MinBaseKV)

    areanum =   args.Area_Num
    areanum = areanum[0]

    if areanum=='0':
        AREAS = [] 
    else:
        AREAS = [int(i) for i in areanum.split(',')]

    ChooseHowMuchAreaNum =   args.Choose_how_much_Area_Num
    NUMAREA = int(ChooseHowMuchAreaNum)        
    

    zonenum =   args.Zone_Num
    zonenum = zonenum[0]
    # logger.info("zonenum>>",zonenum)
    print(zonenum)
    if zonenum=='0':
        ZONES = [] 
    else:
        ZONES = [int(i) for i in zonenum.split(',')]  
    
    # logger.info("ZONES>>",ZONES)
    print(ZONES)
    ChooseHowMuchZoneNum =   args.Choose_how_much_Zone_Num
    NUMZONE = int(ChooseHowMuchZoneNum)  

    confile_type =   args.confile_type   

    Pssps_bsys_Function_Parameter = {
        "NUMAREA":NUMAREA,
        "AREAS": AREAS,
        "NUMZONE": NUMZONE,
        "ZONES": ZONES,
        "MaxBaseKV": maxbasekv,
        "MinBaseKV": minbasekv,    
        "ConfileType":confile_type    
    }    

    today = datetime.date.today()
    logger = Setlog(logfolder = f'../Log/{username}/PSSELog/Powerflow/'
                    , level = logging.INFO
                    ,logger_name = f'powerflow_{today}')
        
    try:
        powerflow_workflow(savfile=savfile
        , userfolder=userfolder
        ,targetfolder = targetfolder
        # , convergence=convergence
        , parameter=Pssps_bsys_Function_Parameter)
    except Exception as e:
        logger.error(e)
        raise e    



