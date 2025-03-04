import os
import requests
from django.shortcuts import render, redirect
from django.core.cache import cache

from webinterface.src.base import how_many_sav_file
from webinterface.src.base.load_filter_data import load_filter_data
from webinterface.src.cache_data_type import get_cache_key

from .readconfig import read_config




def get_filter_data(url:str, params:dict):
      
    response = requests.get(url
                            , params=params

                            )
    if response.status_code == 200:

        return response.json()["results"]
    else:    
        return []

def get_filterfile_num(url:str, params:dict):

    response = requests.get(url
                            , params=params

                            )   
    if response.status_code == 200:
        # print(response.json()["results"])
        return response.json()["results"]


    else:    
        return []
    
def get_data_from_psse_backend(url:str, params:dict):

    response = requests.get(url
                            , params=params
                            
                            )   
    if response.status_code == 200:
        return response.json()["results"]


    else:    
        return []


class MyPage:

    def __init__(self, request,*args):
        self.request = request
        self.args = args
        self.user = str(self.request.user)
        self.user_dir = f"../Data/User/{self.user}"
        self.savfile_dir = f"{self.user_dir}/SavFile"
        self.idvfile_dir = f'{self.user_dir}/IDV'
        self.dynamic_dir = f'{self.user_dir}/Dynamic'
        self.powerflow_dir = f'{self.user_dir}/PowerFlow'
        self.powerflowsub_dir = f'{self.user_dir}/PowerFlowSub'
        self.errorcircuit_dir = f'{self.user_dir}/ErrorCircuit'
        self.filter_dir = f'{self.user_dir}/filter'
        self.excute_idvfile_dir = f'{self.user_dir}/excute_idvfile'
        self.server_settings = read_config()
        self.proxies = {
                        'http': None,
                        'https': None,
                    }  
        # self.api_ip = '10.52.15.201'    
        # self.api_port = '800'     
        self.url = f"http://{self.server_settings['server_host']}:{self.server_settings['server_port']}"

        response = requests.get(f"{self.url}/find_savfile"
                                , params={"sourcedir":self.savfile_dir}
                                , proxies=self.proxies
                                )   
        if response.status_code == 200:
            self.savefiles = response.json()
            self.savefiles = self.savefiles["results"]

        else:    
            self.savefiles = [] 

        response = requests.get(f"{self.url}/find_savfile"
                                , params={"sourcedir":f"{self.user_dir}/SavFile/Powerflow"}
                                , proxies=self.proxies
                                )   
        if response.status_code == 200:
            self.savefiles_of_powerflow = response.json()
            self.savefiles_of_powerflow = self.savefiles_of_powerflow["results"]

        else:    
            self.savefiles_of_powerflow = [] 

        response = requests.get(f"{self.url}/find_savfile"
                                , params={"sourcedir":f"{self.user_dir}/SavFile/ErrorCircuit"}
                                , proxies=self.proxies
                                )   
        if response.status_code == 200:
            self.savefiles_of_errorcircuit = response.json()
            self.savefiles_of_errorcircuit = self.savefiles_of_errorcircuit["results"]

        else:    
            self.savefiles_of_errorcircuit = [] 

            
    def home_page(self):

        return render(self.request, 'main.html',{'loginmessage':'登入成功'})
            
    def upload_page(self):
        
        '''
            Step 1 : 找出使用者有上傳哪些 sav 檔案
            Step 2 : 顯示使用者的 sav 檔案

        '''
            
        print('self.args = ',self.args)
        if list(self.args)==[]:
            return render(self.request, 'upload.html', {'username': self.user
                                                ,'years': self.savefiles})
        else:
            args = list(self.args)
            args = args[0]
            

            return render(self.request, 'upload.html', {'username':self.user
                                        ,'years': self.savefiles
                                        ,'messages':args['messages']}) 

    def upload_page_of_upload_powerflow(self):
        '''
            Step 1 : 找出使用者有上傳哪些 sav 檔案
            Step 2 : 顯示使用者的 sav 檔案

        '''
            
        print('self.args = ',self.args)
        if list(self.args)==[]:
            return render(self.request, 'upload_powerflow.html', {'username': self.user
                                                ,'years': self.savefiles_of_powerflow})
        else:
            args = list(self.args)
            args = args[0]
            

            return render(self.request, 'upload_powerflow.html', {'username':self.user
                                        ,'years': self.savefiles_of_powerflow
                                        ,'messages':args['messages']}) 

    def idv_execute_page(self):
        '''
            Step 1 : 找出使用者有上傳哪些 sav 檔案
            Step 2 : 顯示使用者的 sav 檔案
            Step 3 : 上傳使用者的 idv 檔案

        '''
         

        if list(self.args)==[]:
            return render(self.request, 'excute_idvfile.html', {'username': self.user
                                                ,'years':self.savefiles})
        else:
            args = list(self.args)
            print('args = ',args)
            args = args[0]
            
            return render(self.request, 'excute_idvfile.html', {'username':self.user
                                        ,'years':self.savefiles
                                        ,'messages':args})   
    def powerflow_page(self, *args):
        


        # if os.path.isdir(self.savfiledir):      
            # 找出使用者有上傳哪些 sav 檔案
            
            # self.savefiles = list(how_many_sav_file.How_many_SavFile_in_UserFolder(sav_folder=self.savfiledir))
            
        if self.savefiles_of_powerflow== []:
            
            # areas = {'num': [], 'name': []} 
            zones = {'num': [], 'name': []} 
            owners = {'num': [], 'name': []}
        else:

            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                    , params={"sourcedir":f"{self.filter_dir}/Powerflow/zone"}
                                    )
            print('filterfiles',filterfiles)
            # filterfiles = list(how_many_sav_file.How_many_filter_file_in_UserFolder(filterdir=f"{self.filterdir}/zone"))
            params = {"username": self.user,
                        "filterfiles":filterfiles,
                        "userdir": self.user_dir,
                        "savfiledir": self.savefiles_of_powerflow,
                        "targetdir":  f'{self.filter_dir}/Powerflow',
                        "filterdir": f'{self.filter_dir}/Powerflow',
                        "labeltype": "zone",   
                        } 
            print(params)              
            settings = {"proxy":self.server_settings['proxies']}                         
            zones = get_filter_data(url = f"{self.url}/filter_dispaly/",
                                    params = params)
                





        if list(self.args):   

            args = list(self.args)
            args = args[0]

            # mismatch = args.get('mismatch')

            # powerflow_sub = args.get('powerflow_sub')

            messages = args.get('messages') 
            

            
            return   render(self.request, 'powerflow.html', {'username':self.user
                                                    ,'years':self.savefiles_of_powerflow
                                                    # ,'mismatch':mismatch
                                                    # ,'powerflow_sub':powerflow_sub
                                                    ,'messages':messages
                                                    # ,'areas':areas
                                                    ,'zones':zones
                                                    })
        else:

            return   render(self.request, 'powerflow.html', {'username':self.user
                                                            ,'years':self.savefiles_of_powerflow
                                                            ,'zones':zones
                                                            # ,'areas':areas
                                                            })

    def upload_page_of_upload_errorcircuit(self):
        '''
            Step 1 : 找出使用者有上傳哪些 sav 檔案
            Step 2 : 顯示使用者的 sav 檔案

        '''
            
        print('self.args = ',self.args)
        if list(self.args)==[]:
            return render(self.request, 'upload_errorcircuit.html', {'username': self.user
                                                ,'years': self.savefiles_of_errorcircuit})
        else:
            args = list(self.args)
            args = args[0]
            

            return render(self.request, 'upload_errorcircuit.html', {'username':self.user
                                        ,'years': self.savefiles_of_errorcircuit
                                        ,'messages':args['messages']}) 

    def errorcircuit_page(self):


        if self.savefiles == []:
            
            areas = {'num': [], 'name': []} 
            zones = {'num': [], 'name': []} 
            owners = {'num': [], 'name': []}
        else:
            # settings = {"proxy":self.server_settings['proxies']}              
            # filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
            #                         , params={"sourcedir":f"{self.filter_dir}/load"}
            #                         )            
            # params = {"username": self.user,
            #             "filterfiles":filterfiles,
            #             "userdir": self.user_dir,
            #             "savfiledir": self.savfile_dir,
            #             "targetdir": self.filter_dir,
            #             "filterdir": self.filter_dir,
            #             "labeltype": "load",   
            #             }   
                     
            # load = get_filter_data(url = f"{self.url}/filter_dispaly/",
            #                         params = params)

            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                    , params={"sourcedir":f"{self.filter_dir}/ErrorCircuit/area"}
                                    ) 
            params = {"username": self.user,
                        "filterfiles":filterfiles,
                        "userdir": self.user_dir,
                        "savfiledir": f'{self.savfile_dir}/ErrorCircuit',
                        "targetdir": f'{self.filter_dir}/ErrorCircuit',
                        "filterdir": f'{self.filter_dir}/ErrorCircuit',
                        "labeltype": "area",   
                        }   
                     
            areas = get_filter_data(url = f"{self.url}/filter_dispaly/",
                                    params = params)
            print(areas)
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                    , params={"sourcedir":f"{self.filter_dir}/ErrorCircuit/zone"}
                                    )          

            params = {"username": self.user,
                        "filterfiles":filterfiles,
                        "userdir": self.user_dir,
                        "savfiledir": f'{self.savfile_dir}/ErrorCircuit',
                        "targetdir": f'{self.filter_dir}/ErrorCircuit',
                        "filterdir": f'{self.filter_dir}/ErrorCircuit',
                        "labeltype": "zone",   
                        }   
                      
            zones = get_filter_data(url =f"{self.url}/filter_dispaly/",
                                    params = params
                                    )

            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                    , params={"sourcedir":f"{self.filter_dir}/ErrorCircuit/owner"}
                                    )       

            params = {"username": self.user,
                        "filterfiles":filterfiles,
                        "userdir": self.user_dir,
                        "savfiledir": f'{self.savfile_dir}/ErrorCircuit',
                        "targetdir": f'{self.filter_dir}/ErrorCircuit',
                        "filterdir": f'{self.filter_dir}/ErrorCircuit',
                        "labeltype": "owner",   
                        }   
                                   
            owners = get_filter_data(url = f"{self.url}/filter_dispaly/",
                                    params = params
                                    )





        try:

            if list(self.args):   
                
                
                args = list(self.args)
                args = args[0]
                
                mismatch = args.get('mismatch',' ')

                messages = args.get('messages') 

                return   render(self.request, 'errorcircuit.html', {'username': self.user
                                                        ,'years':self.savefiles_of_errorcircuit
                                                        ,'mismatch':mismatch
                                                        ,'messages':messages
                                                        ,"areas":areas
                                                        ,"zones":zones
                                                        ,"owners":owners})
            else:


                return   render(self.request, 'errorcircuit.html', {'username': self.user
                                                                ,'years':self.savefiles_of_errorcircuit
                                                                ,"areas":areas
                                                                ,"zones":zones
                                                                ,"owners":owners})
        except Exception as e:   

            # if os.path.isdir(self.savfiledir):             
            #     years = how_many_sav_file.How_many_SavFile_in_UserFolder(sav_folder=f'{self.savfiledir}')
                
            # else:       
            #     years = [] 


            return   render(self.request, 'errorcircuit.html', {'username':self.user
                                                    ,'messages':['Server Error 請通知系統管理員']
                                                    ,'years':self.savefiles})          


    def dynamic_page(self):



        try:

            if list(self.args):   
                
                args = list(self.args)
                args = args[0]
                

                messages = args.get('messages') 
                

                
                return   render(self.request, 'dynamic.html', {'username': self.user
                                                        ,'years':self.savefiles_of_powerflow
                                                        ,'messages':messages
                                                        })
            else:



                return   render(self.request, 'dynamic.html', {'username': self.user
                                                                ,'years':self.savefiles_of_powerflow

                                                                })
        except Exception as e:   
            print(e)

            return   render(self.request, 'dynamic.html', {'username':self.user
                                                    ,'messages':['Server Error 請通知系統管理員']
                                                    })



    def select_which_Label(self, selection_Label):         
        cache_key = get_cache_key(self.user, selection_Label.lower())   
        temp_labeldata = cache.get(cache_key, [])
 
            



        return render(self.request, f'Create/{selection_Label}.html'
                            , {'USER': self.user
                                # ,'databasecolumn': databasecolumn
                                ,'selection_Label': selection_Label
                                # ,'messages':front_messages
                                # ,'years': self.savefiles 
                                ,'temp_labeldata': temp_labeldata
                                }
                        )

    def prepare_writing_data_page(self): 

        
        # 從緩存獲取已存在的數據(新增label，加在這裡，prepare_writing也要改)
        prepare_writing_data_area = cache.get(get_cache_key(self.user, 'area'), [])
        prepare_writing_data_zone = cache.get(get_cache_key(self.user, 'zone'), [])
        prepare_writing_data_owner = cache.get(get_cache_key(self.user, 'owner'), [])
        prepare_writing_data_bus = cache.get(get_cache_key(self.user, 'bus'), [])
        prepare_writing_data_machine = cache.get(get_cache_key(self.user, 'machine'), [])
        prepare_writing_data_load = cache.get(get_cache_key(self.user, 'load'), [])
        prepare_writing_data_branch = cache.get(get_cache_key(self.user, 'branch'), [])
        prepare_writing_data_twowinding = cache.get(get_cache_key(self.user, 'twowinding'), [])
        prepare_writing_data_threewinding = cache.get(get_cache_key(self.user, 'threewinding'), [])
        prepare_writing_data_threewinding_winding = cache.get(get_cache_key(self.user, 'threewinding_winding'), [])
        
        print(prepare_writing_data_twowinding)
        print(self.args[0])
        print(not self.args[0])
        if self.args[0]:   
            
            
            args = self.args[0]
            print(args)
            messages = args[0].get('messages') 


            
            return   render(self.request, 'Create/prepare_writing.html', {'username': self.user
                                                            ,'years':self.savefiles
                                                            ,'prepare_writing_data_area':prepare_writing_data_area
                                                            ,'prepare_writing_data_zone':prepare_writing_data_zone
                                                            ,'prepare_writing_data_owner':prepare_writing_data_owner
                                                            ,'prepare_writing_data_bus':prepare_writing_data_bus
                                                            ,'prepare_writing_data_machine':prepare_writing_data_machine
                                                            ,'prepare_writing_data_load':prepare_writing_data_load
                                                            ,'prepare_writing_data_branch':prepare_writing_data_branch
                                                            ,'prepare_writing_data_twowinding':prepare_writing_data_twowinding
                                                            ,'prepare_writing_data_threewinding':prepare_writing_data_threewinding
                                                            ,'prepare_writing_data_threewinding_winding':prepare_writing_data_threewinding_winding
                                                            ,'messages':messages
                                                            })
        else:
          
            messages = []
            return   render(self.request, 'Create/prepare_writing.html', {'username': self.user
                                                            ,'years':self.savefiles
                                                            ,'prepare_writing_data_area':prepare_writing_data_area
                                                            ,'prepare_writing_data_zone':prepare_writing_data_zone
                                                            ,'prepare_writing_data_owner':prepare_writing_data_owner
                                                            ,'prepare_writing_data_bus':prepare_writing_data_bus  
                                                            ,'prepare_writing_data_machine':prepare_writing_data_machine                                                          
                                                            ,'prepare_writing_data_load':prepare_writing_data_load
                                                            ,'prepare_writing_data_branch':prepare_writing_data_branch
                                                            ,'prepare_writing_data_twowinding':prepare_writing_data_twowinding
                                                            ,'prepare_writing_data_threewinding':prepare_writing_data_threewinding
                                                             ,'prepare_writing_data_threewinding_winding':prepare_writing_data_threewinding_winding
                                                            ,'messages':messages
                                                            })





class DownloadPage(MyPage):
    def __init__(self, request,*args):
        super().__init__(request, *args)  # 调用父类的 __init__ 方法

    def download_page(self):
            
        return render(self.request, 'download_page.html')

    def download_savefile_page(self,*args):
        
        if list(self.args):   
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #             self.user,   '下載sav檔案失敗頁面', '失敗')                 
            
            args = list(self.args)
            args = args[0] 

            messages = args.get('messages') 
            return   render(self.request, 'download_savefile_page.html', {'username': self.user
                                                        ,'years':self.savefiles
                                                        ,'messages':messages})        
        else:
            
            return   render(self.request, 'download_savefile_page.html', {'username': self.user
                                                        ,'years':self.savefiles})    

    def download_powerflow_page(self,*args):
        
        # logger.info('USER: %s ACTION: %s MESSAGE: %s',
        # self.user,   '進入下載電力潮流檔案頁面', '進入頁面成功') 
        
        accfiles = get_data_from_psse_backend(url=f"{self.url}/find_acc_files_in_dir"
                                    , params={"sourcedir":self.powerflow_dir}
                                    )
        print(accfiles)
        if  list(self.args ): 
    
            # yearslist = os.listdir(PowerFlow_file_sav_Folder)
            args = list(self.args)
            args = args[0]

            messages = args.get('messages') 
        else:
            messages = []
              
        return   render(self.request, 'download_powerflow_page.html',{'years':accfiles
                                                        ,'messages':messages})  
    def download_errorcircuit_page(self,*args):
        relfiles = get_data_from_psse_backend(url=f"{self.url}/find_rel_files_in_dir"
                                    , params={"sourcedir":self.errorcircuit_dir}
                                    )
        print(list(self.args ))
        if  list(self.args ): 
    
            args = list(self.args)
            args = args[0]

            messages = args.get('messages') 
        else:
            messages = []
              
        return   render(self.request, 'download_errorcircuit_page.html',{'years':relfiles
                                                        ,'messages':messages})         
   
    def download_dynamic_page(self,*args):

        outfiles = get_data_from_psse_backend(url=f"{self.url}/find_out_files_in_dir"
                                    , params={"sourcedir":self.dynamic_dir}
                                    )
        
        print(list(self.args ))
        if  list(self.args ): 
    
            args = list(self.args)
            args = args[0]

            messages = args.get('messages') 
        else:
            messages = []
              
        return   render(self.request, 'download_dynamic_page.html',{'years':outfiles
                                                        ,'messages':messages})  



    def download_idvfile_page(self,*args):         
        
        logger.info('USER: %s ACTION: %s MESSAGE: %s',
                    self.user,   '進入idv檔案下載頁面', '進入idv檔案下載頁面成功')
        
        IdvFile_Folder = f"./User/{self.user}/IDV/"


        if os.path.isdir(IdvFile_Folder):             
            files = fileprocess.How_many_rawfile(IdvFile_Folder, fileextension = r'.idv')
            years = []
            for filesstr in files:
                years.append(filesstr.split('.')[0])
            print(years)    
            # years = files
        else:       
            years = []  
            print(years)                            
            
        if list(self.args):   
            logger.info('USER: %s ACTION: %s MESSAGE: %s',
                        self.user,   '下載idv檔案失敗頁面', '失敗')                 
            
            args = list(self.args)
            args = args[0] 

            messages = args.get('messages') 
            return   render(self.request, 'download_idvfile_page.html', {'username': self.user
                                                        ,'years':years
                                                        ,'messages':messages})        
        else:
            
            return   render(self.request, 'download_idvfile_page.html', {'username': self.user
                                                        ,'years':years})   

    def download_idvfile_for_create_page(self,*args):
        
        if list(self.args):   
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #             self.user,   '下載sav檔案失敗頁面', '失敗')                 
            
            args = list(self.args)
            args = args[0] 

            messages = args.get('messages') 
            return   render(self.request, 'download_idvfile_for_create_page.html', {'username': self.user

                                                        ,'messages':messages})        
        else:
            
            return   render(self.request, 'download_idvfile_for_create_page.html', {'username': self.user
                                                        })  


