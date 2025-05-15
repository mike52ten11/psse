import os
import requests
from pathlib import Path
from icecream import ic
ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='debug > ')

from django.shortcuts import render, redirect
from django.core.cache import cache


from webinterface.src.cache_data_type import get_cache_key
from webinterface.src.base.get_showdata_of_componets import GetShowDataOfComponents

from .src.base.search import SearchFiles
from .readconfig import read_config
from .get_filter_data import (  GetData,
                                create_latest_npzfile)

    


class MyPage:

    def __init__(self, request,*args):
        self.request = request
        self.args = args
        self.user = str(self.request.user)
        self.user_dir = f"../Data/User/{self.user}"
        self.savfile_dir = f"{self.user_dir}/SavFile"
        self.savfile_dir_for_faultcurrent = f"{self.user_dir}/SavFile/FaultCurrent"
        self.idvfile_dir = f'{self.user_dir}/IDV'
        self.dynamic_dir = f'{self.user_dir}/Dynamic'
        self.powerflow_dir = f'{self.user_dir}/PowerFlow'
        self.powerflowsub_dir = f'{self.user_dir}/PowerFlowSub'
        self.errorcircuit_dir = f'{self.user_dir}/FaultCurrent'
        self.filter_dir = f'{self.user_dir}/filter'
        self.excute_idvfile_dir = f'{self.user_dir}/excute_idvfile'
        self.server_settings = read_config()
   
  



            
    def home_page(self):
        os.makedirs(f'{self.user_dir}/SavFile', exist_ok=True)
        os.makedirs(f'{self.user_dir}/SavFile/Powerflow', exist_ok=True)
        os.makedirs(f'{self.user_dir}/SavFile/FaultCurrent', exist_ok=True)
        os.makedirs(f'{self.user_dir}/SavFile/filter', exist_ok=True)
        os.makedirs(f'{self.user_dir}/IDV', exist_ok=True)
        os.makedirs(f'{self.user_dir}/Dynamic', exist_ok=True)
        os.makedirs(f'{self.user_dir}/PowerFlow', exist_ok=True)
        os.makedirs(f'{self.user_dir}/PowerFlowSub', exist_ok=True)
        os.makedirs(f'{self.user_dir}/FaultCurrent', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        return render(self.request, 'main.html')
            
    def upload_page(self):
        
        '''
            Step 1 : 找出使用者有上傳哪些 sav 檔案
            Step 2 : 顯示使用者的 sav 檔案

        '''
        self.savefiles = SearchFiles({"sourcedir":self.savfile_dir}).search_savfiles()                                
    
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
        self.savefiles_of_powerflow = SearchFiles({"sourcedir":f"{self.user_dir}/SavFile/Powerflow"}).search_savfiles()
        
                    
        print('self.args = ',self.savefiles_of_powerflow)
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
        

        self.savefiles_of_powerflow = SearchFiles({"sourcedir":f"{self.user_dir}/SavFile/Powerflow"}).search_savfiles()
   
        if self.savefiles_of_powerflow== []:

            zones = {'num': [], 'name': []}
            areas = {'num': [], 'name': []}
        else:
            sourcedir = f"{self.filter_dir}/Powerflow/zone"
            filterfiles = SearchFiles({"sourcedir":sourcedir}).search_labelfiles()

            print('filterfiles',filterfiles)
            if "latest" in filterfiles:
                npzfile = f"{self.filter_dir}/Powerflow/zone/latest.npz"
                zones = GetData(npzfile).zone_data() 
                
            elif filterfiles == []:
                zones = {'num': [], 'name': []}

            else:   
                zones = create_latest_npzfile(filterfiles=filterfiles, filterdir=sourcedir) 

            sourcedir = f"{self.filter_dir}/Powerflow/area"
            filterfiles = SearchFiles({"sourcedir":sourcedir}).search_labelfiles()

            print('filterfiles',filterfiles)
            if "latest" in filterfiles:
                npzfile = f"{self.filter_dir}/Powerflow/area/latest.npz"
                areas = GetData(npzfile).area_data() 
                
            elif filterfiles == []:
                areas = {'num': [], 'name': []}

            else:   
                areas = create_latest_npzfile(filterfiles=filterfiles, filterdir=sourcedir)                 
                 
                     

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
                                                    ,'areas':areas
                                                    ,'zones':zones
                                                    })
        else:

            return   render(self.request, 'powerflow.html', {'username':self.user
                                                            ,'years':self.savefiles_of_powerflow
                                                            ,'zones':zones
                                                            ,'areas':areas
                                                            })

    def upload_page_of_upload_errorcircuit(self):
        '''
            Step 1 : 找出使用者有上傳哪些 sav 檔案
            Step 2 : 顯示使用者的 sav 檔案

        '''
        self.savefiles_of_errorcircuit = SearchFiles({"sourcedir":f"{self.savfile_dir_for_faultcurrent}"}).search_savfiles()            
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
        self.savefiles_of_errorcircuit = SearchFiles({"sourcedir":f"{self.savfile_dir_for_faultcurrent}"}).search_savfiles()

        if self.savefiles_of_errorcircuit == []:
            
            areas = {'num': [], 'name': []} 
            zones = {'num': [], 'name': []} 
            owners = {'num': [], 'name': []}

        else:
#=============================     area       ===================================================                
            sourcedir = f"{self.filter_dir}/FaultCurrent/area"
            filterfiles = SearchFiles({"sourcedir":sourcedir}).search_labelfiles()

            print('filterfiles',filterfiles)
            if "latest" in filterfiles:
                npzfile = f"{self.filter_dir}/FaultCurrent/area/latest.npz"
                areas = GetData(npzfile).area_data()
            elif filterfiles == []:
                areas = {'num': [], 'name': []}

            else:   
                areas = create_latest_npzfile(filterfiles=filterfiles, filterdir=sourcedir) 
#===============================================================================================================
#===============================================================================================================

#=============================     zone       ===================================================                
            sourcedir = f"{self.filter_dir}/FaultCurrent/zone"
            filterfiles = SearchFiles({"sourcedir":sourcedir}).search_labelfiles()

            print('filterfiles',filterfiles)
            if "latest" in filterfiles:
                npzfile = f"{self.filter_dir}/FaultCurrent/zone/latest.npz"
                zones = GetData(npzfile).zone_data() 
                
            elif filterfiles == []:
                zones = {'num': [], 'name': []}

            else:   
                zones = create_latest_npzfile(filterfiles=filterfiles, filterdir=sourcedir)

#===============================================================================================================
#===============================================================================================================

#=============================     owner       ===================================================
            sourcedir = f"{self.filter_dir}/FaultCurrent/owner"
            filterfiles = SearchFiles({"sourcedir":sourcedir}).search_labelfiles()

            print('filterfiles',filterfiles)
            if "latest" in filterfiles:
                npzfile = f"{self.filter_dir}/FaultCurrent/owner/latest.npz"
                owners = GetData(npzfile).owner_data() 
                
            elif filterfiles == []:
                owners = {'num': [], 'name': []}

            else:   
                owners = create_latest_npzfile(filterfiles=filterfiles, filterdir=sourcedir)

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




            return   render(self.request, 'errorcircuit.html', {'username':self.user
                                                    ,'messages':['Server Error 請通知系統管理員']
                                                    ,'years':self.savefiles_of_errorcircuit})          


    def dynamic_page(self):


        self.savefiles_of_powerflow = SearchFiles({"sourcedir":f"{self.user_dir}/SavFile/Powerflow"}).search_savfiles()
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



        prepare_writing_data_area = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/area.idv'
                                                            ).area()
                                             
        prepare_writing_data_zone = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/zone.idv'
                                                            ).zone()

        prepare_writing_data_owner = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/owner.idv'
                                                            ).owner()

        prepare_writing_data_bus = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/bus.idv'
                                                            ).bus()

        prepare_writing_data_machine = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/machine.idv'
                                                            ).machine()


        prepare_writing_data_load = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/load.idv'
                                                            ).load()

        prepare_writing_data_branch = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/branch.idv'
                                                            ).branch()                                                            
        prepare_writing_data_twowinding = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/twowinding.idv'
                                                            ).twowinding()

        prepare_writing_data_threewinding = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/threewinding.idv'
                                                            ).threewinding()
        # prepare_writing_data_machine = cache.get(get_cache_key(self.user, 'machine'), [])

        # prepare_writing_data_branch = cache.get(get_cache_key(self.user, 'branch'), [])
        # prepare_writing_data_twowinding = cache.get(get_cache_key(self.user, 'twowinding'), [])
        # prepare_writing_data_threewinding = cache.get(get_cache_key(self.user, 'threewinding'), [])
        prepare_writing_data_threewinding_winding = GetShowDataOfComponents(
                                                                show_data_path = f'temp/{self.user}/writedata/show/threewinding_winding.idv'
                                                            ).threewinding_winding()        

        savefiles = SearchFiles({"sourcedir":self.savfile_dir}).search_savfiles() 

        print(prepare_writing_data_twowinding)

        if list(self.args):   
            args = list(self.args)
            args = args[0]            
            
            # args = self.args[0]
            print(args)
            messages = args.get('messages') 


            
            return   render(self.request, 'Create/prepare_writing.html', {'username': self.user
                                                            ,'years':savefiles
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
                                                            ,'years':savefiles
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
        savefiles = SearchFiles({"sourcedir":self.savfile_dir}).search_savfiles()
        if list(self.args):   
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #             self.user,   '下載sav檔案失敗頁面', '失敗')                 
            
            args = list(self.args)
            args = args[0] 

            messages = args.get('messages') 
            return   render(self.request, 'download_savefile_page.html', {'username': self.user
                                                        ,'years':savefiles
                                                        ,'messages':messages})        
        else:
            
            return   render(self.request, 'download_savefile_page.html', {'username': self.user
                                                        ,'years':savefiles})    
    def download_savefile_of_powerflow_page(self,*args):
        savefiles_of_powerflow = SearchFiles({"sourcedir":f'{self.savfile_dir}/Powerflow'}).search_savfiles()
        if list(self.args):   
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #             self.user,   '下載sav檔案失敗頁面', '失敗')                 
            
            args = list(self.args)
            args = args[0] 

            messages = args.get('messages') 
            return   render(self.request, 'download_savefile_of_powerflow_page.html', {'username': self.user
                                                        ,'years':savefiles_of_powerflow
                                                        ,'messages':messages})        
        else:
            
            return   render(self.request, 'download_savefile_of_powerflow_page.html', {'username': self.user
                                                        ,'years':savefiles_of_powerflow})  

    def download_savefile_of_errorcircuit_page(self,*args):
        savefiles_of_errorcircuit = SearchFiles({"sourcedir":f'{self.savfile_dir}/ErrorCircuit'}).search_savfiles()
        if list(self.args):   
            # logger.info('USER: %s ACTION: %s MESSAGE: %s',
            #             self.user,   '下載sav檔案失敗頁面', '失敗')                 
            
            args = list(self.args)
            args = args[0] 

            messages = args.get('messages') 
            return   render(self.request, 'download_savefile_of_errorcircuit_page.html', {'username': self.user
                                                        ,'years':savefiles_of_errorcircuit
                                                        ,'messages':messages})        
        else:
            
            return   render(self.request, 'download_savefile_of_errorcircuit_page.html', {'username': self.user
                                                        ,'years':savefiles_of_errorcircuit})                                                          
    def download_powerflow_page(self,*args):
        

        # accfiles = SearchFiles({"sourcedir":self.powerflow_dir}).search_accfiles()  
        accfiles = SearchFiles({"sourcedir":self.powerflow_dir}).search_powerflow_file()
        print(accfiles)
        if  list(self.args ): 
    
            
            args = list(self.args)
            args = args[0]

            messages = args.get('messages') 
        else:
            messages = []
              
        return   render(self.request, 'download_powerflow_page.html',{'years':accfiles
                                                        ,'messages':messages}) 

    def download_errorcircuit_page(self,*args):
        relfiles = SearchFiles({"sourcedir":self.errorcircuit_dir}).search_relfiles() 

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
        
        outfiles = os.listdir(self.dynamic_dir)

        # outfiles = SearchFiles({"sourcedir":self.dynamic_dir}).search_outfiles()
        ic(outfiles)
        
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


