
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
from .get_filter_data import  GetData

def writeFile(filename, data):  
    f = open(filename, "a")  
    f.write(data)  
    f.close() 




class CheckDataExist:
    def __init__(self,datapath,datadir):
        self.datapath = datapath
        self.datadir = datadir

    def twowinding(self, data):
        two_winding_data = GetData(self.datapath
                            ).two_winding_transformer_data(self.datadir)
        datakey = {}                    
        for twowindingdata in two_winding_data:
            datakey[f'{twowindingdata["fromnum"]},{twowindingdata["tonum"]},{twowindingdata["transformer_id"]}'] = True

        return datakey.get(f"{data['FromBusNumber']},{data['ToBusNumber']},{data['ID']}",False)


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

            psspycommand =  {   'function':'area_data',
                                'data':[f"{area_number}" 
                                        ," "
                                        ," "
                                        ," "
                                        ,f"'{area_name}'"],
                                'labeltype':'area'
                            }
            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").area()
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)
            writeFile(filename=f"temp/{self.user}/writedata/show/area.idv", data=f"{area_number},'{area_name}'\n")

            messages.success(self.request, '成功新增 area ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='AREA')        


    def write_zonedata_to_savfiles(self):
        zone_number = self.request.GET.get('ZONENumber')
        zone_name = self.request.GET.get('ZONEName')
        if zone_number and zone_name:
            psspycommand =  {   'function':'zone_data',
                                'data':[f"{zone_number}" 
                                        ,f"'{zone_name}'"],
                                'labeltype':'zone'
                            }
            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").zone()
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)
            writeFile(filename=f"temp/{self.user}/writedata/show/zone.idv", data=f"{zone_number},'{zone_name}'\n")

            messages.success(self.request, '成功新增 zone ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(zone number, zone name)')

        return redirect('select_Label', selection_Label='ZONE')   

  

    def write_ownerdata_to_savfiles(self):
        owner_number = self.request.GET.get('OwnerNumber')
        owner_name = self.request.GET.get('OwnerName')

        
        if owner_number and owner_name:

            psspycommand =  {   'function':'owner_data',
                                'data':[f"{owner_number}" 
                                        ,f"'{owner_name}'"],
                                'labeltype':'owner'
                            }
            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").owner()
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)
            writeFile(filename=f"temp/{self.user}/writedata/show/owner.idv", data=f"{owner_number},'{owner_name}'\n")

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


        

        if bus_number and bus_name:

            psspycommand =  {   'function':'bus_data_4',
                                'data':[f'{bus_number}', 
                                        '0',
                                        f'{Code}',f'{Area_Num}',f'{Zone_Num}',f'{Owner_Num}',
                                        f'{Base_kV}',f'{Voltage}',f'{Angel}',f'{Normal_Vmax}',f'{Normal_Vmin}',f'{Emergency_Vmax}',f'{Emergency_Vmin}',
                                        f"'{bus_name}'"],
                                'labeltype':'bus'
                            }
            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").bus()
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)
            writeFile(filename=f"temp/{self.user}/writedata/show/bus.idv", data=f"{bus_number},'{bus_name}',{Code},{Area_Num},{Zone_Num},{Owner_Num},{Base_kV},{Voltage},{Angel},{Normal_Vmax},{Normal_Vmin},{Emergency_Vmax},{Emergency_Vmin}\n")

            messages.success(self.request, '成功新增 Bus ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(owner number, owner name)')

        return redirect('select_Label', selection_Label='BUS') 



    def write_machine_to_savfiles(self):

        BUS_Number = int(self.request.GET.get('BusNumber'))
        ID = self.request.GET.get('ID')
        # ID = '1'
        MachineControlMode = int(self.request.GET.get('MachineControlMode'))
        BASE = self.request.GET.get('BASE')
        Pgen = self.request.GET.get('Pgen')
        Qgen = self.request.GET.get('Qgen')
        
        Qmax = self.request.GET.get('Qmax')
        Qmin = self.request.GET.get('Qmin')
        Pmax = self.request.GET.get('Pmax')
        Pmin = self.request.GET.get('Pmin')
        Mbase = self.request.GET.get('Mbase')
        RSource = self.request.GET.get('RSource')
        XSource = self.request.GET.get('XSource')

        #seq machine
        R = self.request.GET.get('R')        
        SubtransientX = self.request.GET.get('SubtransientX')
        RNegative = self.request.GET.get('RNegative')
        XNegative = self.request.GET.get('XNegative')
        RZero = self.request.GET.get('RZero')
        XZero = self.request.GET.get('XZero')
        TransientX = self.request.GET.get('TransientX')
        SynchronousX = self.request.GET.get('SynchronousX')

        

        if BUS_Number:
            psspycommand =  {   'function':'machine_data_3',
                                'data':[str(BUS_Number)
                                        ,str(ID)
                                        ,'0','1','0','0','0',str(MachineControlMode),str(BASE)
                                        ,str(Pgen),str(Qgen),str(Qmax),str(Qmin),str(Pmax),str(Pmin),str(Mbase),str(RSource),str(XSource)
                                        ,"","","","","","","",""
                                        ,""],
                                'labeltype':'machine'
                            }

            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").machine()
            psspycommand =  {   'function':'seq_machine_data_3',
                                'data':[str(BUS_Number)
                                        ,str(ID)
                                        ,'0'
                                        ,str(R),str(SubtransientX),str(RNegative),str(XNegative),str(RZero),str(XZero),str(TransientX),str(SynchronousX)
                                        ,"0.0","0.0","0.0"],
                                'labeltype':'seq_machine'
                            }     
            results_of_convert = psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").machine()                                   
            print(results_of_convert)
                
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)
            writeFile(filename=f"temp/{self.user}/writedata/show/machine.idv", data=f"{BUS_Number},{ID},{MachineControlMode},{BASE},{Pgen},{Qgen},{Qmax},{Qmin},{Pmax},{Pmin},{Mbase},{RSource},{XSource}"\
                                                                                f",{R},{SubtransientX},{RNegative},{SubtransientX},{XNegative},{RZero},{XZero},{TransientX},{SynchronousX}\n")

            messages.success(self.request, '成功新增 Machine ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(Machine number, Machine name)')

        return redirect('select_Label', selection_Label='Machine')


    def write_loaddata_to_savfiles(self):

        bus_number = self.request.GET.get('BusNumber')
        Pload = self.request.GET.get('Pload')
        Qload = self.request.GET.get('Qload')

        

        if bus_number:
            psspycommand =  {   'function':'load_data_6',
                                'data':[str(bus_number), 
                                        ' ',
                                        ' ',' ',' ',' ',' ',' ',' ',
                                        str(Pload),str(Qload),' ',' ',' ',' ',' ',' ',],
                                'labeltype':'load'
                            }            
            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").load()
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)
            writeFile(filename=f"temp/{self.user}/writedata/show/load.idv", data=f"{bus_number},{Pload},{Qload}\n")

            messages.success(self.request, '成功新增 load ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(load number)')

        return redirect('select_Label', selection_Label='LOAD')   
 

    def write_branchdata_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('FromBusNumber'))
        ToBusNumber = int(self.request.GET.get('ToBusNumber'))
        ID = self.request.GET.get('ID')
        LineR = float(self.request.GET.get('LineR'))
        LineX = float(self.request.GET.get('LineX'))
        ChargingB = float(self.request.GET.get('ChargingB'))
        Length = self.request.GET.get('Length')
        
        if Length != "":
            Length = float(Length)
        else:
            Length = 0.0    
        RATE1 = float(self.request.GET.get('RATE1'))  
        NAME = self.request.GET.get('NAME')
        if NAME!='':
            NAME = f"'{NAME}'"
            
        #seq branch
        R_Zero = float(self.request.GET.get('R_Zero')) 
        X_Zero = float(self.request.GET.get('X_Zero'))  
        B_Zero = float(self.request.GET.get('B_Zero'))


        if FromBusNumber:

            psspycommand =  {   'function':'branch_data_3',
                    'data':[str(FromBusNumber), 
                            str(ToBusNumber),
                            ID,
                            ' ',' ',' ',' ',' ',' ',
                            str(LineR),str(LineX),str(ChargingB),' ',' ',' ',' ',str(Length),' ',' ',' ',' ',
                            str(RATE1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                            NAME],
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
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)

            writeFile(filename=f"temp/{self.user}/writedata/show/branch.idv", data=f"{FromBusNumber},{ToBusNumber},{ID},{LineR},{LineX},{ChargingB},{RATE1},{R_Zero},{X_Zero},{B_Zero},{Length},{NAME}\n")

            messages.success(self.request, '成功新增 branch ，尚未寫入，請到預覽查看新增內容並寫入')
        else:
            messages.warning(self.request, '請填入必填資訊(from number)')

        return redirect('select_Label', selection_Label='LOABRANCHD')               


    def write_twowinding_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('FromBusNumber'))
        ToBusNumber = int(self.request.GET.get('ToBusNumber'))
        ID = self.request.GET.get('ID')

        ControlledBus = self.request.GET.get('ControlledBus')
        if ControlledBus=='':
            ControlledBus = FromBusNumber
        else:
            ControlledBus = int(ControlledBus)
        
        Winding_int = self.request.GET.get('Winding_int')
        if Winding_int!='':
           Winding_int = int(Winding_int) 
        Impedance = self.request.GET.get('Impedance')
        if Impedance!='':
            Impedance = int(Impedance)
        Admittance = self.request.GET.get('Admittance')
        if Admittance!='':
            Admittance = int(Admittance)

        SpecifiedR = self.request.GET.get('SpecifiedR')
        if SpecifiedR!='':
            SpecifiedR = float(SpecifiedR)
        SpecifiedX = self.request.GET.get('SpecifiedX')
        if SpecifiedX!='':
            SpecifiedX = float(SpecifiedX)
        Winding = self.request.GET.get('Winding')
        if Winding!='':
            Winding = float(Winding)
        Wind1 = self.request.GET.get('Wind1')
        if Wind1!='':
            Wind1 = float(Wind1)

        Wind1Ratio = self.request.GET.get('Wind1Ratio')
        if Wind1Ratio!='':
            Wind1Ratio = float(Wind1Ratio)

        Wind2Ratio = self.request.GET.get('Wind2Ratio')
        if Wind2Ratio!='':
            Wind2Ratio = float(Wind2Ratio)

        Wind2 = self.request.GET.get('Wind2')
        if Wind2!='':
            Wind2 = float(Wind2)
        RATE1 = self.request.GET.get('RATE1')
        if RATE1!='':
            RATE1 = float(RATE1)
        Name = self.request.GET.get('Name')
        if Name!='':
            Name = f"'{Name}'"
        #seq 2winding
        Connection = self.request.GET.get('Connection')
        if Connection!='':
            Connection = int(Connection)
        R01 = self.request.GET.get('R01')
        if R01!='':
            R01 = float(R01)
        X01 = self.request.GET.get('X01')
        if X01!='':
            X01 = float(X01)




        if FromBusNumber and ToBusNumber:
            if CheckDataExist(    datapath=f"../Data/User/{self.user}/filter/two_winding_transformer/latest.npz",
                                datadir=f"../Data/User/{self.user}/filter/two_winding_transformer"
                            ).twowinding(data={"FromBusNumber":FromBusNumber,
                                                "ToBusNumber":ToBusNumber,
                                                "ID":ID
                                                }
                                        ):
                psspycommand =  {   'function':'two_winding_chng_6',
                                    'data':[f'{FromBusNumber}', 
                                            f'{ToBusNumber}',
                                            f"'{ID}'",
                                            '','','','','','','','',
                                            str(ControlledBus),                                            
                                            '','','','0',f'{Winding_int}',f'{Impedance}',f'{Admittance}',
                                            f'{SpecifiedR}',f'{SpecifiedX}',f'{Winding}',f'{Wind1Ratio}',f'{Wind1}','',f'{Wind2Ratio}',f'{Wind2}','','','','','','','','','','','','','',
                                            f'{RATE1}',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                            f"{Name}",'" "'],
                                    'labeltype':'twowinding'
                                }
                psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").twowinding_edit()                
            else:                            
                psspycommand =  {   'function':'two_winding_data_6',
                                    'data':[str(FromBusNumber), 
                                            str(ToBusNumber),
                                            ID,
                                            ' ',' ',' ',' ',' ',' ',' ',' ',str(ControlledBus),' ',' ',' ',' ',str(Winding_int),str(Impedance),str(Admittance),
                                            str(SpecifiedR),str(SpecifiedX),str(Winding),str(Wind1Ratio) ,str(Wind1),' ',str(Wind2Ratio),str(Wind2),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
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
                
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)

            writeFile(filename=f"temp/{self.user}/writedata/show/twowinding.idv"
            , data=f"{FromBusNumber},{ToBusNumber},{ID},{ControlledBus},{Winding_int},{Impedance},{Admittance},{SpecifiedR},{SpecifiedX},{Winding},{Wind1},{Wind1Ratio},{Wind2Ratio},{Wind2},{RATE1},{Name},{Connection},{R01},{X01}\n")

            
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
        if Name!="":
            Name = f"'{Name}'"


        R01 = self.request.GET.get('R01')
        if R01!="":
            R01 = float(R01)

        X01 = self.request.GET.get('X01')
        if X01!="":
            X01 = float(X01)
        
        R02 = self.request.GET.get('R02')
        if R02!="":
            R02 = float(R02)
                   
        X02 = self.request.GET.get('X02')
        if X02!="":
            X02 = float(X02)
                  
        R03 = self.request.GET.get('R03')
        if R03!="":
            R03 = float(R03)
                    
        X03 = self.request.GET.get('X03')
        if X03!="":
            X03 = float(X03)


        if FromBusNumber and ToBusNumber and LastBusNumber: 

            psspycommand =  {   'function':'three_wnd_imped_data_4',
                                'data':[str(FromBusNumber), 
                                        str(ToBusNumber),
                                        str(LastBusNumber),
                                        ID,
                                        ' ',' ',' ',' ',str(Winding),str(Impedance),str(Admittance),' ',' ',' ',' ',' ',str(ImpaedanceAdjustmentCode),
                                        str(W12R),str(W12X),str(W23R),str(W23X),str(W31R),str(W31X),str(Winding12MVABase),str(Winding23MVABase),str(Winding31MVABase),' ',' ',' ',' ',' ',' ',' ',' ',
                                        Name,
                                        "' '"],
                                'labeltype':'three_wnd_imped_data_4'
                            }

            psspy_to_idv(psspycommand=psspycommand, idvpath=f"temp/{self.user}/writedata").threewinding()
            
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

            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)

            writeFile(filename=f"temp/{self.user}/writedata/show/threewinding.idv"
            , data = f"{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},{Name},{Winding},{Impedance},{Admittance},{W12R},{W12X},{W23R},{W23X},{W31R},{W31X},{Winding12MVABase},{Winding23MVABase},{Winding31MVABase},{ImpaedanceAdjustmentCode},{connection},{R01},{X01},{R02},{X02},{R03},{X03}\n")

            messages.success(self.request, '成功新增 three winding ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='TRANSFORMER3Winding')  

    def write_threewinding_winding_to_savfiles(self):

        FromBusNumber = int(self.request.GET.get('windingsFromBusNumber'))
        
        ToBusNumber = int(self.request.GET.get('windingsToBusNumber'))

        LastBusNumber = int(self.request.GET.get('windingsLastBusNumber'))        


        BusNumber = self.request.GET.get('busnumber_to_modify')
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
        

    

        if FromBusNumber:
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
            os.makedirs(f"temp/{self.user}/writedata/show",exist_ok=True)

            writeFile(filename=f"temp/{self.user}/writedata/show/threewinding_winding.idv"
            , data = f"{FromBusNumber},{ToBusNumber},{LastBusNumber},{BusNumber},{Tap_Positions},{Impendance},{Controlled},{Ratio},{Nominal},{Angle},{Rmax},{Rmin},{Vmax},{Vmin},{Load_Drop_1},{Load_Drop_2},{Wnd_Connect},{RATE1},{RATE2},{RATE3},{RATE4},{RATE5},{RATE6},{RATE7},{RATE8},{RATE9},{RATE10},{RATE11},{RATE12}\n")
        
            
            messages.success(self.request, '成功新增 three winding_winding ，尚未寫入，請到預覽查看新增內容並寫入')
        
        return redirect('select_Label', selection_Label='TRANSFORMER3Winding')  
