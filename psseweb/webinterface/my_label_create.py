
import os
import requests
import json
import numpy as np
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib import messages
from datetime import datetime

from webinterface.src.cache_data_type import get_cache_key
from webinterface.src.write_data.pssepyfunctions_to_idv import psspy_to_idv
from .readconfig import read_config
def create_api(url:str, params:dict):

    response = requests.post(url
                            , data={'params': json.dumps(params)}
                            # ,proxies = settings['proxy']
                            )   
    if response.status_code == 200:
        return response.json()["results"]

    else:    
        return []




class MyLabelCreate:
    def __init__(self, request):        
        self.request = request 
        self.user = str(self.request.user)
        self.savfiles = self.request.GET.getlist('year')
        self.user_dir = f"../Data/User/{self.user}"
        self.savfile_dir = f"{self.user_dir}/SavFile"
        self.idvfile_dir = f'{self.user_dir}/IDV'
        self.filter_dir = f'{self.user_dir}/filter'

        self.proxies = {
                        'http': None,
                        'https': None,
                    }  
        # self.api_ip = '10.52.20.21'    
        # self.api_port = '800' 
        self.server_settings = read_config()
        self.url = f"http://{self.server_settings['server_host']}:{self.server_settings['server_port']}"

    def write_areadata_to_savfiles(self):

        area_number = self.request.GET.get('AREANumber')
        area_name = self.request.GET.get('AREAName')

        

        if area_number and area_name:

            now_area_data = np.load(f'{self.filter_dir}/area/latest.npz')
            psspycommand =  {   'function':'area_data',
                                'data':[f"{area_number}" 
                                        ," "
                                        ," "
                                        ," "
                                        ,f"'{area_name}'"],
                                'labeltype':'area'
                            }
            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").area()
            
            # num = now_area_data["num"]
            # name = now_area_data["name"]

            # new_num = np.append(num,area_number)
            # new_name = np.append(name, area_name)

            # np.savez(f'{self.filter_dir}/area/latest.npz', num=new_num, name=new_name)
            # print('new_num-->', new_num)
            # print('new_name-->',new_name)
            cache_key = get_cache_key(self.user, 'area')
            
            # 從緩存獲取現有數據
            temp_areas = cache.get(cache_key, [])
            
            # 添加新數據
            new_area = {
                'area_number': area_number,
                'area_name': area_name,
                'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            }
            temp_areas.append(new_area)
            
            # 更新緩存，設置24小時過期
            cache.set(cache_key, temp_areas, 60 * 60 * 24)
            
            messages.success(self.request, '成功新增 area ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='AREA')        

        # args = {"userName":self.user
        #         ,"labeltype":"area"
        #         }        
        # for i in list(self.request.GET.keys()): 
        #     args[i] = self.request.GET[i]

        # params = {  "savfiles":self.savfiles,
        #             "savfile_dir": self.savfile_dir,
        #             "target_dir": self.savfile_dir,
        #             "idvfile_dir":self.idvfile_dir,                        
        #             "args": args,   
        #             } 
        # print('params-->',params)              
        # settings = {"proxy":self.proxies} 
        # cache_key = get_cache_key(self.user, 'area')

        # results = create_api(url = f"http://{self.api_ip}:{self.api_port}/write_data_to_savfile/",
        #                             params = params, 
        #                             settings = settings)
        # return results
    def write_zonedata_to_savfiles(self):
        zone_number = self.request.GET.get('ZONENumber')
        zone_name = self.request.GET.get('ZONEName')
        psspycommand =  {   'function':'zone_data',
                            'data':[f"{zone_number}" 
                                    ,f"'{zone_name}'"],
                            'labeltype':'zone'
                        }
        

        if zone_number and zone_name:

            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").zone()
            print(results_of_convert)
            if results_of_convert:
                messages.error(self.request, results_of_convert['backend_message'])
            else:                
                cache_key = get_cache_key(self.user, 'zone')
                
                # 從緩存獲取現有數據
                temp_zones = cache.get(cache_key, [])
                
                # 添加新數據
                new_zone = {
                    'zone_number': zone_number,
                    'zone_name': zone_name,
                    'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                }
                temp_zones.append(new_zone)
                
                # 更新緩存，設置24小時過期
                cache.set(cache_key, temp_zones, 60 * 60 * 24)
                
                messages.success(self.request, '成功新增 zone ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(zone number, zone name)')

        return redirect('select_Label', selection_Label='ZONE')     

    def write_ownerdata_to_savfiles(self):
        owner_number = self.request.GET.get('OWNERNumber')
        owner_name = self.request.GET.get('OWNERName')
        psspycommand =  {   'function':'owner_data',
                            'data':[f"{owner_number}" 
                                    ,f"'{owner_name}'"],
                            'labeltype':'owner'
                        }
        

        if owner_number and owner_name:

            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").zone()
            print(results_of_convert)
            if results_of_convert:
                messages.error(self.request, results_of_convert['backend_message'])
            else:                
                cache_key = get_cache_key(self.user, 'owner')
                
                # 從緩存獲取現有數據
                temp_owners = cache.get(cache_key, [])
                
                # 添加新數據
                new_owner = {
                    'owner_number': owner_number,
                    'owner_name': owner_name,
                    'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                }
                temp_owners.append(new_owner)
                
                # 更新緩存，設置24小時過期
                cache.set(cache_key, temp_owners, 60 * 60 * 24)
                
                messages.success(self.request, '成功新增 owner ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(owner number, owner name)')

        return redirect('select_Label', selection_Label='OWNER')   

    def write_busdata_to_savfiles(self):
        bus_number = self.request.GET.get('BUSNumber')
        bus_name = self.request.GET.get('BUSName')
        Code = int(self.request.GET.get('Code'))
        Area_Num = int(self.request.GET.get('AreaNum'))
        Zone_Num = int(self.request.GET.get('ZoneNum'))
        Owner_Num = int(self.request.GET.get('OwnerNum'))
        
        Base_kV = float(self.request.GET.get('BasekV'))
        Voltage = float(self.request.GET.get('Voltage'))
        Angel = float(self.request.GET.get('Angel'))
        Normal_Vmax = float(self.request.GET.get('NormalVmax'))
        Normal_Vmin = float(self.request.GET.get('NormalVmin'))
        Emergency_Vmax = float(self.request.GET.get('EmergencyVmax'))
        Emergency_Vmin = float(self.request.GET.get('EmergencyVmin'))

        psspycommand =  {   'function':'bus_data_4',
                            'data':[f'{bus_number}', 
                                    '0',
                                    f'{Code}',f'{Area_Num}',f'{Zone_Num}',f'{Owner_Num}',
                                    f'{Base_kV}',f'{Voltage}',f'{Angel}',f'{Normal_Vmax}',f'{Normal_Vmin}',f'{Emergency_Vmax}',f'{Emergency_Vmin}',
                                    f"'{bus_name}'"],
                            'labeltype':'bus'
                        }
        

        if bus_number and bus_name:

            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").bus()
            print(results_of_convert)
            if results_of_convert:
                messages.error(self.request, results_of_convert['backend_message'])
            else:                
                cache_key = get_cache_key(self.user, 'bus')
                
                # 從緩存獲取現有數據
                temp_bus = cache.get(cache_key, [])
                
                # 添加新數據
                new_bus = {
                    'bus_number': bus_number,
                    'bus_name': bus_name,
                    'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                }
                temp_bus.append(new_bus)
                print('new_bus', new_bus)
                # 更新緩存，設置24小時過期
                cache.set(cache_key, temp_bus, 60 * 60 * 24)
                
                messages.success(self.request, '成功新增 bus ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(bus number, bus name)')

        return redirect('select_Label', selection_Label='BUS') 

    def write_machine_to_savfiles(self):

        BUS_Number = int(self.request.GET.get('BusNumber'))
        ID = self.request.GET.get('ID')
        # ID = '1'
        MachineControlMode = int(self.request.GET.get('MachineControlMode'))
        BASE = int(self.request.GET.get('BASE'))
        Pgen = float(self.request.GET.get('Pgen'))
        Qgen = float(self.request.GET.get('Qgen'))
        
        Qmax = float(self.request.GET.get('Qmax'))
        Qmin = float(self.request.GET.get('Qmin'))
        Pmax = float(self.request.GET.get('Pmax'))
        Pmin = float(self.request.GET.get('Pmin'))
        Mbase = float(self.request.GET.get('Mbase'))
        RSource = float(self.request.GET.get('RSource'))
        XSource = float(self.request.GET.get('XSource'))

        #seq machine
        R = float(self.request.GET.get('R'))        
        SubtransientX = float(self.request.GET.get('SubtransientX'))
        RNegative = float(self.request.GET.get('RNegative'))
        XNegative = float(self.request.GET.get('XNegative'))
        RZero = float(self.request.GET.get('RZero'))
        XZero = float(self.request.GET.get('XZero'))
        TransientX = float(self.request.GET.get('TransientX'))
        SynchronousX = float(self.request.GET.get('SynchronousX'))

        

        if BUS_Number:
            psspycommand =  {   'function':'machine_data_4',
                                'data':[str(BUS_Number)
                                        ,str(ID)
                                        ,'0','1','0','0','0',str(MachineControlMode),str(BASE)
                                        ,str(Pgen),str(Qgen),str(Qmax),str(Qmin),str(Pmax),str(Pmin),str(Mbase),str(RSource),str(XSource)
                                        ,"","","","","","","",""
                                        ,""],
                                'labeltype':'machine'
                            }

            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").machine()
            psspycommand =  {   'function':'seq_machine_data_4',
                                'data':[str(BUS_Number)
                                        ,str(ID)
                                        ,'0'
                                        ,str(R),str(SubtransientX),str(RNegative),str(XNegative),str(RZero),str(XZero),str(TransientX),str(SynchronousX)
                                        ,"0.0","0.0","0.0"],
                                'labeltype':'seq_machine'
                            }     
            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").machine()                                   
            print(results_of_convert)
            if results_of_convert:
                messages.error(self.request, results_of_convert['backend_message'])
            else:                
                cache_key = get_cache_key(self.user, 'machine')
                
                # 從緩存獲取現有數據
                temp_machine = cache.get(cache_key, [])
                
                # 添加新數據
                new_machine = {
                    'bus_number': BUS_Number,
                    'id': ID,
                    'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                }
                temp_machine.append(new_machine)
                print('new_machine', new_machine)
                # 更新緩存，設置24小時過期
                cache.set(cache_key, temp_machine, 60 * 60 * 24)
                
                messages.success(self.request, '成功新增 Machine ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(bus number)')

        return redirect('select_Label', selection_Label='Machine') 


    def write_loaddata_to_savfiles(self):

        bus_number = self.request.GET.get('BusNumber')
        Pload = self.request.GET.get('Pload')
        Qload = self.request.GET.get('Qload')
        psspycommand =  {   'function':'load_data_6',
                            'data':[str(bus_number), 
                                    ' ',
                                    ' ',' ',' ',' ',' ',' ',' ',
                                    str(Pload),str(Qload),' ',' ',' ',' ',' ',' ',],
                            'labeltype':'load'
                        }
        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").load()

        if bus_number:
            cache_key = get_cache_key(self.user, 'load')
            
            # 從緩存獲取現有數據
            temp_load = cache.get(cache_key, [])
            
            # 添加新數據
            new_load = {
                'bus_number': bus_number,
                'Pload':Pload,
                'Qload':Qload,
                'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            }
            temp_load.append(new_load)
            
            # 更新緩存，設置24小時過期
            cache.set(cache_key, temp_load, 60 * 60 * 24)
            
            messages.success(self.request, '成功新增 load ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='LOAD')   

    def write_branchdata_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('FromBusNumber'))
        ToBusNumber = int(self.request.GET.get('ToBusNumber'))
        ID = self.request.GET.get('ID')
        LineR = float(self.request.GET.get('LineR'))
        LineX = float(self.request.GET.get('LineX'))
        ChargingB = float(self.request.GET.get('ChargingB'))
        Length = float(self.request.GET.get('Length')) 
        REAT1 = float(self.request.GET.get('REAT1'))  
        NAME = self.request.GET.get('NAME')

        #seq branch
        R_Zero = float(self.request.GET.get('R_Zero')) 
        X_Zero = float(self.request.GET.get('X_Zero'))  
        B_Zero = float(self.request.GET.get('B_Zero'))

        psspycommand =  {   'function':'branch_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    ID,
                                    ' ',' ',' ',' ',' ',' ',
                                    str(LineR),str(LineX),str(ChargingB),' ',' ',' ',' ',str(LineX),' ',' ',' ',' ',
                                    str(REAT1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                    "'"+NAME+"'"],
                            'labeltype':'branch'
                        }
        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").branch()

        psspycommand =  {   'function':'seq_branch_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber), 
                                    ID,
                                    ' ',
                                    str(R_Zero),str(X_Zero),str(B_Zero),' ',' ',' '],
                            'labeltype':'seq_branch'
                        }
        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").branch()

        if FromBusNumber:
            cache_key = get_cache_key(self.user, 'branch')
            
            # 從緩存獲取現有數據
            temp_branch = cache.get(cache_key, [])
            
            # 添加新數據
            new_branch = {
                'FromBusNumber': FromBusNumber,
                'ToBusNumber':ToBusNumber,
                'ID':ID,
                'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            }
            temp_branch.append(new_branch)
            
            # 更新緩存，設置24小時過期
            cache.set(cache_key, temp_branch, 60 * 60 * 24)
            
            messages.success(self.request, '成功新增 branch ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='BRANCH')  

    def write_twowinding_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('FromBusNumber'))
        ToBusNumber = int(self.request.GET.get('ToBusNumber'))
        ID = self.request.GET.get('ID')

        ControlledBus = self.request.GET.get('ControlledBus')
        if ControlledBus=='':
            ControlledBus = FromBusNumber
        else:
            ControlledBus = int(ControlledBus)

        Winding_int = int(self.request.GET.get('Winding_int'))
        Impedance = int(self.request.GET.get('Impedance'))
        Admittance = int(self.request.GET.get('Admittance'))

        SpecifiedR = float(self.request.GET.get('SpecifiedR'))
        SpecifiedX = float(self.request.GET.get('SpecifiedX'))
        Winding = float(self.request.GET.get('Winding'))
        Wind1 = float(self.request.GET.get('Wind1'))

        Wind2Ratio = float(self.request.GET.get('Wind2Ratio'))
        Wind2 = float(self.request.GET.get('Wind2'))
        RATE1 = float(self.request.GET.get('RATE1'))
        Name = self.request.GET.get('Name')
        #seq 2winding
        Connection = int(self.request.GET.get('Connection'))
        R01 = float(self.request.GET.get('R01'))
        X01 = float(self.request.GET.get('X01'))

        psspycommand =  {   'function':'two_winding_data_6',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    ID,
                                    ' ',' ',' ',' ',' ',' ',' ',' ',str(ControlledBus),' ',' ',' ',' ',str(Winding_int),str(Impedance),str(Admittance),
                                    str(SpecifiedR),str(SpecifiedX),str(Winding),' ',str(Wind1),' ',str(Wind2Ratio),str(Wind2),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                    str(RATE1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                    "'"+Name+"'"],
                            'labeltype':'twowinding'
                        }
        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").twowinding()

        psspycommand =  {   'function':'seq_two_winding_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    ID,
                                    str(Connection),' ',' ',
                                    ' ',' ',str(R01),str(X01),' ',' ',' ',' ',' ',' ',],
                            'labeltype':'seq_twowinding'
                        }
        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").twowinding()

        if FromBusNumber:
            cache_key = get_cache_key(self.user, 'twowinding')
            
            # 從緩存獲取現有數據
            temp_twowinding = cache.get(cache_key, [])
            
            # 添加新數據
            new_twowinding = {
                'FromBusNumber': FromBusNumber,
                'ToBusNumber':ToBusNumber,
                'ID':ID,
                'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            }
            temp_twowinding.append(new_twowinding)
            
            # 更新緩存，設置24小時過期
            cache.set(cache_key, temp_twowinding, 60 * 60 * 24)
            
            messages.success(self.request, '成功新增 two winding ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='TRANSFORMER2Winding')  

    def write_threewinding_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('FromBusNumber'))
        
        ToBusNumber = int(self.request.GET.get('ToBusNumber'))

        LastBusNumber = int(self.request.GET.get('LastBusNumber'))
        
        ID = self.request.GET.get('ID')

        #three_wnd_imped_data_4
        connection =int( self.request.GET.get('connection'))
        
        Winding =int( self.request.GET.get('Winding'))
        Impedance = int(self.request.GET.get('Impedance'))
        Admittance = int(self.request.GET.get('Admittance'))
        ImpaedanceAdjustmentCode = int(self.request.GET.get('ImpaedanceAdjustmentCode'))
        
        W12R = float(self.request.GET.get('W12R'))  if self.request.GET.get('W12R')!="" else  0.0
        
        W12X = float(self.request.GET.get('W12X')) if self.request.GET.get('W12X')!=""  else  0.0    
            
        W23R = float(self.request.GET.get('W23R')) if self.request.GET.get('W23R')!=""else  0.0  
        
        W23X = float(self.request.GET.get('W23X'))if self.request.GET.get('W23X')!=""  else  0.0  
        
        W31R = float(self.request.GET.get('W31R')) if self.request.GET.get('W31R')!=""  else  0.0  
        
        W31X = float(self.request.GET.get('W31X')) if self.request.GET.get('W31X')!=""  else  0.0  
        

        Winding12MVABase = float(self.request.GET.get('Winding12MVABase')) if self.request.GET.get('Winding12MVABase')!=""  else  0.0   
        
        Winding23MVABase = float(self.request.GET.get('Winding23MVABase')) if self.request.GET.get('Winding23MVABase')!=""  else  0.0           
        
        Winding31MVABase = float(self.request.GET.get('Winding31MVABase')) if self.request.GET.get('Winding31MVABase')!=""  else  0.0           
        

        Name = self.request.GET.get('Name')

        psspycommand =  {   'function':'three_wnd_imped_data_4',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    str(LastBusNumber),
                                    ID,
                                    ' ',' ',' ',' ',str(Winding),str(Impedance),str(Admittance),' ',' ',' ',' ',' ',str(ImpaedanceAdjustmentCode),
                                    str(W12R),str(W12X),str(W23R),str(W23X),str(W31R),str(W31X),str(Winding12MVABase),str(Winding23MVABase),str(Winding31MVABase),' ',' ',' ',' ',' ',' ',' ',' ',
                                    "'"+Name+"'",
                                    "' '"],
                            'labeltype':'three_wnd_imped_data_4'
                        }

        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").threewinding()
        
        if self.request.GET.get('R01')!="":
            R01 = float(self.request.GET.get('R01'))
        if self.request.GET.get('X01')!="":            
            X01 = float(self.request.GET.get('X01'))
        if self.request.GET.get('R02')!="":            
            R02 = float(self.request.GET.get('R02'))
        if self.request.GET.get('X02')!="":            
            X02 = float(self.request.GET.get('X02'))   
        if self.request.GET.get('R03')!="":            
            R03 = float(self.request.GET.get('R03'))
        if self.request.GET.get('X03')!="":            
            X03 = float(self.request.GET.get('X03'))

        psspycommand =  {   'function':'seq_three_winding_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    str(LastBusNumber),
                                    ID,
                                    ' ',' ',str(connection)
                                    ,' ',' ',str(R01),str(X01),' ',' ',str(R02),str(X02),' ',' ',str(R03),str(X03),' ',' '                                    
                                    ],
                            'labeltype':'seq_three_winding_data_3'
                        }
        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").threewinding() 

        if FromBusNumber:
            cache_key = get_cache_key(self.user, 'threewinding')
            
            # 從緩存獲取現有數據
            temp_threewinding = cache.get(cache_key, [])
            
            # 添加新數據
            new_threewinding = {
                'FromBusNumber': FromBusNumber,
                'ToBusNumber':ToBusNumber,
                'ID':ID,
                'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            }
            temp_threewinding.append(new_threewinding)
            
            # 更新緩存，設置24小時過期
            cache.set(cache_key, temp_threewinding, 60 * 60 * 24)
            
            messages.success(self.request, '成功新增 three winding ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='TRANSFORMER3Winding')  

    def write_threewinding_winding_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('FromBusNumber'))
        
        ToBusNumber = int(self.request.GET.get('ToBusNumber'))

        LastBusNumber = int(self.request.GET.get('LastBusNumber'))        
        # ID = self.request.GET.get('ID')

        BusNumber = self.request.GET.get('BusNumber')
        BusNumber = int(BusNumber.split(':')[-1])
        print('BusNumber',BusNumber)

        if BusNumber==FromBusNumber:
            Winding = 1
        elif  BusNumber==ToBusNumber:
            Winding = 2
        else:
            Winding = 3       

        Controlled = int(self.request.GET.get('Controlled')) if self.request.GET.get('Controlled')!=""  else  0
        Tap_Positions = int(self.request.GET.get('Tap_Positions')) if self.request.GET.get('Tap_Positions')!=""  else 33
        Impendance = int(self.request.GET.get('Impendance')) if self.request.GET.get('Impendance')!=""  else  0

        RATE1 = float(self.request.GET.get('RATE1')) if self.request.GET.get('RATE1')!=""  else  0.0 
        RATE2 = float(self.request.GET.get('RATE2')) if self.request.GET.get('RATE2')!=""  else  0.0 
        RATE3 = float(self.request.GET.get('RATE3')) if self.request.GET.get('RATE3')!=""  else  0.0
        RATE4 = float(self.request.GET.get('RATE4')) if self.request.GET.get('RATE4')!=""  else  0.0
        RATE5 = float(self.request.GET.get('RATE5')) if self.request.GET.get('RATE5')!=""  else  0.0
        RATE6 = float(self.request.GET.get('RATE6')) if self.request.GET.get('RATE6')!=""  else  0.0
        RATE7 = float(self.request.GET.get('RATE7')) if self.request.GET.get('RATE7')!=""  else  0.0
        RATE8 = float(self.request.GET.get('RATE8')) if self.request.GET.get('RATE8')!=""  else  0.0
        RATE9 = float(self.request.GET.get('RATE9')) if self.request.GET.get('RATE9')!=""  else  0.0
        RATE10 = float(self.request.GET.get('RATE10')) if self.request.GET.get('RATE10')!=""  else  0.0
        RATE11 = float(self.request.GET.get('RATE11')) if self.request.GET.get('RATE11')!=""  else  0.0
        RATE12 = float(self.request.GET.get('RATE12')) if self.request.GET.get('RATE12')!=""  else  0.0

        Ratio =  float(self.request.GET.get('Ratio')) if self.request.GET.get('Ratio')!=""  else  1.0
        Nominal =  float(self.request.GET.get('Nominal')) if self.request.GET.get('Nominal')!=""  else  0.0
        Angle =  float(self.request.GET.get('Angle')) if self.request.GET.get('Angle')!=""  else  0.0
        Rmax = float(self.request.GET.get('Rmax')) if self.request.GET.get('Rmax')!=""  else  1.1
        Rmin = float(self.request.GET.get('Rmin')) if self.request.GET.get('Rmin')!=""  else  0.9
        Vmax = float(self.request.GET.get('Vmax')) if self.request.GET.get('Vmax')!=""  else  1.1
        Vmin = float(self.request.GET.get('Vmin')) if self.request.GET.get('Vmin')!=""  else  0.9
        Wnd_Connect = float(self.request.GET.get('Wnd_Connect')) if self.request.GET.get('Wnd_Connect')!=""  else  0.0
        Load_Drop_1 = float(self.request.GET.get('Load_Drop_1')) if self.request.GET.get('Load_Drop_1')!=""  else  0.0
        Load_Drop_2 = float(self.request.GET.get('Load_Drop_2')) if self.request.GET.get('Load_Drop_2')!=""  else  0.0
        

        psspycommand =  {   'function':'three_wnd_winding_data_5',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    str(LastBusNumber),
                                    ' ',
                                    str(Winding)
                                    ,str(Tap_Positions),str(Impendance),str(Controlled),' ',' ',' '
                                    ,str(Ratio),str(Nominal),str(Angle),str(Rmax),str(Rmin),str(Vmax),str(Vmin),str(Load_Drop_1),str(Load_Drop_2),str(Wnd_Connect)
                                    ,str(RATE1),str(RATE2),str(RATE3),str(RATE4),str(RATE5),str(RATE6),str(RATE7),str(RATE8),str(RATE9),str(RATE10),str(RATE11),str(RATE12)
                                    ],
                            'labeltype':'three_wnd_winding_data_5'
                        }    

        psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").threewinding_winding()
        

        if FromBusNumber:
            cache_key = get_cache_key(self.user, 'threewinding_winding')
            
            # 從緩存獲取現有數據
            temp_threewinding_winding = cache.get(cache_key, [])
            
            # 添加新數據
            new_threewinding_winding = {
                'FromBusNumber': FromBusNumber,
                'ToBusNumber':ToBusNumber,
                'LastBusNumber':LastBusNumber,
                'BusNumber':BusNumber,
                
                'timestamp': str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            }
            temp_threewinding_winding.append(new_threewinding_winding)
            
            # 更新緩存，設置24小時過期
            cache.set(cache_key, temp_threewinding_winding, 60 * 60 * 24)
            
            messages.success(self.request, '成功新增 three winding ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='TRANSFORMER3Winding')  

    def create_label_data(self, getlabel): 
        
        yearlist = self.request.GET.getlist('year')

        logger.info('USER: %s ACTION: %s MESSAGE: %s %s',
                self.user,   '勾選年份', "勾選 ",yearlist) 

        if yearlist==[]:
            args = {'messages':['至少勾選一個年份']}
            return args
            # return select_which_Label(request, getlabel, args) 

        args = {"userName":self.user,"labeltype":getlabel}
        for i in list(self.request.GET.keys()): 
            args[i] = self.request.GET[i]
            
            
       
        
        userfolder = f"User/{self.user}/"

        sourcefolder = f"User/{self.user}/SavFile/"
        targetfolder = f"User/{self.user}/SavFile/"
        
        # copyfilefolder_from_targetfolder = targetfolder+'year/'

        # os.makedirs(targetfolder, exist_ok = True) 
        # os.makedirs(copyfilefolder_from_targetfolder, exist_ok = True)
        print('userfolder=', userfolder)
        # files = fileprocess.How_many_rawfile(userfolder, fileextension = r'.sav')
        # print('file=', files)

        print(args)
        results = ''



        for savefile in yearlist:
            results = results+savefile+'，'
            print(savefile+'.sav')
            error = Write_in_sav(savefile+'.sav', userfolder,sourcefolder, targetfolder, args)
        if not error:    
            results = results+'寫入成功'
        else:
            results = results+'寫入失敗'
        # Write_in_database(getlabel,args)

        logger.info('USER: %s ACTION: %s MESSAGE: %s %s %s',
                self.user,   '按下寫入按鈕', '建 ',getlabel," 成功") 
        
        args = {'messages':[results]}
        print('arg=',args)

        fileprocess.remove_file(f"User/{self.user}/filter/{getlabel}/latest.npz")
        print('getlabel = ', getlabel)
        if getlabel=='Machine':
           fileprocess.remove_file(f"User/{self.user}/filter/tripline/latest.npz") 
           fileprocess.remove_file(f"User/{self.user}/filter/tripline/bus.npz")
        

        # for savfile_name in yearlist:

        #     cmd = Run_pyfile_by_execmd(python_location= "python"
        #                         ,pyfile= "web/src/pssefunction/filter.py"
        #                         ,args= f"--Label_type {getlabel} "\
        #                                 f"--Sav_File {savfile_name} "
        #                                 f"--User_name {self.user} " 
        #                                 f"--Source_savFile {sourcefolder}/{savfile_name}.sav ")
        return args
        # return select_which_Label(request, getlabel, args)                                                                  
       
     
