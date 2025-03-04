import sys,os
import typing
import shutil
import subprocess
import re
import io

from .. import fileprocess

def How_many_SavFile_in_UserFolder(sourcedir:str) -> typing.Iterator: 

    # files = fileprocess.How_many_rawfile(sav_folder, fileextension = r'.sav')

    return (_.split('.')[0] for _ in fileprocess.How_many_rawfile(sourcedir
                                                                , fileextension = r'.sav')                       
            )

def How_many_filter_file_in_UserFolder(sourcedir:str) -> typing.Iterator: 

    files = fileprocess.How_many_rawfile(sourcedir, fileextension = r'.npz')
    print('sourcedir-->',sourcedir)
    print('files-->',files)
    return (_.split('.')[0] for _ in fileprocess.How_many_rawfile(sourcedir
                                                                , fileextension =  r'.npz')                       
            )      


def How_many_acc_in_dir(sourcedir:str):
    accfile = [] 
    
    for savfilename in os.listdir(sourcedir):
        accfile.append(fileprocess.How_many_rawfile(f"{sourcedir}/{savfilename}" , fileextension = r'.txt'))
    # files = fileprocess.How_many_rawfile(sav_folder, fileextension = r'.sav')
    print('accfile -->', accfile)
    if accfile == []:
        return []
    else:    
        return (_[0].split('.')[0] for _ in accfile                       
                ) 

def How_many_rel_in_dir(sourcedir:str):
    relfile = [] 
    for savfilename in os.listdir(sourcedir):
        
        relfile.append(fileprocess.How_many_rawfile(f"{sourcedir}/{savfilename}" , fileextension = r'.txt'))


    if relfile == []:
        return []
    else:    
        return (_[0].split('.')[0] for _ in relfile                       
                )               

def How_many_out_in_dir(sourcedir:str):
    outfile = [] 
    for savfilename in os.listdir(sourcedir):
        
        outfile.append(fileprocess.How_many_rawfile(f"{sourcedir}/{savfilename}" , fileextension = r'.out'))
    # files = fileprocess.How_many_rawfile(sav_folder, fileextension = r'.sav')
    
    return (_.split('.')[0] for _ in outfile[0]                       
            )          
if __name__ == '__main__':
    user = '621882'
    years = How_many_SavFile_in_UserFolder(user)
    print(list(years))