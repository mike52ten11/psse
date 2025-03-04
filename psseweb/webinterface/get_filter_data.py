import os
import numpy as np
import requests

from django.http import JsonResponse
from .readconfig import read_config

def get_filterfile_num(url:str, params:dict):

    response = requests.get(url
                            , params=params
                            
                            )   
    if response.status_code == 200:
        return response.json()["results"]


    else:    
        return []

class GetData:

    def __init__(self):
        self.proxies = {
                        'http': None,
                        'https': None,
                    }        
        # self.api_ip = '10.52.20.21'    
        # self.api_port = '800'
        self.server_settings = read_config()
        self.url = f"http://{self.server_settings['server_host']}:{self.server_settings['server_port']}"

    def trip_line_data(self, params):
        # filterfiles = args.get('filterfiles')
        # filterdir = args.get('filterdir')
        # labeltype = args.get('labeltype')
        busfaultnum = params.get('busfaultnum')
        # filter_data = np.load(f"{filterdir}/{labeltype}/{labeltype}_{filterfiles}.npz")

        print('params',params)            
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)

            list_data = messages["results"]

            # listdata_num = filter_data['num'][np.where(filter_data['fromnum']==int(busfaultnum))]
            # listdata_name = filter_data['name'][np.where(filter_data['fromnum']==int(busfaultnum))]
            # listdata_circuit_id = filter_data['circuit_id'][np.where(filter_data['fromnum']==int(busfaultnum))]
            

                            
            # list_data = [
            #                 {'num': int(num), 'name': name,'circuit_id':circuit_id}
            #                 for num, name, circuit_id in zip(listdata_num, listdata_name,listdata_circuit_id)
            #             ] 

            # print(list_data)                         
            return JsonResponse({'data':list_data}, safe=False) 

        else:    
            filter_data = []    
            return JsonResponse({'data':filter_data}, safe=False)
        



    def machine_data(self, params): 

        if params['filterfiles']=='latest':
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/machine"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]

            # print(list_data)
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)

    def bus_data(self,params):

                    
        if params['filterfiles']=='latest':
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/bus"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
                                        
            if'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]

            # print(list_data)
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)    

    def zone_data(self,params):

                    
        if params['filterfiles']=='latest':
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/zone"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]

            # print(list_data)
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)  

    def area_data(self,params):

                    
        if params['filterfiles']=='latest':
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/area"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]

            # print(list_data)
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)                     

    def owner_data(self, params):

                    
        if params['filterfiles']=='latest':
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/owner"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]

            # print(list_data)
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)  

    def load_data(self, params):

                    
        if params['filterfiles']=='latest':
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/load"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]

            # print(list_data)
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)   

    def branch_data(self, params):

                    
        if params['filterfiles']=='latest':
            #找filter/{labeltype}資料夾下有哪些filter檔案
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/branch"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]
            # print(list_data)
            
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)
            
    def three_winding_transformer_data(self, params):

                    
        if params['filterfiles']=='latest':
            #找filter/{labeltype}資料夾下有哪些filter檔案
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/three_winding_transformer"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]
            # print(list_data)
            
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)                         

    def two_winding_transformer_data(self, params):

                    
        if params['filterfiles']=='latest':
           
            #找filter/{labeltype}資料夾下有哪些filter檔案
            filterfiles = get_filterfile_num(f"{self.url}/filter_labelfile"
                                        , params={"sourcedir":f"{params['filterdir']}/two_winding_transformer"}
                                        # , settings = {"proxy":self.proxies}
                                        ) 
            if 'latest' in filterfiles:
                params['filterfiles'] = ['latest']
            else:
                params['filterfiles'] = filterfiles
        print('params',params)
        response = requests.get(f"{self.url}/get_filter_data/"
                                , params = params
                                # , proxies = self.proxies
                                )        
        if response.status_code == 200:
            messages = response.json()
            # print(messages)
            list_data = messages["results"]
            # print(list_data)
            
            return JsonResponse({'data':list_data}, safe=False)
        else:    
            list_data = []    

            return JsonResponse({'data':list_data}, safe=False)     