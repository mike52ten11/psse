
import os
import shutil
import json
import requests
from icecream import ic
ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='debug > ')
from datetime import datetime

from django.core.files.storage import default_storage
from django.core.cache import cache

from webinterface.src import fileprocess

from webinterface.src.base.check_filename import checkfilename
from webinterface.src.cache_data_type import get_cache_key
from webinterface.src.base.delete import Delete

from .datapath import data_path_of_user_on_server
from .readconfig import read_config
from .src.pssefunction.run_filter import run_filter

from .src.pssefunction.convert_to_raw import convert_to_raw
from .src import run_powerflow

from .src import run_powerflow_subline_161n1
from .src import run_powerflow_subline_345n1
from .src import run_powerflow_subline_345n2

from .src import run_error_circuit
from .src import run_dynamic

class CreateWriteSavTempFile():
    def __init__(self,temp_dir):
        self.temp_dir = temp_dir

    def area(self):
        with open(f'{self.temp_dir}/area.idv', 'r', encoding='ansi') as f:
            area_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(area_data) 

    def zone(self):
        with open(f'{self.temp_dir}/zone.idv', 'r', encoding='ansi') as f:
            zone_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(zone_data)                 

    def owner(self):
        with open(f'{self.temp_dir}/owner.idv', 'r', encoding='ansi') as f:
            owner_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(owner_data) 

    def bus(self):
        with open(f'{self.temp_dir}/bus.idv', 'r', encoding='ansi') as f:
            bus_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(bus_data)

    def machine(self):
        with open(f'{self.temp_dir}/machine.idv', 'r', encoding='ansi') as f:
            machine_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(machine_data) 

    def load(self):
        with open(f'{self.temp_dir}/load.idv', 'r', encoding='ansi') as f:
            laod_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(laod_data) 

    def branch(self):
        with open(f'{self.temp_dir}/branch.idv', 'r', encoding='ansi') as f:
            branch_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(branch_data) 
    def branch(self):
        with open(f'{self.temp_dir}/branch.idv', 'r', encoding='ansi') as f:
            branch_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(branch_data) 
    def twowinding(self):
        with open(f'{self.temp_dir}/twowinding.idv', 'r', encoding='ansi') as f:
            branch_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(branch_data) 

    def twowinding_edit(self):
        with open(f'{self.temp_dir}/twowinding_edit.idv', 'r', encoding='ansi') as f:
            branch_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(branch_data)             

    def threewinding(self):
        with open(f'{self.temp_dir}/threewinding.idv', 'r', encoding='ansi') as f:
            branch_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(branch_data) 


    def threewinding_winding(self):
        with open(f'{self.temp_dir}/threewinding_winding.idv', 'r', encoding='ansi') as f:
            branch_data = f.readlines()

        with open(f'{self.temp_dir}/temp.idv', 'a', encoding='ansi') as f:
            f.writelines(branch_data)                                     

class MyFunctions:
    def __init__(self, request):
        self.request = request
        self.user = str(request.user)
        self.datapath = data_path_of_user_on_server(self.user)
        self.server_settings = read_config()
        self.url = f"http://{self.server_settings['server_host']}:{self.server_settings['server_port']}"
        
    def filter(self, sav_file_name):

        print('sav_file_name in filter = ',sav_file_name)
        savfile_dir =  f'{self.datapath["savfile_dir"]}'
        filter_dir = f'{self.datapath["filter_dir"]}'
        
        for savfile in sav_file_name:
            Delete().action_of_filter_all(filter_dir,savfile)

            convert_results = convert_to_raw(sav_file_name=savfile, savfile_dir=savfile_dir, target_dir=savfile_dir)     
  
            if isinstance(convert_results, dict) and "error" in convert_results:  # 如果回傳了錯誤
                return [
                            f'轉成raw檔案失敗，\nfunction:{convert_results["error"]["function"]}，錯誤訊息:{convert_results["error"]["message"]}，{convert_results["error"]["type"]}\nTraceback:\n{convert_results["error"]["traceback"]}'
                        ]
            result = run_filter(filename=savfile, rawfilepath=f"{savfile_dir}/{savfile}.raw", filter_dir=filter_dir)
            print('result -->',result)
            if isinstance(result, dict) and "error" in result:  # 如果回傳了錯誤
                # 根據需求處理錯誤
                return   [
                            f'製作filter檔案失敗，\nfunction:{result["error"]["function"]}，錯誤訊息:{result["error"]["message"]}，{result["error"]["type"]}\nTraceback:\n{result["error"]["traceback"]}'
                          ]    
                                                
        return [f'上傳成功，製作filter檔案成功']

    def filter_powerflow(self, sav_file_name):

        print('sav_file_name in filter = ',sav_file_name)
        savfile_dir =  f'{self.datapath["savfile_dir"]}/PowerFlow'
        filter_dir = f'{self.datapath["filter_dir"]}/PowerFlow'
        
        for savfile in sav_file_name:
            Delete().action_of_filter_all(filter_dir,savfile)

            convert_results = convert_to_raw(sav_file_name=savfile, savfile_dir=savfile_dir, target_dir=savfile_dir)     
  
            if isinstance(convert_results, dict) and "error" in convert_results:  # 如果回傳了錯誤
                return [
                            f'轉成raw檔案失敗，\nfunction:{convert_results["error"]["function"]}，錯誤訊息:{convert_results["error"]["message"]}，{convert_results["error"]["type"]}\nTraceback:\n{convert_results["error"]["traceback"]}'
                        ]
            result = run_filter(filename=savfile, rawfilepath=f"{savfile_dir}/{savfile}.raw", filter_dir=filter_dir)
            print('result -->',result)
            if isinstance(result, dict) and "error" in result:  # 如果回傳了錯誤
                # 根據需求處理錯誤
                return   [
                            f'製作filter檔案失敗，\nfunction:{result["error"]["function"]}，錯誤訊息:{result["error"]["message"]}，{result["error"]["type"]}\nTraceback:\n{result["error"]["traceback"]}'
                          ]    
                                                
        return [f'上傳成功，製作filter檔案成功']

    def filter_errorcircuit(self, sav_file_name):

                
        print('sav_file_name in filter = ',sav_file_name)
        savfile_dir =  f'{self.datapath["savfile_dir"]}/FaultCurrent'
        filter_dir = f'{self.datapath["filter_dir"]}/FaultCurrent'
        
        for savfile in sav_file_name:
            Delete().action_of_filter_all(filter_dir,savfile)

            convert_results = convert_to_raw(sav_file_name=savfile, savfile_dir=savfile_dir, target_dir=savfile_dir)     
  
            if isinstance(convert_results, dict) and "error" in convert_results:  # 如果回傳了錯誤
                return [
                            f'轉成raw檔案失敗，\nfunction:{convert_results["error"]["function"]}，錯誤訊息:{convert_results["error"]["message"]}，{convert_results["error"]["type"]}\nTraceback:\n{convert_results["error"]["traceback"]}'
                        ]
            result = run_filter(filename=savfile, rawfilepath=f"{savfile_dir}/{savfile}.raw", filter_dir=filter_dir)
            print('result -->',result)
            if isinstance(result, dict) and "error" in result:  # 如果回傳了錯誤
                # 根據需求處理錯誤
                return   [
                            f'製作filter檔案失敗，\nfunction:{result["error"]["function"]}，錯誤訊息:{result["error"]["message"]}，{result["error"]["type"]}\nTraceback:\n{result["error"]["traceback"]}'
                          ]    
                                                
        return [f'上傳成功，製作filter檔案成功']

    def upload(self, upload_what):
        messages = ''
        
        if self.request.method == 'POST':
 
            if upload_what == 'savfile':

                sav_file = self.request.FILES.get("savfile",0)
                messages = checkfilename(sav_file)
                if messages['error']:

                    return {'messages': messages['show_message']}              

                if  sav_file:
                    
                    sav_file_name = str(sav_file.name[0:4])[0:4]
                    file_path = default_storage.save(f'temp/{self.user}/Savfile/{sav_file_name}.sav', sav_file)
                    
                    print('file_path-->',file_path)
                    shutil.move(file_path
                                , f'{self.datapath["savfile_dir"]}/{sav_file_name}.sav')
                    args={"error":0}
                else:
                
                    messages = ['請選擇sav檔']
                    args={"error":1,"return_value":{"backend_message":"請選擇sav檔",
                                                    "front_message":"請選擇sav檔"}}
                return args
                
            elif upload_what == "dynamic":
                savfilename = self.request.POST.get('year')
                dv_file = self.request.FILES.get('dv_file')
                dll_file = self.request.FILES.get('dll_file')        
                co_gen_file = self.request.FILES.get('co-gen_file')
                renewable_energy_69kV_file = self.request.FILES.get('renewable_energy_69kV_file')

                os.makedirs(f'{self.datapath["dynamic_dir"]}/{savfilename}', exist_ok=True)
                if dv_file != None and dll_file != None and co_gen_file != None: 
                    uploadfilename = dv_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', dv_file)
                    
                    #上傳 dv_file 到B伺服器(單機用move)
                    shutil.move(temp_file_path
                                , f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}")
                    
                    #上傳 dll_file 到B伺服器(單機用move)
                    uploadfilename = dll_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', dll_file)
                    
                    shutil.move(temp_file_path
                                , f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}")
                                       
                    #上傳 co_gen_file 到B伺服器(單機用move)
                    uploadfilename = co_gen_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', co_gen_file)
                    shutil.move(temp_file_path
                                , f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}")

                    
                    uploadfilename = renewable_energy_69kV_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', renewable_energy_69kV_file)
                    shutil.move(temp_file_path
                                , f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}")                    
                    return {"messages":['正在執行中...請稍後']} 

            elif upload_what == "writing_data":

                if os.path.exists(f'temp/{self.user}/writedata/area.idv'):
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').area()

                if os.path.exists(f'temp/{self.user}/writedata/zone.idv'):
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').zone()

                if os.path.exists(f'temp/{self.user}/writedata/owner.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').owner()

                if os.path.exists(f'temp/{self.user}/writedata/bus.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').bus()

                if os.path.exists(f'temp/{self.user}/writedata/machine.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').machine()

                if os.path.exists(f'temp/{self.user}/writedata/load.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').load()

                if os.path.exists(f'temp/{self.user}/writedata/branch.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').branch()

                if os.path.exists(f'temp/{self.user}/writedata/twowinding_edit.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').twowinding_edit()

                if os.path.exists(f'temp/{self.user}/writedata/twowinding.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').twowinding()

                if os.path.exists(f'temp/{self.user}/writedata/threewinding.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').threewinding()

                if os.path.exists(f'temp/{self.user}/writedata/threewinding_winding.idv'):                
                    CreateWriteSavTempFile(f'temp/{self.user}/writedata').threewinding_winding()                                                            


                #移動temp.idv到B伺服器(單機用move)
                os.makedirs(f'{self.datapath["idvfile_dir"]}', exist_ok=True)
                shutil.move(f'temp/{self.user}/writedata/temp.idv'
                            , f"{self.datapath['idvfile_dir']}/temp.idv"
                            )
                fileprocess.remove_dir(f'temp/{self.user}/writedata')
                
            else:
                return {"messages":[f"沒有{upload_what}這個按鈕 有問題!!"]}
                
    def upload_powerflow(self, upload_what):          
        sav_file = self.request.FILES.get("savfile",0)
        messages = checkfilename(sav_file)
        if messages['error']:

            args = {'messages': messages['show_message']}
            return args              

        if  sav_file:
            
            sav_file_name = str(sav_file.name[0:4])[0:4]
            temp_path = f'temp/{self.user}/Savfile/Powerflow/{sav_file_name}.sav'
            file_path = default_storage.save(temp_path, sav_file)
            print('file_path-->',file_path)
            shutil.move(file_path
                        , f'{self.datapath["savfile_dir"]}/Powerflow/{sav_file_name}.sav')

            messages = ['正在上傳中...請稍後']
            args={"messages":messages}
        else:
        
            messages = ['請選擇sav檔']
            args={"messages":messages}
        return args         


    def upload_errorcircuit(self, upload_what):          
        sav_file = self.request.FILES.get("savfile",0)
        # messages = checkfilename(sav_file)
        # if messages['error']:

        #     args = {'messages': messages['show_message']}
        #     return args              

        if  sav_file:
            
            sav_file_name = str(sav_file.name[0:5])[0:5]
            temp_path = f'temp/{self.user}/Savfile/FaultCurrent/{sav_file_name}.sav'
            file_path = default_storage.save(temp_path, sav_file)
            
            print('file_path-->',file_path)
            shutil.move(file_path
                        , f'{self.datapath["savfile_dir"]}/FaultCurrent/{sav_file_name}.sav')


            messages = ['正在上傳中...請稍後']
            args={"messages":messages}
        else:
        
            messages = ['請選擇sav檔']
            args={"messages":messages}
        return args



    def delete_sav(self):
        savfilelist = self.request.POST.getlist('year')
        if savfilelist==[]:
            return {'messages':["請至少選擇一個檔案"]}

        params = {  "savfilelist":savfilelist
                    ,"savfile_dir":self.datapath["savfile_dir"]
                    ,"idvfile_dir":self.datapath["idvfile_dir"]
                    ,"powerflow_dir":self.datapath["powerflow_dir"]
                    ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                    ,"dynamic_dir":self.datapath["dynamic_dir"]
                    ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                    ,"filter_dir":self.datapath["filter_dir"]

                }
        
        Delete().action_of_delete_savfile(params)
        return {'messages':['刪除成功']}


    def delete_sav_powerflow(self, savfilelist):


        params = {  "savfilelist":savfilelist
                    ,"savfile_dir":f'{self.datapath["savfile_dir"]}/Powerflow'
                    ,"idvfile_dir":self.datapath["idvfile_dir"]
                    ,"powerflow_dir":self.datapath["powerflow_dir"]
                    ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                    ,"dynamic_dir":self.datapath["dynamic_dir"]
                    ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                    ,"filter_dir":f'{self.datapath["filter_dir"]}/Powerflow'

                }
        Delete().action_of_delete_savfile(params)
        return '刪除成功'




    def delete_sav_errorcircuit(self):
        savfilelist = self.request.POST.getlist('year')
        if savfilelist==[]:
            return {'messages':["請至少選擇一個檔案"]}

        params = {  "savfilelist":savfilelist
                    ,"savfile_dir":f'{self.datapath["savfile_dir"]}/FaultCurrent'
                    ,"idvfile_dir":self.datapath["idvfile_dir"]
                    ,"powerflow_dir":self.datapath["powerflow_dir"]
                    ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                    ,"dynamic_dir":self.datapath["dynamic_dir"]
                    ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                    ,"filter_dir":f'{self.datapath["filter_dir"]}/FaultCurrent'

                }
        Delete().action_of_delete_savfile(params)
        return {'messages':['刪除成功']}
         

    def execute_idvfile(self):
        messages = ''

        if self.request.method == 'POST':
            '''
                Step 1 : 先刪除這個使用者的filter資料夾 
                Step 2 : 先建立SavFile, RawFile, IDV 資料夾

            '''   
            savfilelist = self.request.POST.getlist('year')     
            print('yearlist = ',savfilelist)
            #沒有勾選 -->return         
            if savfilelist==[]:
                args = {'messages':['至少勾選一個年份']}
                return args



            params = {"username": self.user,
                        "savfilelist":savfilelist,
                        "idv_path":f'{self.userdir}/excute_idvfile/temp.idv',
                        "user_dir": self.datapath["user_dir"],
                        "source_dir": self.datapath["savfile_dir"],
                        "target_dir": self.datapath["savfile_dir"]
                        }
            response = requests.get(f"{self.url}/idv/"
                                    , params=params
                                    ,proxies = self.proxies
                                    )
            # print(response.text)
            # 請求成功回傳資料
            if response.status_code == 200:
                messages = response.json()
                print(messages)


                args = messages["messages"]
            else:    
                args={"messages":"失敗"}
        else:
            logger.info('USER: %s ACTION: %s MESSAGE: %s',
                            self.user,   '上傳失敗', '使用者沒有選擇idv檔')                 
            messages = ['請選擇sav檔']
            args={"messages":messages}
                


        return args  

    def write_idvfile_content_to_savfile(self, savfilelist):

        cache.delete(get_cache_key(self.user, 'branch'))
        cache.delete(get_cache_key(self.user, 'twowinding'))
        cache.delete(get_cache_key(self.user, 'threewinding'))
        cache.delete(get_cache_key(self.user, 'threewinding_winding'))

        

        message = []
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")
        str_current_datetime = str(current_datetime)        
        for savfile in savfilelist:


            args =  f" --Source_SavFileName {self.datapath['savfile_dir']}/{savfile}.sav"\
                    f" --Target_SavFileName {self.datapath['savfile_dir']}/{savfile}_{str_current_datetime}.sav"\
                    f" --User_Folder {self.datapath['user_dir']}"\
                    f" --User_name {self.user}"\
                    f" --IDV_Path {self.datapath['user_dir']}/IDV/temp.idv"
            

            cmd = fileprocess.run_pyfile_by_execmd(python_location='python'
                                        ,pyfile='webinterface/src/run_writingdata_to_sav.py'
                                        ,args=args)
            print(cmd)
            result = fileprocess.execCmd(cmd)
            # print(result)
            if result['error']:
                print(result)
                message.append(f'{savfile} 失敗')
            else:
                message.append(f'{savfile} 成功')
        
        return {"messages":['，'.join(message)],'temp_idvpath':f'temp/{self.user}/writedata/temp.idv'}
        ## savfilelist = self.request.POST.getlist('year')

        # params = {"username": self.user,
        #             "savfilelist":savfilelist,
        #             "idv_path":f'{self.datapath["user_dir"]}/IDV/temp.idv',
        #             "user_dir": self.datapath["user_dir"],
        #             "source_dir": self.datapath["savfile_dir"],
        #             "target_dir": self.datapath["savfile_dir"]
        #             }
        # print(params)            
        # response = requests.get(f"{self.url}/write_data_to_savfile/"
        #                         , params=params
        #                         )
        # if response.status_code == 200:

        #     return {"messages":response.json()["results"],'temp_idvpath':f'temp/{self.user}/writedata/temp.idv'}


        # else:    
        #     return []                                        


    def run_powerflow(self):

        yearlist = self.request.POST.getlist('year')
        # convergence_thread_hold = self.request.POST.get('convergence_thread_hold')
        
        zone = self.request.POST.getlist('chekbox_Zone')
        area = self.request.POST.getlist('chekbox_area')
        # minbasekv = self.request.POST.get('minbasekv')
        # maxbasekv = self.request.POST.get('maxbasekv')
        
        N1_161KV = self.request.POST.get('N1_161KV')
        N1_345KV = self.request.POST.get('N1_345KV')
        N2_345KV = self.request.POST.get('N2_345KV')
        args={}
        # if N1_161KV==None and N1_345KV==None and N2_345KV==None:
        #     args = {'messages':['161KV_N1、345KV_N1、345KV_N2至少勾選一個']}
        #     return args

        if N1_161KV=="N1_161KV":
            confile_type = "N1"
            case_sub = "161KV_N-1"
            targetfolder = f'{self.datapath["powerflow_dir"]}/'
            print(targetfolder)
            minbasekv = 161.0
            maxbasekv = 161.0

        elif N1_345KV=="N1_345KV":
            confile_type = "N1"
            case_sub = "345KV_N-1"
            targetfolder = f'{self.datapath["powerflow_dir"]}'
            minbasekv = 345.0
            maxbasekv = 345.0
            print('case_sub -->',case_sub)

        elif N2_345KV=="N2_345KV":
            confile_type = "N2"
            case_sub = "345KV_N-2"
            targetfolder = f'{self.datapath["powerflow_dir"]}'
            minbasekv = 345.0
            maxbasekv = 345.0
        else:
            pass

 
        return_of_RUN_PowerFlow = run_powerflow.RUN_PowerFlow(username=self.user
                                                            ,yearlist=yearlist
                                                            ,TargetFolder = targetfolder
                                                            ,area=area
                                                            ,zone=zone                                                            
                                                            ,minbasekv=minbasekv
                                                            ,maxbasekv=maxbasekv
                                                            ,confile_type=case_sub) 

        args['powerflow_messages']  = { 'mismatch':[f'{front_value["content"]}' for front_value in return_of_RUN_PowerFlow["return_value"]]
            ,'messages':['執行PowerFlow完成']}                                                                                          

        '''
                               分歧開始
        '''
        if  N1_161KV=="N1_161KV":
            return_of_sub = run_powerflow_subline_161n1.Run_Powerflow_of_subline(source_Folder=f'{self.datapath["savfile_dir"]}/Powerflow'
                                                                        ,powerflow_folder=self.datapath["powerflow_dir"]
                                                                        ,user=self.user
                                                                        ,Sav_File=yearlist
                                                                        ,area_num=area
                                                                        ,zone_num=zone
                                                                        ,maxbasekv=maxbasekv
                                                                        ,minbasekv=minbasekv
                                                                        ,confile_type=case_sub
                                                                        )
        elif N1_345KV=="N1_345KV":
            return_of_sub = run_powerflow_subline_345n1.Run_Powerflow_of_subline(source_Folder=f'{self.datapath["savfile_dir"]}/Powerflow'
                                                                        ,powerflow_folder=self.datapath["powerflow_dir"]
                                                                        ,user=self.user
                                                                        ,Sav_File=yearlist
                                                                        ,area_num=area
                                                                        ,zone_num=zone
                                                                        ,maxbasekv=maxbasekv
                                                                        ,minbasekv=minbasekv
                                                                        ,confile_type=case_sub
                                                                        )
        elif N2_345KV=="N2_345KV":  
            return_of_sub = run_powerflow_subline_345n2.Run_Powerflow_of_subline(source_Folder=f'{self.datapath["savfile_dir"]}/Powerflow'
                                                                        ,powerflow_folder=self.datapath["powerflow_dir"]
                                                                        ,user=self.user
                                                                        ,Sav_File=yearlist
                                                                        ,area_num=area
                                                                        ,zone_num=zone
                                                                        ,maxbasekv=maxbasekv
                                                                        ,minbasekv=minbasekv
                                                                        ,confile_type=case_sub
                                                                        )
        else:
            pass  
        if return_of_sub['error']:      
            args["powerflow_sub_messages"] = { 'mismatch':'執行錯誤'
            ,'messages':['執行分岐錯誤']}   
        else:                              
            print('return_of_sub -->',return_of_sub["return_value"])
            mismatch_sub = []
            for front_value in return_of_sub["return_value"]:
                for sub_value in front_value:
                    mismatch_sub.append(sub_value["content"])        
            args["powerflow_sub_messages"] = { 'mismatch':mismatch_sub
                ,'messages':['執行PowerFlow完成']}                         
        """
            測試區塊
        """
        # args["powerflow_sub_messages"] = { 'mismatch':['測試PowerFlowsub完成']
        #     ,'messages':['執行PowerFlow完成']} 

        return args
                
    def run_errorcircuit(self):

        #Step 1 : 檢查有沒有勾選檔案
        savefiles = self.request.POST.getlist('year')     


        #Step 2 : 檢查有沒有填入min和max basekV limit
        minbasekv = self.request.POST.get('minbasekv')
        maxbasekv = self.request.POST.get('maxbasekv')
        #沒有輸入 -->return 到errorcircuit頁面  
        if minbasekv=="" or maxbasekv=="":
            args = {'messages':['請輸入min和max basekV limit']}
            return args

        #Step 3 : 檢查有沒有勾選area 或 zone 或 owner 
        area = self.request.POST.getlist('checkbox_area')
        print('len(area) = ',len(area))

        zone = self.request.POST.getlist('chekbox_Zone')
        print('len(zone) = ',len(zone))

        owner = self.request.POST.getlist('chekbox_Owner')
        print('len(owner)',len(owner))
        #沒有勾選 -->return 到errorcircuit頁面
        if area==[] and zone==[] and owner==[]:
            args = {'messages':['至少選擇一個area 或 zone 或 owner']}
            return args

        # params = {  "username":self.user,
        #             "savefiles": savefiles,
        #             "savfile_dir":f'{self.datapath["savfile_dir"]}/ErrorCircuit',
        #             "errorcircuit_dir":self.datapath["errorcircuit_dir"],
        #             "area":area,
        #             "zone":zone,
        #             "owner":owner,
        #             "minbasekv":minbasekv,
        #             "maxbasekv":maxbasekv,
        #             }
        result = run_error_circuit.RUN_ErrorCircuit( username = self.user
                                    ,savfiledir = f'{self.datapath["savfile_dir"]}/FaultCurrent'
                                    ,savefiles = savefiles
                                    ,errorcircuitdir = self.datapath["errorcircuit_dir"]
                                    ,logpath = f'Log/{self.user}/ErrorCircuitFunction_log/'
                                    ,area=area
                                    ,zone=zone
                                    ,owner=owner
                                    ,minbasekv=minbasekv
                                    ,maxbasekv=maxbasekv)
                    
        if result["error"]:
            logger.error(result["which_log"]) 
            print(' result[return_value] >> ', result['return_value'])


            args = { 'mismatch':[f'{front_value["content"]}' for front_value in result["return_value"]]
                    ,'messages':['執行失敗'] } 
        else:
            
                
            args = { 'mismatch':[f'{front_value["content"]}' for front_value in result["return_value"]], 
                'messages':['執行故障電流完成']}                          

        return {'errorcircuit_messages':args} 

    def run_dynamic(self):

        
        '''
            Step 1 : 檢查有沒有勾選檔案 
                        -->沒有就回到dynamic頁面

            Step 2 : 檢查有沒有上傳和dyr dll con-gen 
                        -->沒有就回到dynamic頁面

            Step 3 : 檢查有沒有勾選area 或 zone 或 owner 
                        -->沒有就回到dynamic頁面

            Step 4 : 執行故障電流
        '''
        
        #Step 1 : 檢查有沒有勾選檔案
        savfilename = self.request.POST.get('year')    

        #沒有勾選 -->return 到errorcircuit頁面          
        if savfilename==[] :
            
            args = {'messages':['請勾選一個年份']}
            return args  

        dv_file = self.request.FILES.get('dv_file')
        dll_file = self.request.FILES.get('dll_file')        
        co_gen_file = self.request.FILES.get('co-gen_file')
        renewable_energy_69kV_file = self.request.FILES.get('renewable_energy_69kV_file')


        selected_machine_buses = self.request.POST.get('selected_machine_buses')
        
        selected_machine_busnumber = [] 
        selected_machine_busid = []
        for machine_busnum_busname in selected_machine_buses.split(','):

            selected_machine_busnumber.append(machine_busnum_busname.split('-')[0])
            selected_machine_busid.append(machine_busnum_busname.split('-')[-1])

        # selected_machine_busnumber = ' '.join(selected_machine_busnumber) 
        

        dynamic_bus_fault = self.request.POST.get('dynamic_bus_fault')
        ic(list(self.request.POST.keys()))

        dynamic_bus_fault_num = dynamic_bus_fault.split('-')[0]


        selected_dynamic_trip_lines = self.request.POST.get('selected_trip_lines')
        
        selected_dynamic_trip_line_num= []

        circuit_id_for_elected_dynamic_trip_line = []

        for trip_line_num in selected_dynamic_trip_lines.split(','):

            selected_dynamic_trip_line_num.append(trip_line_num.split('-')[0])

            circuit_id_for_elected_dynamic_trip_line.append(trip_line_num.split('-')[-1])

        selected_dynamic_trip_line_num = ' '.join(selected_dynamic_trip_line_num) 

        circuit_id_for_elected_dynamic_trip_line = ' '.join(circuit_id_for_elected_dynamic_trip_line)

        ic("selected_machine_busnumber >> ",selected_machine_busnumber)
        ic("dynamic_bus_fault_num >> ",dynamic_bus_fault_num)
        ic("dynamic_trip_line_num >> ",selected_dynamic_trip_line_num)
        ic("circuit_id_for_elected_dynamic_trip_line >> ",circuit_id_for_elected_dynamic_trip_line)

        # print(self.request.POST.keys())
        # initial_time = self.request.POST.get('initial_time')
        initial_time = 1.0 #固定1秒
        bus_fault_time = self.request.POST.get('bus_fault_time') #對應到網頁的 trip_line_time
        trip_line_time = self.request.POST.get('trip_line_time') #對應到網頁的 clear_fault_time
        clear_fault_time = self.request.POST.get('clear_fault_time')#對應到網頁的 模擬時間
        
        ic("initial_time >> ",initial_time)
        ic("bus_fault_time >> ",bus_fault_time)
        ic("trip_line_time >> ",trip_line_time)
        ic("clear_fault_time >> ",clear_fault_time)



        # params = {  "username":self.user,
        #             "result_dir": f'{self.datapath["dynamic_dir"]}/{savfilename}',
        #             "savfile_dir":f'{self.datapath["savfile_dir"]}/Powerflow',
        #             "dynamic_dir":self.datapath["dynamic_dir"],
        #             "savfilename":savfilename,
        #             "dv_file":f'{self.datapath["dynamic_dir"]}/{savfilename}/{dv_file.name}',
        #             "dll_file":f'{self.datapath["dynamic_dir"]}/{savfilename}/{dll_file.name}',
        #             "co_gen_file":f'{self.datapath["dynamic_dir"]}/{savfilename}/{co_gen_file.name}',
        #             "selected_machine_busnumber":selected_machine_busnumber,
        #             "selected_machine_busid":selected_machine_busid,
        #             "dynamic_bus_fault_num":dynamic_bus_fault_num,
        #             "selected_dynamic_trip_line_num":selected_dynamic_trip_line_num,
        #             "circuit_id_for_elected_dynamic_trip_line":circuit_id_for_elected_dynamic_trip_line,
        #             "initial_time":initial_time,
        #             "bus_fault_time":bus_fault_time,
        #             "trip_line_time":trip_line_time,
        #             "clear_fault_time":clear_fault_time,
                    
                    
        #             }
        result = run_dynamic.RUN_dynamic( username = self.user
                                    ,resultdir = f'{self.datapath["dynamic_dir"]}/{savfilename}'
                                    ,savfile_Folder = f'{self.datapath["savfile_dir"]}/Powerflow'
                                    ,savfilename = savfilename #f"{year}.sav"
                                    ,dv_file = f'{self.datapath["dynamic_dir"]}/{savfilename}/{dv_file.name}'#f'User/{self.user}/Dynamic/{year}/{dv_file}'
                                    ,dll_file = f'{self.datapath["dynamic_dir"]}/{savfilename}/{dll_file.name}'#f'User/{self.user}/Dynamic/{year}/{dll_file}'
                                    ,co_gen_file = f'{self.datapath["dynamic_dir"]}/{savfilename}/{co_gen_file.name}'#f'User/{self.user}/Dynamic/{year}/{co_gen_file}'  
                                    ,renewable_energy_69kV_file = f'{self.datapath["dynamic_dir"]}/{savfilename}/{renewable_energy_69kV_file.name}'#f'User/{self.user}/Dynamic/{year}/{co_gen_file}'

                                    ,selected_machine_busnumber = selected_machine_busnumber
                                    ,selected_machine_busid = selected_machine_busid
                                    ,dynamic_bus_fault_num = dynamic_bus_fault_num
                                    ,selected_dynamic_trip_line_num = selected_dynamic_trip_line_num
                                    ,circuit_id_for_elected_dynamic_trip_line=circuit_id_for_elected_dynamic_trip_line
                                    ,initial_time = initial_time
                                    ,bus_fault_time = bus_fault_time
                                    ,trip_line_time = trip_line_time
                                    ,clear_fault_time = clear_fault_time
                                    )
        ic("result >> ",result)
        args={} 
        # mismatch = " errocircut "
        if result["error"]:
            
            ic(' result[return_value] >> ', result['return_value'])


            args["dynamic_messages"]={ 'mismatch':[result["return_value"]]
                    ,'messages':['執行失敗'] } 
        else:
            
            ic('result -->',result)    
            args["dynamic_messages"] = { 'mismatch':[result["return_value"]], 
                'messages':['執行暫態完成']}
                    
        # response = requests.get(f"{self.url}/dynamic/"
        #                         , params=params
        #                         # , proxies = server_settings["proxies"]
        #                         )
                                
        # if response.status_code == 200:
        #     messages = response.json()
        #     print('messages = ',messages)
        #     args["dynamic_messages"] = args
        # else:    
        #     args["dynamic_messages"] = "失敗"

        return args

       