
import os
import json
import requests
from django.core.files.storage import default_storage
from django.core.cache import cache

from webinterface.src import fileprocess
from webinterface.src.base import how_many_sav_file
from webinterface.src.base.check_filename import checkfilename
from webinterface.src.cache_data_type import get_cache_key

# from .run import run
from .datapath import data_path_of_user_on_server
from .readconfig import read_config


class MyFunctions:
    def __init__(self, request):
        self.request = request
        self.user = str(request.user)
        self.datapath = data_path_of_user_on_server(self.user)
        self.server_settings = read_config()
        self.url = f"http://{self.server_settings['server_host']}:{self.server_settings['server_port']}"
        
    def filter(self, sav_file_name):

        print('sav_file_name in filter = ',sav_file_name)
        params = {  "savefile":sav_file_name,
                    "savfile_dir":self.datapath["savfile_dir"],
                    "target_dir": self.datapath["filter_dir"],
                    "filter_dir": self.datapath["filter_dir"],                  
                    "user":self.user,
                    }
                
        print('my functions yearlist = ', params)            
        response = requests.get(f"{self.url}/filter_all/"
                                , params=params
                                
                                )   
        if response.status_code == 200:
            messages = response.json()
            print('messages = ',messages)
            args = messages["messages"]                        
        else:
            print(response.status_code)
            args={"messages":"上傳失敗"}
        # args={"messages":"上傳完成"}

                                                
        return args

    def filter_powerflow(self, sav_file_name):

        print('sav_file_name in filter = ',sav_file_name)
        params = {  "savefile":sav_file_name,
                    "savfile_dir":f'{self.datapath["savfile_dir"]}/PowerFlow',
                    "target_dir": f'{self.datapath["filter_dir"]}/PowerFlow',
                    "filter_dir": f'{self.datapath["filter_dir"]}/PowerFlow',                  
                    "user":self.user,
                    }
                
        print('my functions yearlist = ', params)            
        response = requests.get(f"{self.url}/filter_all/"
                                , params=params
                                
                                )   
        if response.status_code == 200:
            messages = response.json()
            print('messages = ',messages)
            args = messages["messages"]                        
        else:
            print(response.status_code)
            args={"messages":"上傳失敗"}
        # args={"messages":"上傳完成"}

                                                
        return args

    def filter_errorcircuit(self, sav_file_name):

        print('sav_file_name in filter = ',sav_file_name)
        params = {  "savefile":sav_file_name,
                    "savfile_dir":f'{self.datapath["savfile_dir"]}/ErrorCircuit',
                    "target_dir": f'{self.datapath["filter_dir"]}/ErrorCircuit',
                    "filter_dir": f'{self.datapath["filter_dir"]}/ErrorCircuit',                  
                    "user":self.user,
                    }
                
        print('my functions yearlist = ', params)            
        response = requests.get(f"{self.url}/filter_all/"
                                , params=params
                                
                                )   
        if response.status_code == 200:
            messages = response.json()
            print('messages = ',messages)
            args = messages["messages"]                        
        else:
            print(response.status_code)
            args={"messages":"上傳失敗"}
        # args={"messages":"上傳完成"}

                                                
        return args

    def upload(self, upload_what):
        messages = ''
        
        if self.request.method == 'POST':
            '''
                Step 1 : 先刪除這個使用者的filter資料夾 
                Step 2 : 先建立SavFile, RawFile, IDV 資料夾

            '''   
            if "upload" in self.request.POST:


                #先建立這個使用者的SavFile, RawFile, IDV 資料夾             
                # os.makedirs(f'{self.savfile_dir}', exist_ok = True)                
                # os.makedirs(f'{self.idvfile_dir}', exist_ok = True)
                # os.makedirs(f'{self.dynamic_dir}', exist_ok = True)
                

                sav_file = self.request.FILES.get("savfile",0)
                messages = checkfilename(sav_file)
                if not messages['ifok']:

                    args = {'messages': messages['show_message']}
                    return args              

                if  sav_file:
                    
                    sav_file_name = str(sav_file.name[0:4])[0:4]
                    file_path = default_storage.save(f'temp/{self.user}/{sav_file_name}.sav', sav_file)
                    
                    params = {  "savfile_path":f"{self.datapath['savfile_dir']}/{sav_file_name}.sav"
                                ,"sav_file_name":f"{sav_file_name}"
                                ,"savfile_dir":self.datapath["savfile_dir"]
                                ,"idvfile_dir":self.datapath["idvfile_dir"]
                                ,"powerflow_dir":self.datapath["powerflow_dir"]
                                ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                                ,"dynamic_dir":self.datapath["dynamic_dir"]
                                ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                                ,"filter_dir":self.datapath["filter_dir"]

                            }
                    
                    # 準備上傳到B伺服器
                    with open(default_storage.path(file_path), 'rb') as f:
                        files = {'file': (sav_file_name, f)}
                        response = requests.post(f"{self.url}/upload_savfile/"
                                    , files=files
                                    ,data={'params': json.dumps(params)}) 

                    print(response.text)
                    fileprocess.remove_file(f'temp/{self.user}/{sav_file_name}.sav') 


                    if response.status_code == 200:
                        
                        return response.json()
                    else:    
                                            
                        return {"messages":["Server Error"]}
                else:
                
                    messages = ['請選擇sav檔']
                    args={"messages":messages}
                return args
                
            elif upload_what == "dynamic":
                savfilename = self.request.POST.get('year')
                dv_file = self.request.FILES.get('dv_file')
                dll_file = self.request.FILES.get('dll_file')        
                co_gen_file = self.request.FILES.get('co-gen_file')

                
                if not (dv_file==None or dll_file==None or co_gen_file==None): 
                    uploadfilename = dv_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', dv_file)
                    params = {"dynamicfile_dir":f"{self.datapath['dynamic_dir']}/{savfilename}",
                                "dynamicfile_path":f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}"
                            }
                    # 準備上傳到B伺服器
                    with open(default_storage.path(temp_file_path), 'rb') as f:
                        files = {'file': (uploadfilename, f)}
                        response = requests.post(f"{self.url}/upload_dynamicfile/"
                                    , files=files
                                    ,data={'params': json.dumps(params)}) 

                    print(response.json())   
                    fileprocess.remove_file(temp_file_path)

                    uploadfilename = dll_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', dll_file)
                    params ["dynamicfile_path"] = f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}"
                    # 準備上傳到B伺服器
                    with open(default_storage.path(temp_file_path), 'rb') as f:
                        files = {'file': (uploadfilename, f)}
                        response = requests.post(f"{self.url}/upload_dynamicfile/"
                                    , files=files
                                    ,data={'params': json.dumps(params)}) 

                    print(response.json())   
                    fileprocess.remove_file(temp_file_path)

                    uploadfilename = co_gen_file.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', co_gen_file)
                    params["dynamicfile_path"] = f"{self.datapath['dynamic_dir']}/{savfilename}/{uploadfilename}"
                    # 準備上傳到B伺服器
                    with open(default_storage.path(temp_file_path), 'rb') as f:
                        files = {'file': (uploadfilename, f)}
                        response = requests.post(f"{self.url}/upload_dynamicfile/"
                                    , files=files
                                    ,data={'params': json.dumps(params)})   
                    print(response.json())
                    fileprocess.remove_file(temp_file_path)

                    messages = ['正在執行中...請稍後']
                    args={"messages":messages}
                    return args 
            elif upload_what == "idvfile":  
                idvfile = self.request.FILES.get("idvfile",0)
                if  idvfile:
                    uploadfilename = idvfile.name
                    temp_file_path = default_storage.save(f'temp/{self.user}/{uploadfilename}', idvfile)
                    params = {"excute_idvfile_dir":f"{self.datapath['excute_idvfile_dir']}",
                                "excute_idvfile_path":f"{self.datapath['excute_idvfile_dir']}/temp.idv"
                            }
                    # 準備上傳到B伺服器
                    with open(default_storage.path(temp_file_path), 'rb') as f:
                        files = {'file': (uploadfilename, f)}
                        response = requests.post(f"{self.url}/upload_idvfile/"
                                    , files=files
                                    ,data={'params': json.dumps(params)}) 

                    print(response.json())   
                    fileprocess.remove_file(temp_file_path)            
                      
                else:
                    return {"messages":[f"請選擇一個idv檔"]}   

            elif upload_what == "writing_data":        

                writing_data_idvfile = f'temp/{self.user}/writedata/temp.idv'
                params = {"idvfile_path":f"{self.datapath['idvfile_dir']}/temp.idv",
                            "idvfile_dir":f"{self.datapath['idvfile_dir']}"
                        }  
                print('writing_data_idvfile -->',writing_data_idvfile)                      
                with open(writing_data_idvfile, 'rb') as f:
                    files = {'file': ('temp.idv', f)}
                    response = requests.post(f"{self.url}/upload_idvfile_of_writata/"
                                    , files=files
                                    ,data={'params': json.dumps(params)}
                                    ) 

                print(response.json())   
                # fileprocess.remove_file(writing_data_idvfile)      
                messages = ['正在執行中...請稍後']
                args={"messages":messages}
                
            else:
                return {"messages":[f"沒有{upload_what}這個按鈕 有問題!!"]}
    def upload_powerflow(self, upload_what):          
        sav_file = self.request.FILES.get("savfile",0)
        messages = checkfilename(sav_file)
        if not messages['ifok']:

            args = {'messages': messages['show_message']}
            return args              

        if  sav_file:
            
            sav_file_name = str(sav_file.name[0:4])[0:4]
            temp_path = f'temp/{self.user}/Savfile/Powerflow/{sav_file_name}.sav'
            file_path = default_storage.save(temp_path, sav_file)
            
            params = {  "savfile_path":f"{self.datapath['savfile_dir']}/Powerflow/{sav_file_name}.sav"
                        ,"sav_file_name":f"{sav_file_name}"
                        ,"savfile_dir":f"{self.datapath['savfile_dir']}/Powerflow"
                        ,"idvfile_dir":self.datapath["idvfile_dir"]
                        ,"powerflow_dir":self.datapath["powerflow_dir"]
                        ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                        ,"dynamic_dir":self.datapath["dynamic_dir"]
                        ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                        ,"filter_dir":f"{self.datapath['filter_dir']}/Powerflow"

                    }
            
            # 準備上傳到B伺服器
            with open(default_storage.path(file_path), 'rb') as f:
                files = {'file': (sav_file_name, f)}
                response = requests.post(f"{self.url}/upload_savfile/"
                            , files=files
                            ,data={'params': json.dumps(params)}) 

            print(response.text)
            fileprocess.remove_file(temp_path) 


            messages = ['正在上傳中...請稍後']
            args={"messages":messages}
        else:
        
            messages = ['請選擇sav檔']
            args={"messages":messages}
        return args         


    def upload_errorcircuit(self, upload_what):          
        sav_file = self.request.FILES.get("savfile",0)
        messages = checkfilename(sav_file)
        if not messages['ifok']:

            args = {'messages': messages['show_message']}
            return args              

        if  sav_file:
            
            sav_file_name = str(sav_file.name[0:4])[0:4]
            temp_path = f'temp/{self.user}/Savfile/ErrorCircuit/{sav_file_name}.sav'
            file_path = default_storage.save(temp_path, sav_file)
            
            params = {  "savfile_path":f"{self.datapath['savfile_dir']}/ErrorCircuit/{sav_file_name}.sav"
                        ,"sav_file_name":f"{sav_file_name}"
                        ,"savfile_dir":f"{self.datapath['savfile_dir']}/ErrorCircuit"
                        ,"idvfile_dir":self.datapath["idvfile_dir"]
                        ,"powerflow_dir":self.datapath["powerflow_dir"]
                        ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                        ,"dynamic_dir":self.datapath["dynamic_dir"]
                        ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                        ,"filter_dir":f"{self.datapath['filter_dir']}/ErrorCircuit"

                    }
            
            # 準備上傳到B伺服器
            with open(default_storage.path(file_path), 'rb') as f:
                files = {'file': (sav_file_name, f)}
                response = requests.post(f"{self.url}/upload_savfile/"
                            , files=files
                            ,data={'params': json.dumps(params)}) 

            print(response.text)
            fileprocess.remove_file(temp_path) 


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
        

        response = requests.post(f"{self.url}/delete_savfile/"
                    ,data={'params': json.dumps(params)}) 

        if response.status_code == 200:
            
            return response.json()["results"]
        else:    
                                 
            return {"messages":["Server Error"]}

    def delete_sav_powerflow(self):
        savfilelist = self.request.POST.getlist('year')
        if savfilelist==[]:
            return {'messages':["請至少選擇一個檔案"]}

        params = {  "savfilelist":savfilelist
                    ,"savfile_dir":f'{self.datapath["savfile_dir"]}/Powerflow'
                    ,"idvfile_dir":self.datapath["idvfile_dir"]
                    ,"powerflow_dir":self.datapath["powerflow_dir"]
                    ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                    ,"dynamic_dir":self.datapath["dynamic_dir"]
                    ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                    ,"filter_dir":f'{self.datapath["filter_dir"]}/Powerflow'

                }
        

        response = requests.post(f"{self.url}/delete_savfile/"
                    ,data={'params': json.dumps(params)}) 

        if response.status_code == 200:
            
            return response.json()["results"]
        else:    
                                 
            return {"messages":["Server Error"]}


    def delete_sav_errorcircuit(self):
        savfilelist = self.request.POST.getlist('year')
        if savfilelist==[]:
            return {'messages':["請至少選擇一個檔案"]}

        params = {  "savfilelist":savfilelist
                    ,"savfile_dir":f'{self.datapath["savfile_dir"]}/ErrorCircuit'
                    ,"idvfile_dir":self.datapath["idvfile_dir"]
                    ,"powerflow_dir":self.datapath["powerflow_dir"]
                    ,"powerflowsub_dir":self.datapath["powerflowsub_dir"]
                    ,"dynamic_dir":self.datapath["dynamic_dir"]
                    ,"errorcircuit_dir":self.datapath["errorcircuit_dir"]
                    ,"filter_dir":f'{self.datapath["filter_dir"]}/ErrorCircuit'

                }
        

        response = requests.post(f"{self.url}/delete_savfile/"
                    ,data={'params': json.dumps(params)}) 

        if response.status_code == 200:
            
            return response.json()["results"]
        else:    
                                 
            return {"messages":["Server Error"]}            

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
        cache.delete(get_cache_key(self.user, 'area'))
        cache.delete(get_cache_key(self.user, 'zone'))  
        cache.delete(get_cache_key(self.user, 'owner')) 
        cache.delete(get_cache_key(self.user, 'bus'))
        cache.delete(get_cache_key(self.user, 'machine'))     
        cache.delete(get_cache_key(self.user, 'load')) 
        cache.delete(get_cache_key(self.user, 'branch'))
        cache.delete(get_cache_key(self.user, 'twowinding'))
        cache.delete(get_cache_key(self.user, 'threewinding'))
        cache.delete(get_cache_key(self.user, 'threewinding_winding'))
        # savfilelist = self.request.POST.getlist('year')

        params = {"username": self.user,
                    "savfilelist":savfilelist,
                    "idv_path":f'{self.datapath["user_dir"]}/IDV/temp.idv',
                    "user_dir": self.datapath["user_dir"],
                    "source_dir": self.datapath["savfile_dir"],
                    "target_dir": self.datapath["savfile_dir"]
                    }
        print(params)            
        response = requests.get(f"{self.url}/write_data_to_savfile/"
                                , params=params
                                )
        if response.status_code == 200:

            return {"messages":response.json()["results"],'temp_idvpath':f'temp/{self.user}/writedata/temp.idv'}


        else:    
            return []                                        


    def run_powerflow(self):

        yearlist = self.request.POST.getlist('year')
        # convergence_thread_hold = self.request.POST.get('convergence_thread_hold')
        
        zone = self.request.POST.getlist('chekbox_Zone')
        minbasekv = self.request.POST.get('minbasekv')
        maxbasekv = self.request.POST.get('maxbasekv')

        N0 = self.request.POST.get('N0')
        N1 = self.request.POST.get('N1')
        N2 = self.request.POST.get('N2')

        if N0==None and N1==None and N2==None:
            args = {'messages':['N0、N1、N2至少勾選一個']}
            return args
        # print('N0 = ',N0)
        # print('N1 = ',N1)
        # print('N2 = ',N2)
        if N1=="N1" and N2=="N2":
            confile_type = "N1N2"

        elif N1=="N1" and N2==None:
            confile_type = "N1"

        elif N1==None and N2=="N2":
            confile_type = "N2"

        else:
            confile_type = "N0"

        params = {"username": self.user,
                    "yearlist":yearlist,
                    # "convergence_thread_hold":convergence_thread_hold,
                    "zone":zone,
                    "minbasekv":minbasekv,
                    "maxbasekv":maxbasekv,
                    "confile_type":confile_type
                    }
        print(params)     
                       
        response = requests.get(f"{self.url}/powerflow/"
                                , params = params
                                )
        args={} 
                               
        if response.status_code == 200:
            messages = response.json()
            print('messages["messages"]-->',messages["messages"])
            # print('messages = ',messages)
            args['powerflow_messages'] = messages["messages"]
        else:    
            args["powerflow_messages"] = "失敗"

        print('args-->',args)

        params_sub = {"username": self.user,
                    "yearlist":yearlist,
                    "source_Folder":f'{self.datapath["savfile_dir"]}/Powerflow',
                    "powerflow_folder":self.datapath["powerflow_dir"],
                    "zone":zone,
                    "minbasekv":minbasekv,
                    "maxbasekv":maxbasekv,
                    }
        print('params_sub = ',params_sub)     
                       
        response = requests.get(f"{self.url}/powerflowsub/"
                                , params=params_sub
                                )
        if response.status_code == 200:
            messages = response.json()
            # print('messages = ',messages)
            args["powerflow_sub_messages"] = messages["messages"]
        else:    
            args["powerflow_sub_messages"] = "失敗"

        return args                
                
    def run_errorcircuit(self):

        '''
            Step 1 : 檢查有沒有勾選檔案 
                        -->沒有就回到errorcircuit頁面

            Step 2 : 檢查有沒有填入min和max basekV limit 
                        -->沒有就回到errorcircuit頁面

            Step 3 : 檢查有沒有勾選area 或 zone 或 owner 
                        -->沒有就回到errorcircuit頁面

            Step 4 : 執行故障電流
        '''
        
        #Step 1 : 檢查有沒有勾選檔案
        savefiles = self.request.POST.getlist('year')     

        #沒有勾選 -->return 到errorcircuit頁面          
        if savefiles==[]:
            args = {'messages':['至少勾選一個年份']}
            return args

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

        params = {  "username":self.user,
                    "savefiles": savefiles,
                    "savfile_dir":f'{self.datapath["savfile_dir"]}/ErrorCircuit',
                    "errorcircuit_dir":self.datapath["errorcircuit_dir"],
                    "area":area,
                    "zone":zone,
                    "owner":owner,
                    "minbasekv":minbasekv,
                    "maxbasekv":maxbasekv,
                    }
        print(params)
                    
        response = requests.get(f"{self.url}/errorcircuit/"
                                , params=params
                                # , proxies = self.proxies
                                )
        args={}                         
        if response.status_code == 200:
            messages = response.json()
            print('messages = ',messages)
            args["errorcircuit_messages"] = messages["messages"]
        else:    
            args["errorcircuit_messages"] = "失敗"

        return args 

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
            print(len(savfilename))
            args = {'messages':['請勾選一個年份']}
            return args  

        dv_file = self.request.FILES.get('dv_file')
        dll_file = self.request.FILES.get('dll_file')        
        co_gen_file = self.request.FILES.get('co-gen_file')


        selected_machine_buses = self.request.POST.get('selected_machine_buses')
        
        selected_machine_busnumber = [] 
        selected_machine_busid = []
        for machine_busnum_busname in selected_machine_buses.split(','):

            selected_machine_busnumber.append(machine_busnum_busname.split('-')[0])
            selected_machine_busid.append(machine_busnum_busname.split('-')[-1])

        # selected_machine_busnumber = ' '.join(selected_machine_busnumber) 
        

        dynamic_bus_fault = self.request.POST.get('dynamic_bus_fault')
        print(list(self.request.POST.keys()))

        dynamic_bus_fault_num = dynamic_bus_fault.split('-')[0]


        selected_dynamic_trip_lines = self.request.POST.get('selected_trip_lines')
        
        selected_dynamic_trip_line_num= []

        circuit_id_for_elected_dynamic_trip_line = []

        for trip_line_num in selected_dynamic_trip_lines.split(','):

            selected_dynamic_trip_line_num.append(trip_line_num.split('-')[0])

            circuit_id_for_elected_dynamic_trip_line.append(trip_line_num.split('-')[-1])

        selected_dynamic_trip_line_num = ' '.join(selected_dynamic_trip_line_num) 

        circuit_id_for_elected_dynamic_trip_line = ' '.join(circuit_id_for_elected_dynamic_trip_line)

        print("selected_machine_busnumber >> ",selected_machine_busnumber)
        print("dynamic_bus_fault_num >> ",dynamic_bus_fault_num)
        print("dynamic_trip_line_num >> ",selected_dynamic_trip_line_num)
        print("circuit_id_for_elected_dynamic_trip_line >> ",circuit_id_for_elected_dynamic_trip_line)

        # print(self.request.POST.keys())
        initial_time = self.request.POST.get('initial_time')
        bus_fault_time = self.request.POST.get('bus_fault_time')
        trip_line_time = self.request.POST.get('trip_line_time')
        clear_fault_time = self.request.POST.get('clear_fault_time')
        
        print("initial_time >> ",initial_time)
        print("bus_fault_time >> ",bus_fault_time)
        print("trip_line_time >> ",trip_line_time)
        print("clear_fault_time >> ",clear_fault_time)



        params = {  "username":self.user,
                    "result_dir": f'{self.datapath["dynamic_dir"]}/{savfilename}',
                    "savfile_dir":f'{self.datapath["savfile_dir"]}/Powerflow',
                    "dynamic_dir":self.datapath["dynamic_dir"],
                    "savfilename":savfilename,
                    "dv_file":f'{self.datapath["dynamic_dir"]}/{savfilename}/{dv_file.name}',
                    "dll_file":f'{self.datapath["dynamic_dir"]}/{savfilename}/{dll_file.name}',
                    "co_gen_file":f'{self.datapath["dynamic_dir"]}/{savfilename}/{co_gen_file.name}',
                    "selected_machine_busnumber":selected_machine_busnumber,
                    "selected_machine_busid":selected_machine_busid,
                    "dynamic_bus_fault_num":dynamic_bus_fault_num,
                    "selected_dynamic_trip_line_num":selected_dynamic_trip_line_num,
                    "circuit_id_for_elected_dynamic_trip_line":circuit_id_for_elected_dynamic_trip_line,
                    "initial_time":initial_time,
                    "bus_fault_time":bus_fault_time,
                    "trip_line_time":trip_line_time,
                    "clear_fault_time":clear_fault_time,
                    
                    
                    }

                    
        response = requests.get(f"{self.url}/dynamic/"
                                , params=params
                                # , proxies = server_settings["proxies"]
                                )
        args={}                         
        if response.status_code == 200:
            messages = response.json()
            print('messages = ',messages)
            args["dynamic_messages"] = messages["messages"]
        else:    
            args["dynamic_messages"] = "失敗"

        return args

       