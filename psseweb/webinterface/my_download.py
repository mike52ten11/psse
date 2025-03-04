
import os
import requests
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.http import HttpResponse

# from web.logger import logger
from .src import fileprocess
import uuid
from .readconfig import read_config
def download_zipfile_from_psseserver(url:str, params:dict):
    storage_path = f'temp/{uuid.uuid4()}.zip'
    response = requests.get(url
                            , params=params
                            # ,proxies = settings['proxy']
                            )
    print(response.status_code)
    if response.status_code==200:
        with open(storage_path, 'wb') as f:
            f.write(response.content)

        return {"error":0, "file_path":storage_path,'download_what':params['download_what']}   
    else:
        print(response.json()['results'])
        return {"error":1, "file_path":storage_path, "error_messages":response.json()['results']['messages'][0]}

    # try:        
    #     response = requests.get(url
    #                             , params=params
    #                             # ,proxies = settings['proxy']
    #                             )
    #     print(response.status_code)
    #     if response.status_code==200:
    #         with open(storage_path, 'wb') as f:
    #             f.write(response.content)

    #         return {"error":0, "file_path":storage_path,'download_what':params['download_what']}   
    #     else:
    #         print(response.json()['results'])
    #         return {"error":1, "file_path":storage_path, "error_messages":response.json()['results']['messages'][0]}

    # except Exception as e:
    #     print('e -->',e)
    #     return {"error":1, "file_path":storage_path, "error_messages":str(e)}



class MyDownload:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.userdir = f"../Data/User/{self.user}"
        self.savfile_dir = f"{self.userdir}/SavFile"
        self.idvfile_dir = f'{self.userdir}/IDV'
        self.dynamic_dir = f'{self.userdir}/Dynamic'
        self.powerflow_dir = f'{self.userdir}/PowerFlow'
        self.powerflowsub_dir = f'{self.userdir}/PowerFlowSub'
        self.errorcircuit_dir = f'{self.userdir}/ErrorCircuit'
        self.filter_dir = f'{self.userdir}/filter'
        self.excute_idvfile_dir = f'{self.userdir}/excute_idvfile'                
        self.savfiles = request.POST.getlist('year')
        self.download_dir = f"../Data/User/{self.user}/DownloadFile"
        self.proxies = {
                        'http': None,
                        'https': None,
                    }
        # self.api_ip = '10.52.15.201'    
        # self.api_port = '800'
        self.server_settings = read_config()
        self.url = f"http://{self.server_settings['server_host']}:{self.server_settings['server_port']}"

        
    def download_savefile(self):
        params = {
            'savfile_dir': self.savfile_dir,
            'download_dir': f"{self.download_dir}/SavFile",
            'savfiles': self.savfiles,
            'download_what': "download_savefile",
            }
        print(params)    

        return   download_zipfile_from_psseserver(
                                    url = f"{self.url}/download_savfile/"
                                    , params = params
                                    # , settings = self.api_settings
                                )     


    def download_powerflow(self):
        if 'download_powerflow' in self.request.POST:
            params = {
                'savfiles':self.savfiles,
                'download_what': "download_powerflow",
                'powerflow_dir': self.powerflow_dir,
                'powerflowsub_dir':self.powerflowsub_dir,
                'download_dir':f"{self.download_dir}/Powerflow"
                }
        elif 'download_powerflow_log' in self.request.POST:   
            params = {
                'savfiles':self.savfiles,
                'download_what': "download_powerflow_log",
                'powerflow_dir': self.powerflow_dir,
                'powerflowsub_dir':self.powerflowsub_dir,
                'download_dir':f"{self.download_dir}/Powerflow"
                }
        else:
            return {"error":1, "file_path":"none", "error_messages":"error no this buttom"}          

        print(params)    


        return download_zipfile_from_psseserver(
                                    url = f"{self.url}/download_powerflow/"
                                    , params = params
                                    # , settings = self.api_settings
                                )          

    def download_errorcircuit(self):
        print()
        if 'download_errorcircuit' in self.request.POST:
            params = {
                'savfiles':self.savfiles,
                'download_what': "download_errorcircuit",
                'errorcircuit_dir': self.errorcircuit_dir,
                'download_dir':f"{self.download_dir}/Errorcircuit"
                }
        elif 'download_errorcircuit_log' in self.request.POST:   
            params = {
                'savfiles':self.savfiles,
                'download_what': "download_errorcircuit_log",
                'errorcircuit_dir': self.errorcircuit_dir,
                'download_dir':f"{self.download_dir}/Errorcircuit"
                }
        else:
            return {"error":1, "file_path":"none", "error_messages":"error no this buttom"}         
        print(params)    


        return download_zipfile_from_psseserver(
                                    url = f"{self.url}/download_errorcircuit/"
                                    , params = params
                                    # , settings = self.api_settings
                                )

    def download_dynamic(self):
        params = {
            'savfiles':self.savfiles,
            'download_what': "download_dynamic",
            'dynamic_dir': self.dynamic_dir,
            'download_dir':f"{self.download_dir}/Dynamic"
            }
        print(params)    


        return download_zipfile_from_psseserver(
                                    url = f"{self.url}/download_dynamic/"
                                    , params = params
                                    # , settings = self.api_settings
                                )

    def download_idvfile_for_create(self):
        params = {
            'download_what': "download_idvfile_for_create",
            'idvfile_dir': self.idvfile_dir,
            'download_dir':f"{self.download_dir}/IDV_for_create"
            }
        print(params)    


        return download_zipfile_from_psseserver(
                                    url = f"{self.url}/download_idvfile_for_create/"
                                    , params = params
                                    # , settings = self.api_settings
                                )
        # downloadfile = []

        # source_folder = f"{os.getcwd()}/User/{self.user}/Dynamic/"
        # yearfile = os.listdir(source_folder)
        # yearfile = self.years
        # for year in self.years:
            
        #     downloadfile.append(source_folder.replace('\\','/')+\
        #                                 f"/{year}"\
        #                                 f'/{year}.out') #找out
        # for year in self.years:
            
        #     downloadfile.append(source_folder.replace('\\','/')+\
        #                                 f"/{year}"\
        #                                 f'/dynamic_log_for_psse_result.txt') #找執行的log
        # print(downloadfile)
        # DownloadFolder = f'{os.getcwd()}/User/{self.user}/DownloadFile/Dynamic/'
        # zipfilename = 'Dynamic'                                
        # to_zip(zipfolder=DownloadFolder,zipfilename=zipfilename, file=downloadfile) 
        
        # if self.request.method == 'POST':
        #     #try: 
        #     file_path = DownloadFolder+zipfilename+"/Dynamic.zip"
        #     # file_path = "./User/"+str(username)+ "/PowerFlow/Excel_Files/Generate_the_result_of_PowerFlow.xlsx"
        #     with open(file_path, 'rb') as model_excel:
        #         result = model_excel.read()
        #     response = HttpResponse(result)
        #     response['Content-Disposition'] = 'attachment; filename=Dynamic.zip'
            
        #     logger.info('USER: %s ACTION: %s MESSAGE: %s',
        #             self.user,   '按下下載idv檔案按鈕', '下載檔案成功')

        #     return response
        # else:
        #     args = {   'mismatch':'下載失敗',
        #         'messages':['下載失敗']}
        #     return   download_dynamic_out_page(request,args)    

        # if "download_errorcircuit" in self.request.POST:
        #     # logger = Setlog(logfolder= 'Log/', level=logging.INFO,logger_name='system')
            
        #     downloadfile = []
            
        #     source_folder = f"{os.getcwd()}/User/{self.user}/ErrorCircuit/"
            
        #     yearfile = self.years
        #     for year in range(len(yearfile)):
        #         downloadfile.append(os.path.join(source_folder, 
        #                                         yearfile[year]).replace('\\','/')+\
        #                                     '/'+yearfile[year]+'.rel') #找acc
        #     for year in range(len(yearfile)):
        #         if os.path.isfile(os.path.join(source_folder, 
        #                                         yearfile[year]).replace('\\','/')+\
        #                                     '/Excel/'+yearfile[year]+'.csv'):
        #             downloadfile.append(os.path.join(source_folder, 
        #                                         yearfile[year]).replace('\\','/')+\
        #                                     '/Excel/'+yearfile[year]+'.csv') #找excel
        #     print(downloadfile)
        #     DownloadFolder = f"{os.getcwd()}/User/{self.user}/DownloadFile/ErrorCircuit/"
            
        #     zipfilename = 'ErrorCircuit'                                
        #     to_zip(zipfolder=DownloadFolder,zipfilename=zipfilename, file=downloadfile) 
            
        #     if self.request.method == 'POST':
        #         #try: 
        #         file_path = f"{DownloadFolder}{zipfilename}/ErrorCircuit.zip"
                
        #         with open(file_path, 'rb') as model_excel:
        #             result = model_excel.read()

        #         response = HttpResponse(result)
        #         response['Content-Disposition'] = 'attachment; filename=Generate_the_result_of_ErrorCircuit.zip'
                
        #         logger.info('USER: %s ACTION: %s MESSAGE: %s',
        #                 self.user,   '按下下載故障電流按鈕', '下載檔案成功')

        #         return response

 

        # elif "download_errorcircuit_log" in self.request.POST:

        #     downloadfile = []
            
        #     source_folder = f"{os.getcwd()}/User/{self.user}/ErrorCircuit/"
            
        #     yearfile = self.years
        #     for year in range(len(yearfile)):
        #         downloadfile.append(os.path.join(source_folder, 
        #                                         yearfile[year]).replace('\\','/')+\
        #                                     '/'+yearfile[year]+'_log.txt') #找acc




        #     print(downloadfile)
        #     DownloadFolder = f"{os.getcwd()}/User/{self.user}/DownloadFile/ErrorCircuit_log/"
        #     zipfilename = 'ErrorCircuit_log'                                
        #     to_zip(zipfolder=DownloadFolder,zipfilename=zipfilename, file=downloadfile) 
            
        #     if self.request.method == 'POST':
        #         #try: 
        #         file_path = DownloadFolder+zipfilename+"/ErrorCircuit_log.zip"
                
        #         with open(file_path, 'rb') as model_excel:
        #             result = model_excel.read()
        #         response = HttpResponse(result)
        #         response['Content-Disposition'] = 'attachment; filename=Generate_the_result_of_ErrorCircuit_log.zip'
                
        #         logger.info('USER: %s ACTION: %s MESSAGE: %s',
        #                 self.user,   '按下下載故障電流按鈕', '下載檔案成功')

        #         return response

        # else:
        #     args = {   'mismatch':'下載失敗',
        #         'messages':['下載失敗']}
        #     return   download_powerflow_page(self.request,args)  


 

    def download_idvfile(self):


        downloadfile = []
        
        source_folder = f"{os.getcwd()}/User/{self.user}/IDV/"
        
        yearfile = self.years
        for year in range(len(yearfile)):
            downloadfile.append(source_folder.replace('\\','/')+\
                                        '/'+yearfile[year]+'.idv') #找acc

        print(downloadfile)
        DownloadFolder = f'{os.getcwd()}/User/{self.user}/DownloadFile/IDV/'
        zipfilename = 'IDV'
        to_zip(zipfolder=DownloadFolder,zipfilename=zipfilename, file=downloadfile) 
        
        if self.request.method == 'POST':

            file_path = f"{DownloadFolder}{zipfilename}/IDV.zip"
            
            with open(file_path, 'rb') as model_excel:
                result = model_excel.read()

            response = HttpResponse(result)

            response['Content-Disposition'] = 'attachment; filename=IDV.zip'
            
            logger.info('USER: %s ACTION: %s MESSAGE: %s',
                    self.user,   '按下下載idv檔案按鈕', '下載檔案成功')

            return response


        else:

            args = {    'mismatch':'下載失敗',
                        'messages':['下載失敗']}
            return download_idvfile_page(self.request,*args)  


     
     
