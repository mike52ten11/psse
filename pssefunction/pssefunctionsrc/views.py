import os
import json
import numpy as np
import shutil

from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.http import Http404

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

from .class_for_views.upload import Upload
from .class_for_views.delete import Delete
from .class_for_views.search import SearchFiles
# from .class_for_views.writedata import WriteData

from .src import fileprocess
from .src import run_powerflow
from .src import run_powerflow_subline
from .src import run_error_circuit
from .src import run_dynamic
from .src.run_filter import run_filter
from .src.download_file import MyDownload

from .src.base import filter_num_and_name_bylabel
from .src.base.how_many_sav_file import (How_many_SavFile_in_UserFolder
                                        ,How_many_filter_file_in_UserFolder
                                        ,How_many_acc_in_dir
                                        ,How_many_rel_in_dir
                                        ,How_many_out_in_dir
                                        )


def convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(element) for element in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    return obj


class NumpyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super().default(obj)


@csrf_exempt
@require_http_methods(["POST"])
def upload_savfile(request):

    return Upload(request).upload_savfile()
 
@csrf_exempt
@require_http_methods(["POST"])
def upload_dynamicfile(request):
    
    return Upload(request).upload_dynamicfile()


@csrf_exempt
@require_http_methods(["POST"])
def upload_idvfile(request):

    return Upload(request).upload_idvfile()

@csrf_exempt
@require_http_methods(["POST"])
def upload_idvfile_of_writata(request):
    print(request.user)
    return Upload(request).upload_idvfile_of_writata()

@csrf_exempt
@require_http_methods(["POST"])
def delete_savfile(request):

    return Delete(request).action_of_delete_savfile()



###
###===================================================
###                    找 檔案
###===================================================
###
def find_savfile(request):


    return JsonResponse(
                            {
                                'results':SearchFiles(request).search_savfiles()
                            }
                            , json_dumps_params={'ensure_ascii': False}
                            , safe=False
                        )

def find_acc_files_in_dir(request):

    return JsonResponse(
                            {
                                'results':SearchFiles(request).search_accfiles()
                            }
                            , json_dumps_params={'ensure_ascii': False}
                            , safe=False
                        )


def find_rel_files_in_dir(request):

    return JsonResponse(
                            {
                                'results':SearchFiles(request).search_relfiles()
                            }
                            , json_dumps_params={'ensure_ascii': False}
                            , safe=False
                        )

def find_out_files_in_dir(request):

    return JsonResponse(
                            {
                                'results':SearchFiles(request).search_outfiles()
                            }
                            , json_dumps_params={'ensure_ascii': False}
                            , safe=False
                        )


def filter_labelfile(request):
    print(request.GET.get('sourcedir'))
    return JsonResponse(
                            {
                                'results':SearchFiles(request).search_labelfiles()
                            }
                            , json_dumps_params={'ensure_ascii': False}
                            , safe=False
                        )

def filter_label(request):
    labeltype = request.GET.get('labeltype')
    savefile = request.GET.get('savefile')
    savfiledir = request.GET.get('savfiledir')
    filterdir = request.GET.get('filterdir')
    targetdir = request.GET.get('targetdir')

    user = request.GET.get('user')
    print('savefile = ', savefile)

    filtervalue = filter_num_and_name_bylabel.Display_X_Label(labeltype = labeltype
                                                    ,savfiledir = savfiledir
                                                    ,user = user
                                                    ,filterdir = filterdir
                                                    ,targetdir = targetdir).filter_labeltype_num_name(savefile = savefile)
    # filtervalue = [{
    #     'num': int(item['num']),  # 將 numpy.int32 轉換為 Python int
    #     'name': str(item['name'])  # 確保 name 是 string 類型
    # } for item in filtervalue]       
    
    return    JsonResponse({'results':"ok"}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)   

def filter_all_label(request):
    savefiles = request.GET.getlist('savefile')
    savfile_dir = request.GET.get('savfile_dir')
    filter_dir = request.GET.get('filter_dir')
    target_dir = request.GET.get('target_dir')
    user = request.GET.get('user')

    # fileprocess.remove_dir(f'{filter_dir}')
    # fileprocess.remove_file(f'{filter_dir}/load/latest.npz')
    # fileprocess.remove_file(f'{filter_dir}/owner/latest.npz')
    # fileprocess.remove_file(f'{filter_dir}/zone/latest.npz')

    
    print(filter_dir)
    for savfile in savefiles:
        Delete(request).action_of_filter_all(filter_dir,savfile)
        result = run_filter(filename=savfile, rawfilepath=f"{savfile_dir}/{savfile}.raw", filter_dir=filter_dir)
        print('result -->',result)
        if isinstance(result, dict) and "error" in result:  # 如果回傳了錯誤
            # 根據需求處理錯誤
            return    JsonResponse({'messages':f'製作filter檔案失敗，\nfunction:{result["error"]["function"]}，錯誤訊息:{result["error"]["message"]}，{result["error"]["type"]}\nTraceback:\n{result["error"]["traceback"]}'}, 
                                        json_dumps_params={'ensure_ascii': False},
                                        safe=False)      
        # try:
            
        # except Exception as e:
        #     return    JsonResponse({'messages':f'製作filter檔案失敗，\n{e}'}, 
        #                                 json_dumps_params={'ensure_ascii': False},
        #                                 safe=False)                    
        # filtervalue = filter_num_and_name_bylabel.Display_X_Label(labeltype = 'all'
        #                                                 ,savfiledir = savfile_dir
        #                                                 ,user = user
        #                                                 ,filterdir = filter_dir
        #                                                 ,targetdir = target_dir).filter_all(savfile_name = savfile)
    filtermessages = ''

    if not os.path.exists(f"{filter_dir}/area/area_{savefiles[0]}.npz"):
       filtermessages += 'area 錯誤，'

    if not os.path.exists(f"{filter_dir}/branch/branch_{savefiles[0]}.npz"):
       filtermessages += 'branch 錯誤，'

    if not os.path.exists(f"{filter_dir}/bus/bus_{savefiles[0]}.npz"):
       filtermessages += 'bus 錯誤，'

    if not os.path.exists(f"{filter_dir}/load/load_{savefiles[0]}.npz"):
       filtermessages += 'load 錯誤，'

    if not os.path.exists(f"{filter_dir}/machine/machine_{savefiles[0]}.npz"):
       filtermessages += 'machine 錯誤，'
       
    if not os.path.exists(f"{filter_dir}/owner/owner_{savefiles[0]}.npz"):
        filtermessages += 'owner 錯誤，'    

    if not os.path.exists(f"{filter_dir}/tripline/tripline_{savefiles[0]}.npz"):
        filtermessages += 'tripline 錯誤，'  

    if not os.path.exists(f"{filter_dir}/two_winding_transformer/two_winding_transformer_{savefiles[0]}.npz"):
        filtermessages += 'twowinding 錯誤，'  

    if not os.path.exists(f"{filter_dir}/three_winding_transformer/three_winding_transformer_{savefiles[0]}.npz"):
        filtermessages += 'threewinding 錯誤，' 

    if not os.path.exists(f"{filter_dir}/zone/zone_{savefiles[0]}.npz"):
        filtermessages += 'zone 錯誤，'

    

    if filtermessages=='':
        filtermessages = '上傳成功'
    else:
        filtermessages+='請重新上傳'  
    return    JsonResponse({'messages':filtermessages}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)           

def filter_dispaly(request):
    labeltype = request.GET.get('labeltype')
    
    filterfiles = request.GET.getlist('filterfiles')
    savfiledir = request.GET.get('savfiledir')
    filterdir = request.GET.get('filterdir')
    targetdir = request.GET.get('targetdir')

    user = request.GET.get('user')
    print('filterfiles',filterfiles)

    filtervalue = filter_num_and_name_bylabel.Display_X_Label(labeltype = labeltype
                                                    ,savfiledir = savfiledir
                                                    ,user = user
                                                    ,filterdir = filterdir
                                                    ,targetdir = targetdir).display_which_label(filterfiles = filterfiles)    
    filtervalue = [{
        'num': int(item['num']),  # 將 numpy.int32 轉換為 Python int
        'name': str(item['name'])  # 確保 name 是 string 類型
    } for item in filtervalue]       
    
    return    JsonResponse({'results':filtervalue}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False) 

def get_filter_data(request):

    labeltype = request.GET.get('labeltype')
    filterfiles = request.GET.getlist('filterfiles')
    filterdir = request.GET.get('filterdir')
    savfiledir = request.GET.get('savfiledir')
    user = request.GET.get('user')
    targetdir = request.GET.get('targetdir')
    fom_to_last_bus = request.GET.get('fom_to_last_bus',None)
    print('labeltype-->',labeltype)

    if len(filterfiles) > 1 :
         
        filtervalue = filter_num_and_name_bylabel.Display_X_Label(labeltype = labeltype
                                                        ,savfiledir = savfiledir
                                                        ,user = user
                                                        ,filterdir = filterdir
                                                        ,targetdir = targetdir).display_which_label(filterfiles = filterfiles)    

        filtervalue = np.load(f"{filterdir}/{labeltype}/latest.npz")
    elif filterfiles==  ['latest']:
        filtervalue = np.load(f"{filterdir}/{labeltype}/latest.npz")

    elif len(filterfiles) == 1:
        shutil.copyfile(f"{filterdir}/{labeltype}/{filterfiles[0]}.npz",f"{filterdir}/{labeltype}/latest.npz")
        filtervalue = np.load(f"{filterdir}/{labeltype}/latest.npz")        
        # filtervalue = np.load(f"{filterdir}/{labeltype}/{filterfiles[0]}.npz")
    else:
        return    JsonResponse({'results':f"error，filterfiles = {filterfiles}"}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False,
                                status=404)  
    if labeltype=='bus': 
        print(list(filtervalue.keys()))
        filtervalue = [
                    {'num': int(num), 'name': name, "zonenum":int(zonenum), "zonename":zonename}
                    for num, name, zonenum,zonename in zip(filtervalue["num"]
                                        , filtervalue['name']
                                        ,filtervalue['zonenum']
                                        ,filtervalue['zonename'])
                ]         
    elif labeltype=='tripline':
        busfaultnum = request.GET.get('busfaultnum')

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
        print(filtervalue)            
                    
    elif labeltype=='branch':
        if fom_to_last_bus=='from':
            filtervalue = [
                        {'num': int(num), 'name': name,}
                        for num, name in zip(
                                            filtervalue["fromnum"]
                                            , filtervalue['fromname']
                                            )
                    ]
            #不知道為甚麼就算使用python 內建強制轉int型。還是出現TypeError: Object of type int32 is not JSON serializable        
            #所以才使用下面的方式 convert_numpy_types
            # filtervalue = convert_numpy_types(filtervalue)
        elif   fom_to_last_bus=='to':
            filtervalue = [
                        {'num': int(num), 'name': name}
                        for num, name,  in zip(
                                            filtervalue['tonum']
                                            , filtervalue['toname']
                                            )
                    ]
        else:
            pass
        # print()       

    elif labeltype=='machine':
        filtervalue = [
                    {'num': int(num), 'name': name, "machine_id":machine_id}
                    for num, name, machine_id in zip(filtervalue["num"]
                                        , filtervalue['name']
                                        ,filtervalue['machine_id'])
                ]        
    elif labeltype=='three_winding_transformer':
        if fom_to_last_bus=='from':
            print(list(filtervalue.keys()))
            filtervalue = [
                            {'num': int(num), 'name': name}
                            for num, name in zip(filtervalue["fromnum"]
                                                , filtervalue['fromname'])
                        ]     
        elif  fom_to_last_bus=='to':   
            print(list(filtervalue.keys()))
            filtervalue = [
                            {'num': int(num), 'name': name}
                            for num, name in zip(filtervalue["tonum"]
                                                , filtervalue['toname'])
                        ] 
        elif  fom_to_last_bus=='last': 
            print(list(filtervalue.keys()))
            filtervalue = [
                            {'num': int(num), 'name': name}
                            for num, name in zip(filtervalue["lastnum"]
                                                , filtervalue['lastname'])
                        ]  
        else:
            pass                              


    elif labeltype=='two_winding_transformer':

        if  fom_to_last_bus=='from':
            print(list(filtervalue.keys()))
            filtervalue = [
                            {'num': int(num), 'name': name}
                            for num, name in zip(filtervalue["fromnum"]
                                                , filtervalue['fromname'])
                        ]      
        elif fom_to_last_bus=='to':
            
            filtervalue = [
                            {'num': int(num), 'name': name}
                            for num, name in zip(filtervalue["tonum"]
                                                , filtervalue['toname'])
                        ] 
        else:
            pass                             

    else:    

      
        filtervalue = [
                    {'num': int(num), 'name': name}
                    for num, name in zip(filtervalue["num"]
                                        , filtervalue['name'])
                ]
        
    return    JsonResponse({'results':filtervalue}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)   
def add_filter_data(request):
    labeltype = request.GET.get('labeltype')
    add_value = request.GET.get('add_value')
    filterdir = request.GET.get('filterdir')
    savfiledir = request.GET.get('savfiledir')
    user = request.GET.get('user')
    if labeltype=='area':
        num = now_area_data["num"]
        name = now_area_data["name"]

        new_num = np.append(num,area_number)
        new_name = np.append(name, area_name)

        np.savez(f'{self.filter_dir}/area/latest.npz', num=new_num, name=new_name)
        print('new_num-->', new_num)
        print('new_name-->',new_name)        


def powerflow(request):
    username = request.GET.get('username')
    yearlist = request.GET.getlist('yearlist')
    # convergence_thread_hold=request.GET.get('convergence_thread_hold')
    
    zone = request.GET.getlist('zone')
    minbasekv = request.GET.get('minbasekv')
    maxbasekv = request.GET.get('maxbasekv')
    confile_type = request.GET.get('confile_type')
    
    return_of_RUN_PowerFlow = run_powerflow.RUN_PowerFlow(username=username
                                                        ,yearlist=yearlist
                                                        # ,convergence_thread_hold=convergence_thread_hold
                                                        
                                                        ,zone=zone
                                                        ,minbasekv=minbasekv
                                                        ,maxbasekv=maxbasekv
                                                        ,confile_type=confile_type)


    args = { 'mismatch':[f'{front_value["content"]}' for front_value in return_of_RUN_PowerFlow["return_value"]]
        # ,'powerflow_sub':[[f'{front_value["content"]}'] for front_value in mismatch_sub["return_value"]]
        ,'messages':['執行PowerFlow完成']}                                                           
    return    JsonResponse({'messages':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)     


def powerflowsub(request):
    username = request.GET.get('username')
    yearlist = request.GET.getlist('yearlist')
    source_Folder = request.GET.get('source_Folder')
    powerflow_folder = request.GET.get('powerflow_folder')
    
    zone = request.GET.getlist('zone')
    minbasekv = request.GET.get('minbasekv')
    maxbasekv = request.GET.get('maxbasekv')


    return_of_sub = run_powerflow_subline.Run_Powerflow_of_subline(source_Folder=source_Folder
                                                                ,powerflow_folder=powerflow_folder
                                                                ,user=username
                                                                ,Sav_File=yearlist
                                                                ,zone_num=zone
                                                                ,maxbasekv=maxbasekv
                                                                ,minbasekv=minbasekv
                                                                )
    print('return_of_sub -->',return_of_sub["return_value"])
    mismatch_sub = []
    for front_value in return_of_sub["return_value"]:
        for sub_value in front_value:
            mismatch_sub.append(sub_value["content"])
    args = { 'mismatch':mismatch_sub
        # ,'powerflow_sub':[[f'{front_value["content"]}'] for front_value in mismatch_sub["return_value"]]
        ,'messages':['執行PowerFlow完成']}                                                           
    return    JsonResponse({'messages':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)                                                                                 

def errorcircuit(request):
    username = request.GET.get('username')
    savefiles = request.GET.getlist('savefiles')
    savfiledir = request.GET.get('savfile_dir')
    errorcircuitdir = request.GET.get('errorcircuit_dir')
    area = request.GET.getlist('area')
    zone = request.GET.getlist('zone')
    owner = request.GET.getlist('owner')
    minbasekv = request.GET.get('minbasekv')
    maxbasekv = request.GET.get('maxbasekv')
    print(savefiles)
    #Step 4 : 執行故障電流
    result = run_error_circuit.RUN_ErrorCircuit( username = username
                                ,savfiledir = savfiledir
                                ,savefiles = savefiles
                                ,errorcircuitdir = errorcircuitdir
                                ,logpath = f'Log/{username}/ErrorCircuitFunction_log/'
                                ,area=area
                                ,zone=zone
                                ,owner=owner
                                ,minbasekv=minbasekv
                                ,maxbasekv=maxbasekv)
    print("result >> ",result)
    # mismatch = " errocircut "
    if result["error"]:
        logger.error(result["which_log"]) 
        print(' result[return_value] >> ', result['return_value'])


        args = { 'mismatch':[f'{front_value["content"]}' for front_value in result["return_value"]]
                ,'messages':['執行失敗'] } 
    else:
        
            
        args = { 'mismatch':[f'{front_value["content"]}' for front_value in result["return_value"]], 
            'messages':['執行故障電流完成']}  


    return    JsonResponse({'messages':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)     


def dynamic(request):
    username = request.GET.get('username')
    resultdir = request.GET.get('result_dir')
    savfiledir = request.GET.get('savfile_dir')
    savfilename = request.GET.get('savfilename')

    dv_file = request.GET.get('dv_file')
    dll_file = request.GET.get('dll_file')        
    co_gen_file = request.GET.get('co_gen_file')

    print("dv_file >> ",dv_file)
    print("dll_file >> ",dll_file)
    print("co_gen_file >> ",co_gen_file)

    # dv_file = request.GET.get('dv_file')
    # dll_file = request.GET.get('dll_file')
    # co_gen_file = request.GET.get('co_gen_file')

    selected_machine_busnumber = request.GET.getlist('selected_machine_busnumber')
    selected_machine_busid = request.GET.getlist('selected_machine_busid')
    # filterdir = request.GET.get('filterdir')

    # machinedata = np.load(f"{filterdir}/machine/machine_{savfilename}.npz")

    
    # selected_machine_busid = []
    
    # for look_bus in selected_machine_busnumber:

    #     selected_machine_busid.append(machinedata['id'][np.where(machinedata['num']==int(look_bus))][0])


    dynamic_bus_fault_num = request.GET.get('dynamic_bus_fault_num')
    selected_dynamic_trip_line_num = request.GET.get('selected_dynamic_trip_line_num')
    circuit_id_for_elected_dynamic_trip_line = request.GET.get('circuit_id_for_elected_dynamic_trip_line')
    
    initial_time = request.GET.get('initial_time')   
    bus_fault_time = request.GET.get('bus_fault_time')
    trip_line_time = request.GET.get('trip_line_time')
    clear_fault_time = request.GET.get('clear_fault_time') 

    dynamic_dir = request.GET.get('dynamic_dir')

         
    #Step 4 : 執行故障電流
    result = run_dynamic.RUN_dynamic( username = username
                                ,resultdir = resultdir
                                ,savfile_Folder = savfiledir
                                ,savfilename = savfilename #f"{year}.sav"
                                ,dv_file = dv_file#f'User/{self.user}/Dynamic/{year}/{dv_file}'
                                ,dll_file = dll_file#f'User/{self.user}/Dynamic/{year}/{dll_file}'
                                ,co_gen_file = co_gen_file#f'User/{self.user}/Dynamic/{year}/{co_gen_file}'                                           
                                ,selected_machine_busnumber = selected_machine_busnumber
                                ,selected_machine_busid = selected_machine_busid
                                ,dynamic_bus_fault_num = dynamic_bus_fault_num
                                ,selected_dynamic_trip_line_num = selected_dynamic_trip_line_num
                                ,circuit_id_for_elected_dynamic_trip_line=circuit_id_for_elected_dynamic_trip_line
                                ,initial_time = initial_time
                                ,bus_fault_time = bus_fault_time
                                ,trip_line_time = trip_line_time
                                ,clear_fault_time = clear_fault_time
                                )
    print("result >> ",result)
    # mismatch = " errocircut "
    if result["error"]:
         
        print(' result[return_value] >> ', result['return_value'])


        args = { 'mismatch':[result["return_value"]]
                ,'messages':['執行失敗'] } 
    else:
        
        print('result -->',result)    
        args = { 'mismatch':[result["return_value"]], 
            'messages':['執行暫態完成']}  


    return    JsonResponse({'messages':args}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)  


def run_idv(request):

    username = request.GET.get('username')
    savfilelist = request.GET.getlist('savfilelist')
    idvpath = request.GET.get('idv_path')
    userdir = request.GET.get('user_dir')
    sourcedir = request.GET.get('source_dir')
    targetdir = request.GET.get('target_dir')

    message = []

    for savfile in savfilelist:


        args =  f" --Source_SavFileName {sourcedir}/{savfile}.sav"\
                f" --Target_SavFileName {targetdir}/{savfile}.sav"\
                f" --User_Folder {userdir}"\
                f" --User_name {username}"\
                f" --IDV_Path {idvpath}"
        

        cmd = fileprocess.run_pyfile_by_execmd(python_location='python'
                                    ,pyfile='pssefunctionsrc/src/runidv.py'
                                    ,args=args)
        print(cmd)
        result = fileprocess.execCmd(cmd)
        # print(result)
        if result['error']:
            message.append(f'{savfile} 失敗')
        else:
            message.append(f'{savfile} 成功')

    return    JsonResponse({'messages':['，'.join(message)]}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)    

def write_data_to_savfile(request):
    username = request.GET.get('username')
    savfilelist = request.GET.getlist('savfilelist')
    idvpath = request.GET.get('idv_path')
    userdir = request.GET.get('user_dir')
    sourcedir = request.GET.get('source_dir')
    targetdir = request.GET.get('target_dir')

    message = []
    for savfile in savfilelist:


        args =  f" --Source_SavFileName {sourcedir}/{savfile}.sav"\
                f" --Target_SavFileName {targetdir}/{savfile}.sav"\
                f" --User_Folder {userdir}"\
                f" --User_name {username}"\
                f" --IDV_Path {idvpath}"
        

        cmd = fileprocess.run_pyfile_by_execmd(python_location='python'
                                    ,pyfile='pssefunctionsrc/src/run_writingdata_to_sav.py'
                                    ,args=args)
        print(cmd)
        result = fileprocess.execCmd(cmd)
        # print(result)
        if result['error']:
            message.append(f'{savfile} 失敗')
        else:
            message.append(f'{savfile} 成功')
    print(message)
    return    JsonResponse({'results':['，'.join(message)]}, 
                                json_dumps_params={'ensure_ascii': False},
                                safe=False)




# @csrf_exempt
# @require_http_methods(["POST"])                                                                                
# def write_data_to_savfile(request):

#     params = request.POST.get('params', '{}')
#     params = json.loads(params) if params else {}
#     print("params --> ", params)


#     return_frontmessages, return_backendmessages    =  WriteData(params).area()
#     print("return_backendmessages --> ", return_backendmessages)
#     return JsonResponse({'results':[return_frontmessages, return_backendmessages]}, 
#                                 json_dumps_params={'ensure_ascii': False},
#                                 safe=False)


def download_savfile(request):
    savfiles = request.GET.getlist('savfiles')
    savfile_dir = request.GET.get('savfile_dir')
    download_dir = request.GET.get('download_dir')
    params = {
        'savfile_dir': savfile_dir,
        'download_dir': download_dir,
        'savfiles':savfiles
        }
    print('params = ', params)
    return MyDownload(request).download_savefile(params=params)

def download_powerflow(request):
    savfiles = request.GET.getlist('savfiles')
    download_what = request.GET.get('download_what')
    powerflow_dir = request.GET.get('powerflow_dir')
    powerflowsub_dir = request.GET.get('powerflowsub_dir')
    download_dir = request.GET.get('download_dir')

    params = {
        'savfiles':savfiles,
        'download_what': download_what,
        'powerflow_dir': powerflow_dir,
        'powerflowsub_dir':powerflowsub_dir,
        'download_dir':download_dir        
        }
    print('params = ', params)
    return MyDownload(request).download_powerflow(params=params)   


def download_errorcircuit(request):
    savfiles = request.GET.getlist('savfiles')
    download_what = request.GET.get('download_what')
    errorcircuit_dir = request.GET.get('errorcircuit_dir')
    download_dir = request.GET.get('download_dir')

    params = {
        'savfiles':savfiles,
        'download_what': download_what,
        'errorcircuit_dir': errorcircuit_dir,
        'download_dir':download_dir        
        }
    print('params = ', params)
    return MyDownload(request).download_errorcircuit(params=params)       

def download_dynamic(request):
    savfiles = request.GET.getlist('savfiles')
    download_what = request.GET.get('download_what')
    dynamic_dir = request.GET.get('dynamic_dir')
    download_dir = request.GET.get('download_dir')

    params = {
        'savfiles':savfiles,
        'download_what': download_what,
        'dynamic_dir': dynamic_dir,
        'download_dir':download_dir        
        }
    print('params = ', params)
    return MyDownload(request).download_dynamic(params=params)

def download_idvfile_for_create(request):
    download_what = request.GET.get('download_what')
    idvfile_dir = request.GET.get('idvfile_dir')
    download_dir = request.GET.get('download_dir')

    params = {
        'download_what': download_what,
        'idvfile_dir': idvfile_dir,
        'download_dir':download_dir        
        }
    print('params = ', params)
    return MyDownload(request).download_idvfile_for_create(params=params)