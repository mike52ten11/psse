import os
import numpy as np
import requests

from django.http import JsonResponse
from .readconfig import read_config
from .src.base.create_latest_npzfile import CreateLatestNpzfile

def create_latest_npzfile(filterfiles, filterdir):

    filterfile_name = filterfiles[0]
    user_data_of_labeltype = np.load(f"{filterdir}/{filterfile_name}.npz")

    
    Num, Name = user_data_of_labeltype["num"], user_data_of_labeltype['name']
    mapping = dict(zip(Num, Name))


    for filterfile_name in filterfiles[1:len(filterfiles)]:
        
        user_data_of_labeltype = np.load(f"{filterdir}/{filterfile_name}.npz")
        
        mapping.update(dict(zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'])))     
        


    Num = np.array(list(mapping.keys()))
    
    Name = np.array(list(mapping.values()))
    np.savez(f'{filterdir}/latest.npz', name=Name, num=Num)        
    data_of_labeltype = [
        {'num': num, 'name': name}
        for num, name in zip(Num, Name)
    ]        
    
    return data_of_labeltype   




class GetData:

    def __init__(self, npzfile):
        self.npzfile = npzfile

    def trip_line_data_for_api(self,busfaultnum):
        filtervalue = np.load(self.npzfile)
        listdata_tonum = filtervalue['tonum'][np.where(filtervalue['fromnum']==busfaultnum)]
        listdata_toname = filtervalue['toname'][np.where(filtervalue['fromnum']==busfaultnum)]
        listdata_tobus_id = filtervalue['id'][np.where(filtervalue['fromnum']==busfaultnum)] 

        
        listdata_fromnum = filtervalue['fromnum'][np.where(filtervalue['tonum']==busfaultnum)]
        listdata_fromname = filtervalue['fromname'][np.where(filtervalue['tonum']==busfaultnum)]
        listdata_frombus_id = filtervalue['id'][np.where(filtervalue['tonum']==busfaultnum)]

        listdata_num = np.concatenate((listdata_tonum, listdata_fromnum))
        listdata_name = np.concatenate((listdata_toname, listdata_fromname))
        listdata_id = np.concatenate((listdata_tobus_id, listdata_frombus_id))

        filtervalue = [
                        {'num': int(num), 'name': name,'id':circuit_id}
                        for num, name, circuit_id in zip(listdata_num, listdata_name,listdata_id)
                    ]          
        return    JsonResponse({'data':filtervalue}, 
                                    json_dumps_params={'ensure_ascii': False},
                                    safe=False)                            

        



    def machine_data_for_api(self,filterdir): 
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                    {'num': int(num), 'name': name, "machine_id":machine_id}
                    for num, name, machine_id in zip(filtervalue["num"]
                                        , filtervalue['name']
                                        ,filtervalue['machine_id'])
                
                    ]
                    
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).machine_data()
            return  JsonResponse({'data':list_data}, safe=False)  
                    
    def machine_data_for_api_of_dynamic(self,filterdir): 
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                    {'num': int(num), 'name': name, "machine_id":machine_id}
                    for num, name, machine_id in zip(filtervalue["num"]
                                        , filtervalue['name']
                                        ,filtervalue['machine_id'])
                
                    ]
                    
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            return JsonResponse({'data':[]}, safe=False)  

    def bus_data_for_api(self, filterdir):
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'num': int(num), 'name': name, "zonenum":int(zonenum), "zonename":zonename}
                        for num, name, zonenum,zonename in zip(filtervalue["num"]
                                        , filtervalue['name']
                                        ,filtervalue['zonenum']
                                        ,filtervalue['zonename'])
                    ]
                     
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).bus_data()
            return  JsonResponse({'data':list_data}, safe=False)         


    def zone_data_for_api(self, filterdir):
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'num': int(num), 'name': name}
                        for num, name in zip(filtervalue["num"]
                                            , filtervalue['name'])
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).zone_data()
            return  JsonResponse({'data':list_data}, safe=False) 


    def zone_data(self):

        filtervalue = np.load(self.npzfile)
        return  [
                    {'num': int(num), 'name': name}
                    for num, name in zip(filtervalue["num"]
                                        , filtervalue['name'])
                ]       


    def area_data_for_api(self, filterdir):
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'num': int(num), 'name': name}
                        for num, name in zip(filtervalue["num"]
                                            , filtervalue['name'])
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).area_data()
            return  JsonResponse({'data':list_data}, safe=False) 
 
                    


    def area_data(self):
        filtervalue = np.load(self.npzfile)
        # filtervalue = [
        #             {'num': int(num), 'name': name}
        #             for num, name in zip(filtervalue["num"]
        #                                 , filtervalue['name'])
        #         ]
        return [
                    {'num': int(num), 'name': name}
                    for num, name in zip(filtervalue["num"]
                                        , filtervalue['name'])
                ] 

    def owner_data_for_api(self,filterdir):

        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'num': int(num), 'name': name}
                        for num, name in zip(filtervalue["num"]
                                            , filtervalue['name'])
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).owner_data()
            return  JsonResponse({'data':list_data}, safe=False) 
 

    def owner_data(self):

        filtervalue = np.load(self.npzfile)

        return   [
                    {'num': int(num), 'name': name}
                    for num, name in zip(filtervalue["num"]
                                        , filtervalue['name'])
                ]
    
    def load_data_for_api(self, filterdir):
            
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'num': int(num), 'name': name}
                        for num, name in zip(filtervalue["num"]
                                            , filtervalue['name'])
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).load_data()
            return  JsonResponse({'data':list_data}, safe=False)    

    def branch_data_for_api(self, filterdir):
            
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname,'id':id}
                        for fromnum, fromname, tonum, toname,id in zip(filtervalue["fromnum"]  
                                            , filtervalue['fromname']
                                            , filtervalue['tonum']
                                            , filtervalue['toname']
                                            , filtervalue['id'])
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).branch_data()
            return  JsonResponse({'data':list_data}, safe=False) 
            
    def three_winding_transformer_data_for_api(self, filterdir):

        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname, 'lastnum':lastnum, 'lastname':lastname,'transformer_id':transformer_id, 'transformer_name':transformer_name}
                        for fromnum, fromname, tonum, toname, lastnum, lastname, transformer_id, transformer_name in zip(filtervalue["fromnum"]  
                                            , filtervalue['fromname']
                                            , filtervalue['tonum']
                                            , filtervalue['toname']
                                            , filtervalue['lastnum']
                                            , filtervalue['lastname']
                                            , filtervalue['transformer_id']
                                            , filtervalue['transformer_name']
                                            )
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).three_winding_transformer_data()
            return  JsonResponse({'data':list_data}, safe=False)                      

    def two_winding_transformer_data_for_api(self, filterdir):
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname,'transformer_id':transformer_id}
                        for fromnum, fromname, tonum, toname,transformer_id in zip(filtervalue["fromnum"]  
                                            , filtervalue['fromname']
                                            , filtervalue['tonum']
                                            , filtervalue['toname']
                                            , filtervalue['transformer_id'])
                    ]
            return  JsonResponse({'data':list_data}, safe=False)              
        else:
            list_data = CreateLatestNpzfile(filterdir).two_winding_transformer_data()
            return  JsonResponse({'data':list_data}, safe=False) 

    def two_winding_transformer_data(self, filterdir):
        if os.path.exists(self.npzfile):
            filtervalue = np.load(self.npzfile)
            list_data = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname,'transformer_id':transformer_id}
                        for fromnum, fromname, tonum, toname,transformer_id in zip(filtervalue["fromnum"]  
                                            , filtervalue['fromname']
                                            , filtervalue['tonum']
                                            , filtervalue['toname']
                                            , filtervalue['transformer_id'])
                    ]
            return  list_data    
        else:
            list_data = CreateLatestNpzfile(filterdir).two_winding_transformer_data()
            return  list_data