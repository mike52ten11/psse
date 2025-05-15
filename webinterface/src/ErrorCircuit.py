
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



# from Config.Load_PSSE_Location import Load_PSSE_Path


# Load_PSSE_Path()

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
except Exception as error: 
    print(error)
    writeFile('errorlog.txt', str(error)+'\n')
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
    
    def __init__(self):

        self.data = []   
        
    def create_sub_file(self, filename):
        
        self.filename = filename
        self.data = "COM\r\n"+\
                "COM SUBSYSTEM description file entry created by PSS(R)E Config File Builder\r\n"+\
                "COM\r\n"+\
                "SUBSYSTEM '345'\r\n"+\
                " JOIN 'GROUP_1'\r\n"+\
                "   AREA 1\r\n"+\
                "   KVRANGE 0.000 345.000\r\n"+\
                " END\r\n"+\
                "END\r\n" +\
                "END\r\n"
                
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)
                
        
    
    def create_con_file(self, filename):
        
         self.filename = filename        
         self.data =  "COM\r\n"+\
                 "COM SUBSYSTEM description file entry created by PSS(R)E Config File Builder\r\n"+\
                 "COM\r\n"+\
                 "SINGLE BRANCH IN SUBSYSTEM '345'\r\n"+\
                 "DOUBLE BRANCH IN SUBSYSTEM '345'\r\n"+\
                 "END\r\n"
                 
         with open(self.filename, 'w',newline='\n') as file:
             file.write(self.data)
                 
         
    
    def create_mon_file(self, filename):
        self.filename = filename
        self.data =  "COM\r\n"+\
                "COM SUBSYSTEM description file entry created by PSS(R)E Config File Builder\r\n"+\
                "COM\r\n"+\
                "MONITOR VOLTAGE RANGE SUBSYSTEM '345' 0.950 1.050\r\n"+\
                "MONITOR VOLTAGE DEVIATION SUBSYSTEM '345' 0.030 0.060\r\n"+\
                "MONITOR BRANCHES IN SUBSYSTEM '345'\r\n"+\
                "MONITOR TIES FROM SUBSYSTEM '345'\r\n"+\
                "END\r\n"
        with open(self.filename, 'w',newline='\n') as file:
            file.write(self.data)
                

def errorcircuit(savefile,savefilename,targetdir, parameters):
    
    logger.info(f'args["NUMAREA"]>> {parameters["NUMAREA"]}')
    logger.info(f'args["AREAS"]>> {parameters["AREAS"]}')
    logger.info(f'args["NUMZONE"]>> {parameters["NUMZONE"]}')
    logger.info(f'args["ZONES"]>> {parameters["ZONES"]}')
    logger.info(f'args["NUMOWNER"]>> {parameters["NUMOWNER"]}')
    logger.info(f'args["OWNERS"]>> {parameters["OWNERS"]}')
    
    logger.info(f'maxbasekv>> {parameters["MaxBaseKV"]}')
    logger.info(f'minbasekv>> {parameters["MinBaseKV"]}') 

    # ResultPath = targetdir
    # SourcePath = pssepath+"psse/"    
    # Source_savFilename = userfolder +'SavFile/'+ savfFilename
    
    # ResultPath = pssepath+"psse/ErrorCircuit/"+rawfile[0:3]+"/"
    os.makedirs(targetdir,exist_ok=True)

    os.makedirs(f'{targetdir}/Excel/',exist_ok=True)
       
    psspy.case(r"%s" %savefile)
    
    # psspy.bsys(0,1,[ 0.0, 345.0],args["NUMAREA"],args["AREAS"],0,[],0,[],args["NUMZONE"],args["ZONES"])
    psspy.bsys(0,1
    ,[ parameters["MinBaseKV"], parameters["MaxBaseKV"]]
        ,parameters["NUMAREA"]
        ,parameters["AREAS"],0,[]
        ,parameters["NUMOWNER"]
        ,parameters["OWNERS"],parameters["NUMZONE"],parameters["ZONES"]
        )
    psspy.ascc_3(0,0,[1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0], 1.0,r"%s" %f"{targetdir}/{savfFilename}.rel","","")


def ParseConfig():
    
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-usr', '--username', default="User/621882/", type=str, help='save檔路徑')
    parser.add_argument('-sf', '--savefile', default="User/621882/", type=str, help='save檔路徑')
    parser.add_argument('-SavFileName', '--Sav_FileName', default="", type=str, help='Raw檔檔名')
    parser.add_argument('-tgdir', '--targetdir', default="", type=str, help='Raw檔檔名')

    
    parser.add_argument('-AreaNum', '--Area_Num', default="1",nargs='+', type=str, help='array that contains the areas to set (input).')
    parser.add_argument('-ChooseHowMuchAreaNum', '--Choose_how_much_Area_Num', default="1", type=str, help='number of areas to set (input)')
    
    parser.add_argument('-ZoneNum', '--Zone_Num', default="1",nargs='+', type=str, help='array that contains the areas to set (input).')
    parser.add_argument('-ChooseHowMuchZoneNum', '--Choose_how_much_Zone_Num', default="1", type=str, help='number of areas to set (input)')
    
    parser.add_argument('-OwnerNum', '--Owner_Num', default="1",nargs='+', type=str, help='array that contains the areas to set (input).')
    parser.add_argument('-ChoosehowmuchownerNum', '--Choose_how_much_owner_Num', default="1", type=str, help='number of areas to set (input)')

    parser.add_argument('-maxbasekv', '--MaxBaseKV', default="345", type=str, help='Raw檔檔名')
    parser.add_argument('-minbasekv', '--MinBaseKV', default="0", type=str, help='Raw檔檔名')

    args = parser.parse_args()
    username = args.username
    savefile = args.savefile
    savfFilename = args.Sav_FileName
    targetdir = args.targetdir

    maxbasekv = float(args.MaxBaseKV)
    minbasekv = float(args.MinBaseKV)

   

    # logger = Setlog(logfolder= f'Log/{username}/PSSELog/', level=logging.INFO,logger_name='errorcircuit')    
    
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

      
    ownernum =   args.Owner_Num
    ownernum = ownernum[0]
    if ownernum=='0':
        OWNERS = [] 
    else:
        OWNERS = [int(i) for i in ownernum.split(',')]    
    # logger.info("zonenum>>",zonenum)
    
    
    # logger.info("ZONES>>",ZONES)
    print(OWNERS)
    ChoosehowmuchownerNum =   args.Choose_how_much_owner_Num
    NUMOWNER = int(ChoosehowmuchownerNum)  

    Pssps_bsys_Function_Parameter = {
        "NUMAREA":NUMAREA,
        "AREAS": AREAS,
        "NUMZONE": NUMZONE,
        "ZONES": ZONES,
        "NUMOWNER": NUMOWNER,
        "OWNERS":OWNERS,
        "MaxBaseKV": maxbasekv,
        "MinBaseKV": minbasekv,        
    }
    return   username, savefile, savfFilename, targetdir, Pssps_bsys_Function_Parameter



if __name__ == '__main__':

    # convert_rel_to_excelFile(r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\ErrorCircuit\113P\113P.rel'
    #                         ,r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\ErrorCircuit\113P\Excel\113P.xlsx')    
    import argparse
    import logging
    from Log.LogConfig import Setlog 
    username, savefile, savfFilename, targetdir, Pssps_bsys_Function_Parameter = ParseConfig()   
    logger = Setlog(logfolder= f'Log/{username}/PSSELog/', level=logging.INFO,logger_name='errorcircuit')

    try:

        errorcircuit(savefile = savefile,
                     savefilename = savfFilename,
                     targetdir = targetdir,
                     parameters = Pssps_bsys_Function_Parameter)
    except Exception as e:
        logger.error(str(e))
        raise e


