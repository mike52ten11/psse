import os
import json

from django.http import JsonResponse

from .. import fileprocess
from .how_many_sav_file import (How_many_SavFile_in_UserFolder
                                        ,How_many_npz_in_UserFolder
                                        ,How_many_acc_in_dir
                                        ,How_many_rel_in_dir
                                        ,How_many_out_in_dir
                                        )

class SearchFiles:
    def __init__(self, args):
        self.sourcedir  = args['sourcedir']
        print('search_labelfiles sourcedir-->',self.sourcedir)
    def search_savfiles(self):        
        
        print('filter_savfile -->', self.sourcedir)

        return   list(How_many_SavFile_in_UserFolder(sourcedir=f'{self.sourcedir}'))  

    def search_accfiles(self):        
        
        print('accfiles_dir -->', self.sourcedir)

        return   list(How_many_acc_in_dir(sourcedir=f'{self.sourcedir}'))

    def search_powerflow_file(self):
    
        try:
            # 列出 powerflow 資料夾下的所有子資料夾
            years = [d for d in os.listdir(self.sourcedir) 
                    if os.path.isdir(os.path.join(self.sourcedir, d))]
            return years
        except FileNotFoundError:
            print(f"資料夾 {self.sourcedir} 不存在")
            return []
        except Exception as e:
            print(f"發生錯誤: {e}")
            return []

    def search_relfiles(self): 

        print('relfiles_dir -->', self.sourcedir)

        return   list(How_many_rel_in_dir(sourcedir=f'{self.sourcedir}'))

    def search_outfiles(self): 
           
        print('outfiles_dir -->', self.sourcedir)

        return   list(How_many_out_in_dir(sourcedir=f'{self.sourcedir}'))         

    def search_labelfiles(self):  
        print('search_labelfiles sourcedir-->',self.sourcedir)
        return   list(How_many_npz_in_UserFolder(sourcedir=f'{self.sourcedir}'))

    def search_npzfiles(self):        
        
        print('filter_savfile -->', self.sourcedir)

        return   list(How_many_npz_in_UserFolder(sourcedir=f'{self.sourcedir}'))         