import os
import re
import shutil
import subprocess
import numpy as np

import chardet
import pandas as pd

from .run_pyfile_by_execmd import Run_pyfile_by_execmd
def writeFile(filename, data):

    with open(filename, "wb")  as f:
        f.write(data)



def convert_to_raw(sav_file_name, savfile_dir, target_dir):
    cmd = Run_pyfile_by_execmd(python_location= "python"
                        ,pyfile= "webinterface/src/pssefunction/to_raw.py"
                        ,args=f"--Sav_File {sav_file_name} "\
                            f"--savfiledir {savfile_dir} "\
                            f"--target_dir {savfile_dir}")    
    print('cmd-->',cmd)

    r = subprocess.run(cmd,capture_output=True, shell=True)  
    if r.returncode != 0:
        error_message = r.stderr.decode('big5').strip()
        print(f"Error occurred: {error_message}")
        return {
                    "error":1
                    ,"return_value":{
                        "function":"subprocess.Popen in upload.py"
                        ,"front_message":f"轉成raw檔失敗，{error_message}"
                        ,"backend_message":f'error_message -->{error_message}\n'\
                                            f'r.returncode --> {r.returncode}'
                    }

                }
    return 0




