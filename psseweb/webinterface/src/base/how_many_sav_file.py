import sys,os
import typing
import shutil
import subprocess
import re
import io

from webinterface.src import fileprocess

def How_many_SavFile_in_UserFolder(sav_folder:str) -> typing.Iterator: 

    # files = fileprocess.How_many_rawfile(sav_folder, fileextension = r'.sav')

    return (_.split('.')[0] for _ in fileprocess.How_many_rawfile(sav_folder
                                                                , fileextension = r'.sav')                       
            )
def How_many_filter_file_in_UserFolder(filterdir:str) -> typing.Iterator: 

    # files = fileprocess.How_many_rawfile(filterdir, fileextension = r'.npz')

    return (_.split('.')[0] for _ in fileprocess.How_many_rawfile(filterdir
                                                                , fileextension =  r'.npz')                       
            )
if __name__ == '__main__':
    user = '621882'
    years = How_many_SavFile_in_UserFolder(user)
    print(list(years))