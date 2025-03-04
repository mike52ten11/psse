import os
import re
import shutil
import subprocess
import numpy as np

import chardet
from .label_filter.area import area 
from .label_filter.bus import bus
from .label_filter.branch import branch

from .label_filter.fixedshunt import fixedshunt
from .label_filter.generator import generator
from .label_filter.load import load
from .label_filter.owner import owner
from .label_filter.transformer import transformer
# from .label_filter.three_winding_transformer import three_winding_transformer
# from .label_filter.two_winding_transformer import two_winding_transformer
from .label_filter.zone import zone


import pandas as pd
def writeFile(filename, data):

    with open(filename, "wb")  as f:
        f.write(data)



def run_filter(filename,rawfilepath, filter_dir):
    print(filename,rawfilepath, filter_dir)
    print("==============================")
    with open(rawfilepath, 'rb') as f:
        raw_data = f.read()


    result = area(raw_data, rawfilepath, f'{filter_dir}/area/area_{filename}.npz',f'{filter_dir}/area')    
    if not result["success"]:
        return result  # 或者根據需求處理錯誤
    
    result = zone(raw_data, rawfilepath, f'{filter_dir}/zone/zone_{filename}.npz',f'{filter_dir}/zone')
    zone_data_dict = result["data"]
    if not result["success"]:
        return result  # 或者根據需求處理錯誤

    result = bus(raw_data, rawfilepath, f'{filter_dir}/bus/bus_{filename}.npz',f'{filter_dir}/bus',zone_data_dict)
    bus_data_dict = result["data"]
    if not result["success"]:
        return result  # 或者根據需求處理錯誤
     

    result = branch(raw_data, rawfilepath, f'{filter_dir}/branch/branch_{filename}.npz',f'{filter_dir}/branch',bus_data_dict)
    if not result["success"]:
        return result  # 或者根據需求處理錯誤
    else:
        os.makedirs(f'{filter_dir}/tripline', exist_ok=True)        
        shutil.copyfile(f'{filter_dir}/branch/branch_{filename}.npz',f'{filter_dir}/tripline/tripline_{filename}.npz')   
    
    result = fixedshunt(raw_data, rawfilepath, f'{filter_dir}/fixedshunt/fixedshunt_{filename}.npz',f'{filter_dir}/fixedshunt',bus_data_dict)
    if not result["success"]:
        return result  # 或者根據需求處理錯誤
    

    result = generator(raw_data, rawfilepath, f'{filter_dir}/machine/machine_{filename}.npz',f'{filter_dir}/machine',bus_data_dict)
    if not result["success"]:
        return result  # 或者根據需求處理錯誤
    
    result = load(raw_data, rawfilepath, f'{filter_dir}/load/load_{filename}.npz',f'{filter_dir}/load',bus_data_dict)
    if not result["success"]:
        return result  # 或者根據需求處理錯誤  

    result = owner(raw_data, rawfilepath, f'{filter_dir}/owner/owner_{filename}.npz',f'{filter_dir}/owner')
    if not result["success"]:
        return result  # 或者根據需求處理錯誤     

    result = transformer(raw_data, rawfilepath
                        , f'{filter_dir}/three_winding_transformer/three_winding_transformer_{filename}.npz'
                        ,f'{filter_dir}/three_winding_transformer'
                        , f'{filter_dir}/two_winding_transformer/two_winding_transformer_{filename}.npz'
                        ,f'{filter_dir}/two_winding_transformer'
                        ,bus_data_dict)        
    if not result["success"]:
        return result  # 或者根據需求處理錯誤        
    # three_winding_transformer(raw_data, rawfilepath, f'{filter_dir}/three_winding_transformer/three_winding_transformer_{filename}.npz')
    # two_winding_transformer(raw_data, rawfilepath, f'{filter_dir}/two_winding_transformer/two_winding_transformer_{filename}.npz')

        
    return 0




