import os
import threading
import subprocess

import logging
import numpy as np
from collections import OrderedDict

from ..Log.LogConfig import Setlog
from .. import fileprocess
# from ...class_for_views.delete import Delete
from .run_pyfile_by_execmd import Run_pyfile_by_execmd
from . import how_many_sav_file
def writeFile(filename, data):

    with open(filename, "w")  as f:
        f.write(data)

def Filter_savefile_by_labeltype(savfiledir,savfile_name,user,label_type, targetdir):
    

    logger_Filter_savefile_by_labeltype = Setlog(logfolder= 'Log/'+user+'/Filter_savefile_by_labeltype/', level=logging.INFO,logger_name=f'Filter_savefile_by_labeltype_{user}')


    cmd = Run_pyfile_by_execmd(python_location= "python"
                                ,pyfile= "pssefunctionsrc/src/filter.py"
                                ,args= f"--Label_type {label_type} "\
                                       f"--Sav_File {savfile_name} "
                                       f"--User_name {user} " 
                                       f"--savfiledir {savfiledir} "\
                                       f"--target_dir {targetdir}")
    

    print(cmd)
    
    result = fileprocess.execCmd(cmd)  
    # print(result) 
    logger_Filter_savefile_by_labeltype.info('%s %s的num和name取得成功\n',savfile_name,label_type) 
    return  1    


def filter_labeltype_num(filterfiles, filterdir,user,label_type):
    user_data_filter_folder = f"{filterdir}/{label_type}"
    # for savfile_name in years:           
    #     Filter_savefile_by_labeltype(savfile= f"{savfile_Folder}/{savfile_name}.sav"
    #                             ,savfile_name=savfile_name
    #                             ,user=user
    #                             ,label_type=label_type)
    if filterfiles:
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{user_data_filter_folder}/{filterfile_name}.npz")

        
        Num, Name = user_data_of_labeltype["num"], user_data_of_labeltype['name']
        mapping = dict(zip(Num, Name))
        # Name = OrderedDict.fromkeys(Name)
        # Num = OrderedDict.fromkeys(Num)

        for filterfile_name in filterfiles[1:len(filterfiles)]:
            # print("savfile_name",savfile_name)
            user_data_of_labeltype = np.load(f"{user_data_filter_folder}/{filterfile_name}.npz")
            
            mapping.update(dict(zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'])))     
            
            # Name.update(OrderedDict.fromkeys(user_data_of_labeltype['name']))

            

            
            # Num.update(OrderedDict.fromkeys(user_data_of_labeltype['num']))

        Num = np.array(list(mapping.keys()))
        
        Name = np.array(list(mapping.values()))
        np.savez(f'{user_data_filter_folder}/latest.npz', name=Name, num=Num)        
        data_of_labeltype = [
            {'num': num, 'name': name}
            for num, name in zip(Num, Name)
        ]        
        
        return data_of_labeltype   
    else:
        return []
def run_script_with_args(cmd):
    
    subprocess.run(cmd,capture_output=False)


class Display_X_Label():
    
    def __init__(self,labeltype, savfiledir, filterdir, targetdir, user):
        self.labeltype = labeltype
        # self.savefile = savefile
        self.savfiledir = savfiledir
        self.user = user
        self.filterdir = filterdir

        self.targetdir = targetdir

    def filter_labeltype_num_name(self, savefile):

        return Filter_savefile_by_labeltype(savfiledir= self.savfiledir
                                ,savfile_name = savefile
                                ,user = self.user
                                ,label_type = self.labeltype
                                ,targetdir = self.targetdir)

    def filter_all(self, savfile_name):
        
        cmd_load = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type load "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")
        writeFile(f'{self.targetdir}/cmd_load.txt', cmd_load)

        cmd_area = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type area "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")
        writeFile(f'{self.targetdir}/cmd_area.txt', cmd_area)

        cmd_bus = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/filter.py"
                                    ,args= f"--Label_type bus "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")
        writeFile(f'{self.targetdir}/cmd_bus.txt', cmd_bus)


        cmd_zone = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type zone "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")
        
        writeFile(f'{self.targetdir}/cmd_zone.txt', cmd_zone)

        cmd_owner = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type owner "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")

        writeFile(f'{self.targetdir}/cmd_owner.txt', cmd_owner)

        cmd_machine = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/filter.py"
                                    ,args= f"--Label_type machine "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")

        writeFile(f'{self.targetdir}/cmd_machine.txt', cmd_machine)                                        

        cmd_tripline = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type tripline "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")   

        writeFile(f'{self.targetdir}/cmd_tripline.txt', cmd_tripline)

        cmd_branch = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type branch "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}") 

        writeFile(f'{self.targetdir}/cmd_branch.txt', cmd_branch)

        cmd_twowinding = Run_pyfile_by_execmd(python_location= "python"
                                    ,pyfile= "pssefunctionsrc/src/run_filter.py"
                                    ,args= f"--Label_type twowinding "\
                                        f"--Sav_File {savfile_name} "
                                        f"--User_name {self.user} " 
                                        f"--savfiledir {self.savfiledir} "\
                                        f"--target_dir {self.targetdir}")  

        writeFile(f'{self.targetdir}/cmd_twowinding.txt', cmd_twowinding)
        

        threads = [
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_load,)),
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_area,)),
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_bus,)),
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_zone,)),                
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_owner,)),
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_machine,)),
            threading.Thread(target=run_script_with_args, daemon=True, 
                args = (cmd_tripline,)),
            threading.Thread(target=run_script_with_args, daemon=True, 
                            args = (cmd_branch,)),   
            threading.Thread(target=run_script_with_args, daemon=True, 
                            args = (cmd_twowinding,)),                 
                                         
                                                                                        
        ]
        print('threads --> ',threads)
        batch_size = 3
        total_batches = (len(threads) + batch_size - 1) // batch_size  # 向上取整

        for i in range(0, len(threads), batch_size):
            print(f"\n開始執行第 {i//batch_size + 1}/{total_batches} 批次...")
            
            batch = threads[i:i + batch_size]
            
            # 啟動這一批的線程
            for thread in batch:
                print(f"啟動線程: {thread.name}")
                thread.start()
            
            # 等待這一批的線程完成
            for thread in batch:
                try:
                    thread.join(timeout=30)
                    if thread.is_alive():
                        print(f"警告: {thread.name} 執行超時")
                    else:
                        print(f"{thread.name} 已完成")
                except Exception as e:
                    print(f"線程 {thread.name} 發生錯誤: {e}")
                threads.remove(thread)
            print(f"第 {i//batch_size + 1} 批次完成")
        # for thread in threads:
        #     thread.start()

        # for thread in threads:
        #     thread.join(timeout=30)
        print(threads)   
        del threads
        

        return 1       

    def display_which_label(self, filterfiles) :

        print(filterfiles)
        if os.path.isfile(f"{self.filterdir}/{self.labeltype}/latest.npz"):

            filter_data = np.load(f"{self.filterdir}/{self.labeltype}/latest.npz")
            Num, Name = filter_data["num"], filter_data['name']

            return [
                        {'num': num, 'name': name}
                        for num, name in zip(filter_data["num"]
                                                    , filter_data['name'])
                    ] 
        else:            
            return filter_labeltype_num(filterfiles = filterfiles
                                    , filterdir = self.filterdir
                                    , user = self.user
                                    , label_type = self.labeltype)


