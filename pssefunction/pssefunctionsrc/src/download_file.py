
import os

from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse

# from web.logger import logger

from . import fileprocess
from .base import filter_extension
from .tozip import to_zip

class MyDownload:
    def __init__(self, request):
        self.request = request
        self.user = request.user

    def download_savefile(self,params):

        savfile_dir = params["savfile_dir"]
        download_dir = params["download_dir"]
        savfiles = params["savfiles"]

        downloadfile = []

        for savfile in savfiles:
            downloadfile.append(f"{savfile_dir}/{savfile}.sav") #找sav

        print(downloadfile)
       
        zipfilename = 'SavFile'                                
        to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
        
        os.makedirs(f"{download_dir}", exist_ok=True)

        file_path = f"{download_dir}/SavFile.zip"
        print('file_path --> ',file_path)
        with open(file_path, 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        response['Content-Disposition'] = 'attachment; filename=SavFile.zip'
        

        return response


    def download_powerflow(self,params):

        download_what = params["download_what"]
        powerflow_dir = params["powerflow_dir"]
        powerflowsub_dir = params["powerflowsub_dir"]
        download_dir = params["download_dir"]

        savfiles = params["savfiles"]
        downloadfile = []

        if download_what == "download_powerflow":
            # try:
            # source_folder = f"{os.getcwd()}/User/{self.user}/PowerFlow/"
            # power_sub_folder = f"{os.getcwd()}/User/{self.user}/PowerFlowSub/"
            

            #找潮流acc
            for savfile in savfiles:
                if os.path.isfile(f"{powerflow_dir}/{savfile}/{savfile}.acc"):
                    downloadfile.append(f"{powerflow_dir}/{savfile}/{savfile}.acc")                

                #找分岐acc
                for  sub_accfile in filter_extension.find_any_extension(targer_folder=f"{powerflowsub_dir}/{savfile}"
                                                          ,extension=".acc"):
                    downloadfile.append(sub_accfile)

            print('downloadfile -->',downloadfile)
            
            if downloadfile == []:
                args = {   'mismatch':'下載失敗',
                    'messages':['沒有acc，請下載log檔']}
                return   JsonResponse({'results':args}, 
                                    json_dumps_params={'ensure_ascii': False},
                                    safe=False
                                    ,status=404) 

            zipfilename = 'PowerFlow'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
            
            
            file_path = f"{download_dir}/PowerFlow.zip"
            print('file_path --> ',file_path)
            with open(file_path, 'rb') as model_excel:
                result = model_excel.read()
            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=PowerFlow.zip'
            

            return response


        elif   download_what == "download_powerflow_log": 
            
            for savfile in savfiles:
                downloadfile.append(f"{powerflow_dir}/{savfile}/{savfile}.txt")                

                #找分岐acc
                for  sub_accfile in filter_extension.find_any_extension(targer_folder=f"{powerflowsub_dir}/{savfile}"
                                                          ,extension=".txt"):
                    print(sub_accfile)                                      
                    downloadfile.append(sub_accfile)

            print('downloadfile --> ',downloadfile)
            zipfilename = 'PowerFlow_log'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
            
            
            file_path = f"{download_dir}/PowerFlow_log.zip"
            print('file_path --> ',file_path)
            with open(file_path, 'rb') as model_excel:
                result = model_excel.read()
            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=PowerFlow_log.zip'
            

            return response
             

 
        else:
            args = {   'mismatch':'下載失敗',
                'messages':['下載失敗']}
            return   args

    def download_errorcircuit(self,params):
        download_what = params["download_what"]
        if  download_what == "download_errorcircuit":
            # logger = Setlog(logfolder= 'Log/', level=logging.INFO,logger_name='system')
            
            errorcircuit_dir = params["errorcircuit_dir"]
            download_dir = params["download_dir"]

            savfiles = params["savfiles"]  

            downloadfile = []
            
            # source_folder = f"{os.getcwd()}/User/{self.user}/ErrorCircuit/"

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
                return   JsonResponse({'results':args}, 
                                    json_dumps_params={'ensure_ascii': False},
                                    safe=False
                                    ,status=404)                
            zipfilename = 'ErrorCircuit'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 

               
            file_path = f"{download_dir}/ErrorCircuit.zip"
            
            with open(file_path, 'rb') as model_excel:
                result = model_excel.read()

            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=ErrorCircuit.zip'
            
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #         self.user,   '按下下載故障電流按鈕', '下載檔案成功')

            return response

 

        elif download_what=="download_errorcircuit_log":
            errorcircuit_dir = params["errorcircuit_dir"]
            download_dir = params["download_dir"]

            savfiles = params["savfiles"]  
            downloadfile = []
            


            for savfile in savfiles:
                downloadfile.append(f"{errorcircuit_dir}/{savfile}/{savfile}.txt") 




            print(downloadfile)
            
            zipfilename = 'ErrorCircuit_log'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 

               
            file_path = f"{download_dir}/ErrorCircuit_log.zip"
            
            with open(file_path, 'rb') as model_excel:
                result = model_excel.read()

            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=ErrorCircuit_log.zip'            


            return response

        else:
            args = {   'mismatch':'下載失敗',
                'messages':['下載失敗']}
            return   JsonResponse({'results':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)

    def download_dynamic(self,params):

        download_what = params["download_what"]

        if  download_what == "download_dynamic":
            # logger = Setlog(logfolder= 'Log/', level=logging.INFO,logger_name='system')
            
            dynamic_dir = params["dynamic_dir"]
            download_dir = params["download_dir"]

            savfiles = params["savfiles"]  

            downloadfile = []
            
            # source_folder = f"{os.getcwd()}/User/{self.user}/ErrorCircuit/"

            for savfile in savfiles:           
                downloadfile.append(f"{dynamic_dir}/{savfile}/{savfile}.out")#找rel
                downloadfile.append(f"{dynamic_dir}/{savfile}/{savfile}.jpg")#找rel
                downloadfile.append(f"{dynamic_dir}/{savfile}/{savfile}.xlsx")#找rel
                downloadfile.append(f"{dynamic_dir}/{savfile}/dynamic_log_for_psse_result.txt")#找執行psse後的log

            print('downloadfile -->',downloadfile)
            # DownloadFolder = f"{os.getcwd()}/User/{self.user}/DownloadFile/ErrorCircuit/"
            
            zipfilename = 'Dynamic'                                
            to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 

               
            file_path = f"{download_dir}/Dynamic.zip"
            
            with open(file_path, 'rb') as model_excel:
                result = model_excel.read()

            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=Dynamic.zip'
            
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #         self.user,   '按下下載故障電流按鈕', '下載檔案成功')

            return response
        else:

            args = {   'mismatch':'下載失敗',
                'messages':['下載失敗']}
            return   JsonResponse({'results':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)

        # downloadfile = []

        # source_folder = f"{os.getcwd()}/User/{self.user}/Dynamic/"
        # # yearfile = os.listdir(source_folder)
        # # yearfile = self.years
        # for year in self.years:
            
        #     downloadfile.append(source_folder.replace('\\','/')+\
        #                                 f"/{year}"\
        #                                 f'/{year}.out') #找acc
        # for year in self.years:
            
        #     downloadfile.append(source_folder.replace('\\','/')+\
        #                                 f"/{year}"\
        #                                 f'/dynamic_log_for_psse_result.txt') #找acc
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

    def download_idvfile_for_create(self,params):

        download_dir = params["download_dir"]
        idvfile_dir = params["idvfile_dir"]

        downloadfile = [f"{idvfile_dir}/temp.idv"]


        print('downloadfile-->',downloadfile)
       
        zipfilename = 'IDV_for_Create'                                
        to_zip(zipfolder=download_dir,zipfilename=zipfilename, file=downloadfile) 
        
        os.makedirs(f"{download_dir}", exist_ok=True)

        file_path = f"{download_dir}/IDV_for_Create.zip"
        print('file_path --> ',file_path)
        with open(file_path, 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        response['Content-Disposition'] = 'attachment; filename=IDV_for_Create.zip'
        

        return response

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


     
     
