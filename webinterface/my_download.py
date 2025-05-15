
import os
import requests
from pathlib import Path
from typing import List
from icecream import ic
ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='debug > ')
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.http import HttpResponse

# from web.logger import logger
from .src import fileprocess
import uuid
from .readconfig import read_config
from .src.tozip import to_zip,powerflow_to_zip
from .src.base import filter_extension

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


def get_out_filenames(folder: str) -> List[str]:
    folder_path = Path(folder)
    # 找出所有 .out 檔案並提取檔名
    return [file.stem for file in folder_path.glob("*.out")]

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
        self.errorcircuit_dir = f'{self.userdir}/FaultCurrent'
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
        savfile_dir = self.savfile_dir
        download_dir = f"{self.download_dir}/Savfiles"

        
        downloadfile = []        
        for savfile in self.savfiles:
            if os.path.isfile(f"{savfile_dir}/{savfile}.sav"):
                downloadfile.append(f"{savfile_dir}/{savfile}.sav")                


        print('downloadfile -->',downloadfile)
        
        if downloadfile == []:
            return   {'error':0, 'messages':['沒有sav可下載'] } 

        zipfilename = 'Savfiles'                                
        to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
        
        
        file_path = f"{download_dir}/Savfiles.zip"
        return {'error':0, 'zipfile_path': file_path}   

    def download_savefile_of_powerflow(self):
        savfile_dir = f"{self.savfile_dir}/Powerflow"
        download_dir = f"{self.download_dir}/Savfiles"

        
        downloadfile = []        
        for savfile in self.savfiles:
            if os.path.isfile(f"{savfile_dir}/{savfile}.sav"):
                downloadfile.append(f"{savfile_dir}/{savfile}.sav")                


        print('downloadfile -->',downloadfile)
        
        if downloadfile == []:
            return   {'error':0, 'messages':['沒有sav可下載'] } 

        zipfilename = 'Savfiles_of_powerflow'                                
        to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
        
        
        file_path = f"{download_dir}/Savfiles_of_powerflow.zip"
        return {'error':0, 'zipfile_path': file_path}   

    def download_savefile_of_errorcircuit(self):
        savfile_dir = f"{self.savfile_dir}/ErrorCircuit"
        download_dir = f"{self.download_dir}/Savfiles"

        
        downloadfile = []        
        for savfile in self.savfiles:
            if os.path.isfile(f"{savfile_dir}/{savfile}.sav"):
                downloadfile.append(f"{savfile_dir}/{savfile}.sav")                


        print('downloadfile -->',downloadfile)
        
        if downloadfile == []:
            return   {'error':0, 'messages':['沒有sav可下載'] } 

        zipfilename = 'Savfiles_of_errorcircuit'                                
        to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
        
        
        file_path = f"{download_dir}/Savfiles_of_errorcircuit.zip"
        return {'error':0, 'zipfile_path': file_path}   


    def download_powerflow(self):
        powerflow_dir = self.powerflow_dir
        powerflowsub_dir = self.powerflowsub_dir
        download_dir = f"{self.download_dir}/Powerflow"

        
        # downloadfile = []

        if 'download_powerflow' in self.request.POST:

        #     #找潮流acc
        #     for savfile in self.savfiles:
        #         if os.path.isfile(f"{powerflow_dir}/{savfile}/{savfile}.acc"):
        #             downloadfile.append(f"{powerflow_dir}/{savfile}/{savfile}.acc")                

        #         #找分岐acc
        #         for  sub_accfile in filter_extension.find_any_extension(targer_folder=f"{powerflowsub_dir}/{savfile}"
        #                                                   ,extension=".acc"):
        #             downloadfile.append(sub_accfile)

        #     print('downloadfile -->',downloadfile)
            
        #     if downloadfile == []:
        #         return   {'error':0, 'messages':['沒有acc，請下載log檔'] } 

            zipfilename = 'PowerFlow'
            powerflow_to_zip(   years = self.savfiles,
                                zipfolder = download_dir,
                                zipfilename = zipfilename,
                                powerflow_dir = self.powerflow_dir, 
                                powerflowsub_dir = self.powerflowsub_dir
                                ) 
            
            
            file_path = f"{download_dir}/PowerFlow.zip"
            return {'error':0, 'zipfile_path': file_path}



        elif   'download_powerflow_log' in self.request.POST:
            
            for savfile in self.savfiles:
                downloadfile.append(f"{powerflow_dir}/{savfile}/{savfile}.txt")                

                #找分岐acc
                for  sub_accfile in filter_extension.find_any_extension(targer_folder=f"{powerflowsub_dir}/{savfile}"
                                                          ,extension=".txt"):
                    print(sub_accfile)                                      
                    downloadfile.append(sub_accfile)

            print('downloadfile --> ',downloadfile)
            zipfilename = 'PowerFlow_log'                                
            powerflow_to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
            
            
            file_path = f"{download_dir}/PowerFlow_log.zip"
            return {'error':0, 'zipfile_path': file_path}

             

 
        else:
            args = {   'mismatch':'下載失敗',
                'messages':['下載失敗']}
            return   {'error':1, 'messages': ['下載失敗']}      


    def download_errorcircuit(self):
        errorcircuit_dir = self.errorcircuit_dir
        download_dir = f"{self.download_dir}/FaultCurrent"

        savfiles = self.savfiles
        downloadfile = []

        if 'download_errorcircuit' in self.request.POST:
            

            for savfile in savfiles:
                if os.path.isfile(f"{errorcircuit_dir}/{savfile}/{savfile}.rel"):
                    downloadfile.append(f"{errorcircuit_dir}/{savfile}/{savfile}.rel")#找rel

                if os.path.isfile(f"{errorcircuit_dir}/{savfile}/Excel/{savfile}.csv"):
                    downloadfile.append(f"{errorcircuit_dir}/{savfile}/Excel/{savfile}.csv")#找csv

            print('downloadfile -->',downloadfile)
            # DownloadFolder = f"{os.getcwd()}/User/{self.user}/DownloadFile/ErrorCircuit/"
            if downloadfile == []:
                args = {   'mismatch':'下載失敗',
                    'messages':['沒有rel，請下載log檔']}
                return   {'results':args}  

            zipfilename = 'FaultCurrent'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 

               
            file_path = f"{download_dir}/FaultCurrent.zip" 
            return {'error':0, 'zipfile_path': file_path}

        elif 'download_errorcircuit_log' in self.request.POST:   
            for savfile in savfiles:
                downloadfile.append(f"{errorcircuit_dir}/{savfile}/{savfile}.txt") 




            print(downloadfile)
            
            zipfilename = 'FaultCurrent_log'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 

               
            file_path = f"{download_dir}/FaultCurrent_log.zip"
            return {'error':0, 'zipfile_path': file_path}
        else:
            args = {   'mismatch':'下載失敗',
                'messages':['下載失敗']}
            return   JsonResponse({'results':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)

    def download_dynamic(self):
        dynamic_dir = self.dynamic_dir
        download_dir = f"{self.download_dir}/Dynamic"

        # savfiles = self.savfiles
        downloadfile = []        
        if 'download_dynamic' in self.request.POST:
            # dynamic_dir = params["dynamic_dir"]
            # download_dir = params["download_dir"]

            # savfiles = params["savfiles"]  

            # downloadfile = []
            
            # source_folder = f"{os.getcwd()}/User/{self.user}/ErrorCircuit/"

            for savfile in self.savfiles:

                for outfilname in get_out_filenames(f"{dynamic_dir}/{savfile}"):
                    downloadfile.append(f"{dynamic_dir}/{savfile}/{outfilname}.out")#找 out
                    downloadfile.append(f"{dynamic_dir}/{savfile}/{outfilname}.jpg")#找 jpg
                    downloadfile.append(f"{dynamic_dir}/{savfile}/{outfilname}.xlsx")#找 xlsx
                    
                # downloadfile.append(f"{dynamic_dir}/{savfile}/{savfile}.out")#找 out
                # downloadfile.append(f"{dynamic_dir}/{savfile}/{savfile}.jpg")#找 jpg
                # downloadfile.append(f"{dynamic_dir}/{savfile}/{savfile}.xlsx")#找 xlsx
                # downloadfile.append(f"{dynamic_dir}/{savfile}/dynamic_log_for_psse_result.txt")#找執行psse後的log

            print('downloadfile -->',downloadfile)
            # DownloadFolder = f"{os.getcwd()}/User/{self.user}/DownloadFile/ErrorCircuit/"
            
            zipfilename = 'Dynamic'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 

               
            file_path = f"{download_dir}/Dynamic.zip"
            
            return {'error':0, 'zipfile_path': file_path}            

        else:
            args = {   'mismatch':'下載失敗',
                'messages':['下載失敗']}
            return   JsonResponse({'results':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)    
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
 

    # def download_idvfile(self):


    #     downloadfile = []
        
    #     source_folder = f"{os.getcwd()}/User/{self.user}/IDV/"
        
    #     yearfile = self.years
    #     for year in range(len(yearfile)):
    #         downloadfile.append(source_folder.replace('\\','/')+\
    #                                     '/'+yearfile[year]+'.idv') #找acc

    #     print(downloadfile)
    #     DownloadFolder = f'{os.getcwd()}/User/{self.user}/DownloadFile/IDV/'
    #     zipfilename = 'IDV'
    #     to_zip(zipfolder=DownloadFolder,zipfilename=zipfilename, file=downloadfile) 
        
    #     if self.request.method == 'POST':

    #         file_path = f"{DownloadFolder}{zipfilename}/IDV.zip"
            
    #         with open(file_path, 'rb') as model_excel:
    #             result = model_excel.read()

    #         response = HttpResponse(result)

    #         response['Content-Disposition'] = 'attachment; filename=IDV.zip'
            
    #         logger.info('USER: %s ACTION: %s MESSAGE: %s',
    #                 self.user,   '按下下載idv檔案按鈕', '下載檔案成功')

    #         return response


    #     else:

    #         args = {    'mismatch':'下載失敗',
    #                     'messages':['下載失敗']}
    #         return download_idvfile_page(self.request,*args)  


     
     
