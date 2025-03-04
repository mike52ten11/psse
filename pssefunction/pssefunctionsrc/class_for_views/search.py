import os
import json

from django.http import JsonResponse

from ..src import fileprocess
from ..src.base.how_many_sav_file import (How_many_SavFile_in_UserFolder
                                        ,How_many_filter_file_in_UserFolder
                                        ,How_many_acc_in_dir
                                        ,How_many_rel_in_dir
                                        ,How_many_out_in_dir
                                        )

class SearchFiles:
    def __init__(self, request):
        self.sourcedir  = request.GET.get('sourcedir')
        print('search_labelfiles sourcedir-->',self.sourcedir)
    def search_savfiles(self):        
        
        print('filter_savfile -->', self.sourcedir)

        return   list(How_many_SavFile_in_UserFolder(sourcedir=f'{self.sourcedir}'))  

    def search_accfiles(self):        
        
        print('accfiles_dir -->', self.sourcedir)

        return   list(How_many_acc_in_dir(sourcedir=f'{self.sourcedir}'))

    def search_relfiles(self): 

        print('relfiles_dir -->', self.sourcedir)

        return   list(How_many_rel_in_dir(sourcedir=f'{self.sourcedir}'))

    def search_outfiles(self): 
           
        print('outfiles_dir -->', self.sourcedir)

        return   list(How_many_out_in_dir(sourcedir=f'{self.sourcedir}'))         

    def search_labelfiles(self):  
        print('search_labelfiles sourcedir-->',self.sourcedir)
        return   list(How_many_filter_file_in_UserFolder(sourcedir=f'{self.sourcedir}'))