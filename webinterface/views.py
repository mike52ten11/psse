import os
import json
from icecream import ic
ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='debug > ')
# import coredumpy


# from webinterface.my_login import MyLogin
from webinterface.my_page import MyPage, DownloadPage
from webinterface.my_download import MyDownload
from webinterface.my_functions import MyFunctions
from webinterface.my_label_create import MyLabelCreate
from webinterface.delete import DeleteComponet
from webinterface.edit import EditComponet
from webinterface.src import fileprocess

# from webinterface.src.base.get_error import  error_handler

from .get_filter_data import  GetData

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from django.contrib import messages
from django.urls import reverse


from django.contrib import auth
from django.core.exceptions import ValidationError
#登入
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required
#密碼驗證
from django.contrib.auth.password_validation import validate_password

#忘記密碼
from django.contrib.auth.models import User


from django.http import StreamingHttpResponse
# from channels.generic.http import AsyncHttpConsumer
import asyncio
import threading
import traceback
import sys
from django.core.cache import cache


 

###
###===================================================
###                    首頁
###===================================================
### 


def home(request):

    return MyPage(request).home_page()

###
###===================================================
###                    上傳頁面
###===================================================
### 

def upload_page(request,*args):

    return MyPage(request,*args).upload_page()                                

    

def upload(request, *args):

    #先上傳sav檔
    args_of_upload = MyFunctions(request).upload(upload_what = 'savfile')

    sav_file = request.FILES.get("savfile",0)
    if not sav_file:
        return upload_page(request, {'messages':["沒有指定save 檔"]})    
    sav_file_name = str(sav_file)[0:4] 
    savfiles = [sav_file_name]   

    def background_task(user, savfiles):

        args = MyFunctions(request).filter(savfiles)

        # 使用 cache 存儲結果
        cache.set(f'upload_result_{user.username}', ['upload',args], 30)  # 30秒過期  



    if args_of_upload["error"]:
        # 上傳失敗
        cache.set(f'upload_result_{request.user.username}', ["error",f'{args_of_upload["return_value"]["backend_message"]}'], 600)  # 30秒過期        
        # args = {'messages':[args_of_upload["return_value"]["front_message"]]}
        messages.error(request, args_of_upload["return_value"]["front_message"])
        return redirect('upload_page')
    else:
        # 上傳成功，開始後台線程任務

        thread = threading.Thread(target=background_task, args=(request.user, savfiles,))
        thread.start()

        args={"messages":["上傳成功，正在製作filter檔案"]}
        cache.set(f'upload_result_{request.user.username}', ['正在執行...請稍後',"waiting"], 600)  # 30秒過期        
        messages.success(request, "上傳成功，正在製作filter檔案")

        # 返回執行頁面
        return redirect('upload_page')



def upload_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'upload_result_{request.user.username}')
    print('從 cache 讀取結果',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': '正在執行中，請稍候...'
            })
        elif result[0]  == 'upload':
            cache.delete(f'upload_result_{request.user.username}')
            return JsonResponse({
                'status': 'success',
                'message': result[1]
            })
        else:

            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })   




def delete_sav(request):

    return upload_page(request, MyFunctions(request).delete_sav())                 
###
###===================================================
###                    idv執行頁面
###===================================================
### 

def idv_execute_page(request, *args):

    return MyPage(request,*args).idv_execute_page()


###
###===================================================
###                    idv執行
###===================================================
### 




def idv_execute(request, *args):
    args = MyFunctions(request).upload(upload_what = 'idvfile')
    def background_task(user):
        try:
        # 執行任務
            args = MyFunctions(request).execute_idvfile()
            
        #     # 使用 cache 存儲結果
            cache.set(f'idv_execute_result_{user.username}', ['execute_idvfile'], 30)  # 30秒過期
        except Exception as err:

            cache.set(f'idv_execute_result_{request.user.username}', ['error'], 10)  # 10秒過期
            

    # 啟動後台線程
    thread = threading.Thread(target=background_task, args=(request.user,))
    thread.start()

    
    cache.set(f'idv_execute_result_{request.user.username}', ['正在執行...請稍後'], 30)  # 30秒過期
    # 返回執行頁面
    return idv_execute_page(request, args)

def idv_execute_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'idv_execute_result_{request.user.username}')
    print('從 cache 讀取結果',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result == ['正在執行...請稍後']:
            return JsonResponse({
                'status': 'processing',
                'message': '正在執行中，請稍候...'
            })
        elif result == ['execute_idvfile']:
            return JsonResponse({
                'status': 'success',
                'message': 'IDV檔案執行成功'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })

###
###===================================================
###                    powerflow 檔案上傳頁面
###===================================================
### 

def upload_page_of_upload_powerflow(request, *args):

    return MyPage(request,*args).upload_page_of_upload_powerflow()

    

def upload_powerflow(request, *args):
    

    def background_task(user, savfiles):

        try:
        # 執行任務
            args = MyFunctions(request).filter_powerflow(savfiles)
            print(args)
        #     # 使用 cache 存儲結果
            cache.set(f'upload_powerflow_result_{user.username}', ['upload_powerflow',args], 30)  # 30秒過期
        except Exception as err:
            cache.set(f'upload_powerflow_result_{request.user.username}', ['error',err], 10)  # 10秒過期
                 
        finally:
            # 標記任務已完成
            cache.set(f'upload_powerflow_completed_{user.username}', True, 1800)
            print(f"Background task for {user.username} completed")

    sav_file = request.FILES.get("savfile",0)
           
    if sav_file:
        sav_file_name = str(sav_file)[0:4]
        savfiles = [sav_file_name]
        args = MyFunctions(request).upload_powerflow(upload_what = 'savfile')
        
        cache.set(f'upload_powerflow_completed_{request.user.username}', False, 1800)
        # 啟動後台線程
        thread = threading.Thread(target=background_task, args=(request.user, savfiles,))
        thread.start()
        cache.set(f'upload_powerflow_result_{request.user.username}', ['正在執行...請稍後',"waiting"], 600)  # 30秒過期
        
        messages.success(request, '上傳成功，解析內容中')
        return redirect('upload_page_of_upload_powerflow')
    else:
        messages.error(request, '至少勾選一個sav 檔')
        return redirect('upload_page_of_upload_powerflow')
    # 返回執行頁面
    # return upload_page_of_upload_powerflow(request, args)



def upload_powerflow_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'upload_powerflow_result_{request.user.username}')
    task_completed = cache.get(f'upload_powerflow_result_{request.user.username}')
    print('從 cache 讀取結果',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': '上傳成功，正在製作filter檔案...'
            })
        elif result[0]  == 'upload_powerflow':
            if task_completed:
                # 可以在這裡清理緩存，表明結果已被讀取
                # cache.delete(f'dynamic_result_{request.user.username}')
                cache.delete(f'upload_powerflow_completed_{request.user.username}')

            return JsonResponse({
                'status': 'success',
                'message': result[1]
            })
        else:

            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })   


def delete_sav_powerflow(request):
    savfilelist = request.POST.getlist('year')
    if savfilelist==[]:
        messages.error(request, "請至少選擇一個檔案")
        return  redirect('upload_page_of_upload_powerflow')
    else:
        
        messages.success(request
                        , MyFunctions(request).delete_sav_powerflow(savfilelist)
                        )
        return redirect('upload_page_of_upload_powerflow')
###
###===================================================
###                    powerflow執行頁面
###===================================================
### 

def powerflow_page(request, *args):

    return MyPage(request,*args).powerflow_page()





def powerflow(request, *args):

    def background_task(user):
        # 執行任務
        try:
            args = MyFunctions(request).run_powerflow()
            
        #     # 使用 cache 存儲結果
            cache.set(f'powerflow_result_{user.username}', ['powerflow',args['powerflow_messages']['mismatch']], 30)  # 30秒過期
            cache.set(f'powerflowsub_result_{user.username}', ['powerflowsub',args['powerflow_sub_messages']['mismatch']], 30)  # 30秒過期       
            print('background_task = ',args)
        except Exception as err:

            cache.set(f'powerflow_result_{request.user.username}', ['error',err], 10)  # 10秒過期
            cache.set(f'powerflowsub_result_{request.user.username}', ['error',err], 10)  # 10秒過期
                       

        # try:
        # # 執行任務
        #     args = MyFunctions(request).run_powerflow()
            
        # #     # 使用 cache 存儲結果
        #     cache.set(f'idv_execute_result_{user.username}', ['powerflow',args], 30)  # 30秒過期
        # except Exception as err:

        #     cache.set(f'idv_execute_result_{request.user.username}', ['error',err], 10)  # 10秒過期
        
    N1_161KV = request.POST.get('N1_161KV')
    N1_345KV = request.POST.get('N1_345KV')
    N2_345KV = request.POST.get('N2_345KV')

    # args={}
    if request.POST.getlist('year')==[]:
        # args = {'messages':['至少勾選一個sav 檔']}
        messages.error(request, '至少勾選一個sav 檔')
        return redirect('powerflow_page')


    elif N1_161KV==None and N1_345KV==None and N2_345KV==None:
        # args = {'messages':['N0、N1、N2至少勾選一個']}
        messages.error(request, '161KV_N1、345KV_N1、345KV_N2至少勾選一個')
        return redirect('powerflow_page')        

    else:
        # 啟動後台線程
        thread = threading.Thread(target=background_task, args=(request.user,))
        thread.start()

        
        cache.set(f'powerflow_result_{request.user.username}', ['正在執行...請稍後','跑潮流中'], 1800)  # 30秒過期
        cache.set(f'powerflowsub_result_{request.user.username}', ['正在執行...請稍後','跑分岐中'], 1800)
        # 返回執行頁面
        # args = {"messages":['正在執行...請稍後']}

        messages.success(request, '正在執行...請稍後')
        return redirect('powerflow_page')

    # return powerflow_page(request, args)

def powerflow_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'powerflow_result_{request.user.username}')
    print(' 從 cache 讀取結果 powerflow',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': result[1]
            })
        elif result[0] == 'powerflow':
            
            return JsonResponse({
                'status': 'success',
                'message': '<br>'.join(result[1])
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })    


def powerflowsub_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'powerflowsub_result_{request.user.username}')
    print('從 cache 讀取結果 powerflowsub',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': result[1]
            })
        elif result[0] == 'powerflowsub':
            
            return JsonResponse({
                'status': 'success',
                'message': '<br>'.join(result[1])
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })      



###
###===================================================
###                    errorcircuit 檔案上傳頁面
###===================================================
### 

def upload_page_of_upload_errorcircuit(request, *args):

    return MyPage(request,*args).upload_page_of_upload_errorcircuit()

    

def upload_errorcircuit(request, *args):
    args = MyFunctions(request).upload_errorcircuit(upload_what = 'savfile')
    sav_file = request.FILES.get("savfile",0)
    sav_file_name = str(sav_file)[0:5] 
    savfiles = [sav_file_name]   
    def background_task(user, savfiles):

        args = MyFunctions(request).filter_errorcircuit(savfiles)
        
    #     # 使用 cache 存儲結果
        cache.set(f'upload_errorcircuit_result_{user.username}', ['upload_errorcircuit',args], 30)  # 30秒過期        

    if sav_file:
        # 啟動後台線程
        thread = threading.Thread(target=background_task, args=(request.user, savfiles,))
        thread.start()

    
        cache.set(f'upload_errorcircuit_result_{request.user.username}', ['正在執行...請稍後',"waiting"], 600)  # 30秒過期
    else:
        args = {'messages':["沒有指定save 檔"]}
    # 返回執行頁面
    return upload_page_of_upload_errorcircuit(request, args)



def upload_errorcircuit_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'upload_errorcircuit_result_{request.user.username}')
    print('從 cache 讀取結果',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': '正在執行中，請稍候...'
            })
        elif result[0]  == 'upload_errorcircuit':
            return JsonResponse({
                'status': 'success',
                'message': result[1]
            })
        else:

            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })   


def delete_sav_errorcircuit(request):

    return upload_page_of_upload_errorcircuit(request, MyFunctions(request).delete_sav_errorcircuit())        



###
###===================================================
###                    error circuit執行頁面
###===================================================
### 

def errorcircuit_page(request, *args):

    return MyPage(request,*args).errorcircuit_page()





def errorcircuit(request, *args):

    def background_task(user):

        # 執行任務
    #     args = MyFunctions(request).run_errorcircuit()
    #     print('args',args)
    # #     # 使用 cache 存儲結果
    #     cache.set(f'errorcircuit_result_{user.username}', ['errorcircuit',args['errorcircuit_messages']], 30)  # 30秒過期

        try:
            args = MyFunctions(request).run_errorcircuit()
            print('args',args)
        #     # 使用 cache 存儲結果
            cache.set(f'errorcircuit_result_{user.username}', ['errorcircuit',args['errorcircuit_messages']['mismatch']], 30)  # 30秒過期

        except Exception as err:

            cache.set(f'errorcircuit_result_{request.user.username}', ['error',err], 10)  # 10秒過期
        
    savefiles = request.POST.getlist('year')    

    #沒有勾選 -->return 到errorcircuit頁面          
    if savefiles==[]:
        messages.error(request, '至少勾選一個年份')
        # 重定向到 errorcircuit_page，使用 URL 名稱
        return redirect('errorcircuit_page')
        # return redirect('errorcircuit_page', {'messages':['至少勾選一個年份']})
    else:    
        # 啟動後台線程
        thread = threading.Thread(target=background_task, args=(request.user,))
        thread.start()

        
        cache.set(f'errorcircuit_result_{request.user.username}', ['正在執行...請稍後','跑故障電流中'], 1800)  # 30秒過期
        # 返回執行頁面
        args = {"messages":['正在執行...請稍後']}

        return errorcircuit_page(request, args)

def errorcircuit_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'errorcircuit_result_{request.user.username}')
    print(' 從 cache 讀取結果 errorcircuit',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': result[1]
            })
        elif result[0] == 'errorcircuit':
            
            return JsonResponse({
                'status': 'success',
                'message': '<br>'.join(result[1])
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })    



###
###===================================================
###                    暫態執行頁面
###===================================================
### 

def dynamic_page(request, *args):
   
    return MyPage(request,*args).dynamic_page()




def dynamic(request, *args):


    args = MyFunctions(request).upload(upload_what = 'dynamic')

    def background_task(user):
        # args = MyFunctions(request).run_dynamic()
        try:
            args = MyFunctions(request).run_dynamic()
            
        #     # 使用 cache 存儲結果
            cache.set(f'dynamic_result_{user.username}', ['dynamic',args['dynamic_messages']['mismatch']], 30)  # 30秒過期
            
            print('background_task = ',args)
        except Exception as err:

            cache.set(f'dynamic_result_{user.username}', ['error',err], 10)  # 10秒過期
        finally:
            # 標記任務已完成
            cache.set(f'dynamic_task_completed_{user.username}', True, 1800)
            print(f"Background task for {user.username} completed")        

    cache.set(f'dynamic_result_{request.user.username}', ['正在執行...請稍後','跑暫態中'], 1800)  # 30秒過期
    # 啟動後台線程
    thread = threading.Thread(target=background_task, daemon=True, args=(request.user,))
    thread.start()


    # 返回執行頁面
    args = {"messages":['正在執行...請稍後']}

    return dynamic_page(request, args)

def dynamic_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'dynamic_result_{request.user.username}')
    task_completed = cache.get(f'dynamic_task_completed_{request.user.username}')
    print(' 從 cache 讀取結果 dynamic',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': result[1]
            })
        elif result[0] == 'dynamic':
            if task_completed:
                # 可以在這裡清理緩存，表明結果已被讀取
                # cache.delete(f'dynamic_result_{request.user.username}')
                cache.delete(f'dynamic_task_completed_{request.user.username}')
                            
            return JsonResponse({
                'status': 'success',
                'message': '<br>'.join(result[1])
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })    
###
###===================================================
###                    每個頁籤的頁面
###===================================================
### 

def select_which_Label(request, selection_Label, *args):
    print('selection_Label --> ',selection_Label)
    if selection_Label=='TRANSFORMER3Winding_Winding':
       selection_Label =  'TRANSFORMER3Winding'
    # elif selection_Label=='twowingding':
    #    selection_Label =  'TRANSFORMER2Winding'   
    # else:
    #     pass
    return MyPage(request,*args).select_which_Label(selection_Label)

###
###===================================================
###                    寫入area暫存idv檔
###===================================================
### 
def write_to_savfile_for_area(request):
    
    return select_which_Label(request, 'area'
                                ,MyLabelCreate(request).write_areadata_to_savfiles())

###
###===================================================
###                    寫入zone暫存idv檔
###===================================================
### 
def write_to_savfile_for_zone(request):
    
    return select_which_Label(request, 'zone'
                                ,MyLabelCreate(request).write_zonedata_to_savfiles())

###
###===================================================
###                    寫入owner存idv檔
###===================================================
### 
def write_to_savfile_for_owner(request):
    
    return select_which_Label(request, 'owner'
                                ,MyLabelCreate(request).write_ownerdata_to_savfiles())

###
###===================================================
###                    寫入bus存idv檔
###===================================================
### 
def write_to_savfile_for_bus(request):
    
    return select_which_Label(request, 'bus'
                                ,MyLabelCreate(request).write_busdata_to_savfiles())  


###
###===================================================
###                    寫入machine存idv檔
###===================================================
### 
def write_to_savfile_for_machine(request):
    
    return select_which_Label(request, 'machine'
                                ,MyLabelCreate(request).write_machine_to_savfiles())  

###
###===================================================
###                    寫入load存idv檔
###===================================================
### 
def write_to_savfile_for_load(request):
    
    return select_which_Label(request, 'load'
                                ,MyLabelCreate(request).write_loaddata_to_savfiles())  

###
###===================================================
###                    寫入branch存idv檔
###===================================================
### 
def write_to_savfile_for_branch(request):
    
    return select_which_Label(request, 'branch'
                                ,MyLabelCreate(request).write_branchdata_to_savfiles())                                  

###
###===================================================
###                    寫入two winding存idv檔
###===================================================
### 
def write_to_savfile_for_twowinding(request):
    
    return select_which_Label(request, 'TRANSFORMER2Winding'
                                ,MyLabelCreate(request).write_twowinding_to_savfiles())

###
###===================================================
###                    寫入three winding 的transformer 存idv檔
###===================================================
### 
def write_to_savfile_for_threewinding(request):
    
    return select_which_Label(request, 'TRANSFORMER3Winding'
                                ,MyLabelCreate(request).write_threewinding_to_savfiles())
###
###===================================================
###                    寫入three winding 的winding存idv檔
###===================================================
### 
def write_to_savfile_for_threewinding_winding(request):
    
    return select_which_Label(request, 'TRANSFORMER3Winding'
                                ,MyLabelCreate(request).write_threewinding_winding_to_savfiles())
                                
###
###===================================================
###                    預覽寫入的內容 的頁面
###===================================================
### 
def prepare_writing_data_page(request, *args):

    return MyPage(request, *args).prepare_writing_data_page()
###
###===================================================
###    用執行idv的funcuction 將預覽的內容(暫存idv檔) 寫入sav檔
###===================================================
### 


def prepare_writing_data(request, *args):


    args = MyFunctions(request).upload(upload_what = 'writing_data')
    savfilelist = request.POST.getlist('year')

    def background_task(user, savfilelist):
        args = MyFunctions(request).write_idvfile_content_to_savfile(savfilelist)
        # args_filter = MyFunctions(request).filter(savfilelist)
        # args_filter = MyFunctions(request).filter(sav_file_name=savfilelist)
    #     # 使用 cache 存儲結果
        cache.set(f'writedata_result_{user.username}', ['writedata',args], 30)  # 30秒過期
        print('background_task = ',args)
        
        
        # 執行任務
        # try:
        #     args = MyFunctions(request).write_idvfile_content_to_savfile()
            
        # #     # 使用 cache 存儲結果
        #     cache.set(f'writedata_result_{user.username}', ['writedata',args['messages']], 30)  # 30秒過期
            
        #     print('background_task = ',args)
        # except Exception as err:

        #     cache.set(f'writedata_result_{request.user.username}', ['error',err], 10)  # 10秒過期
         


    # 啟動後台線程
    thread = threading.Thread(target=background_task, args=(request.user,savfilelist,))
    thread.start()

    
    cache.set(f'writedata_result_{request.user.username}', ['正在執行...請稍後','寫入中'], 1800)  # 30秒過期
    # 返回執行頁面
    # messages.info(request, '正在執行...請稍後')

    # 重定向到頁面
    return redirect('prepare_writing_data_page')    
    # args = {"messages":['正在執行...請稍後']}

    # return prepare_writing_data_page(request, args)

def prepare_writing_data_status(request):
    # 從 cache 讀取結果
    result = cache.get(f'writedata_result_{request.user.username}')
    print(' 從 cache 讀取結果 writedata',result)
    if result:
        # 根據不同的執行結果返回不同的狀態
        if result[0] == '正在執行...請稍後':
            return JsonResponse({
                'status': 'processing',
                'message': result[1]
            })
        elif result[0] == 'writedata':
            # os.remove(result[1]['temp_idvpath'])
            return JsonResponse({
                'status': 'success',
                'message': '<br>'.join(result[1]["messages"])
            })
        else:
            
            return JsonResponse({
                'status': 'error',
                'message': f'執行發生錯誤：{result[1]["messages"]}'
            })
    
    return JsonResponse({
        'status': 'wait', 
        'message': '等待執行...'
    })      
###
###===================================================
###                    下載 頁面
###===================================================
### 

def download_page(request):

    pag = MyPage(request)
    return pag.DownloadPage(pag.request).download_page()


def download_savefile_page(request,*args):

    return DownloadPage(request,*args).download_savefile_page()

def download_savefile_of_powerflow_page(request,*args):

    return DownloadPage(request,*args).download_savefile_of_powerflow_page()

def download_savefile_of_errorcircuit_page(request,*args):

    return DownloadPage(request,*args).download_savefile_of_errorcircuit_page()    


def download_powerflow_page(request,*args):

    
    return DownloadPage(request,*args).download_powerflow_page()


def download_errorcircuit_page(request,*args):
    
    return DownloadPage(request,*args).download_errorcircuit_page()


def download_dynamic_page(request,*args):

    return DownloadPage(request,*args).download_dynamic_page()


def download_idvfile_page(request,*args):
    pag = MyPage(request)
    return pag.DownloadPage(pag.request,*args).download_idvfile_page()



def download_idvfile_for_create_page(request,*args):

    return DownloadPage(request,*args).download_idvfile_for_create_page()
###
###===================================================
###                    下載檔案
###===================================================
###

def download_savefile(request):
    if request.POST.getlist('year')==[]:

        return download_savefile_page(request, {'messages':['至少勾選一個年份']}) 

    download_ok = MyDownload(request).download_savefile()
    print('file_path --> ',download_ok)
    zipfile_path = download_ok['zipfile_path']
    
    with open(zipfile_path, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    if 'download_savefile_buttom' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=Savfiles.zip'
        return response
    else:
        return download_savefile_page(request,{'messages':['下載失敗']})           

def download_savefile_of_powerflow(request):
    if request.POST.getlist('year')==[]:

        return download_savefile_of_powerflow_page(request, {'messages':['至少勾選一個年份']}) 

    download_ok = MyDownload(request).download_savefile_of_powerflow()
    print('file_path --> ',download_ok)
    zipfile_path = download_ok['zipfile_path']
    
    with open(zipfile_path, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    if 'download_savefile_of_powerflow_buttom' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=Savfiles_of_powerflow.zip'
        return response
    else:
        return download_savefile_page(request,{'messages':['下載失敗']})   

def download_savefile_of_errorcircuit(request):
    if request.POST.getlist('year')==[]:

        return download_savefile_of_errorcircuit_page(request, {'messages':['至少勾選一個年份']}) 

    download_ok = MyDownload(request).download_savefile_of_errorcircuit()
    print('file_path --> ',download_ok)
    zipfile_path = download_ok['zipfile_path']
    
    with open(zipfile_path, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    if 'download_savefile_of_errorcircuit_buttom' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=Savfiles_of_errorcircuit.zip'
        return response
    else:
        return download_savefile_page(request,{'messages':['下載失敗']})         

def download_powerflow(request): 
    if request.POST.getlist('year')==[]:

        return download_powerflow_page(request, {'messages':['至少勾選一個年份']}) 

    download_ok = MyDownload(request).download_powerflow()
    print('file_path --> ',download_ok)
    zipfile_path = download_ok['zipfile_path']
    
    with open(zipfile_path, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    if 'download_powerflow' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=PowerFlow.zip'
        return response
    elif 'download_powerflow_log' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=PowerFlow_log.zip'
        return response
    else:
        return download_powerflow_page(request,{'messages':['下載失敗']})
                            
    


def download_errorcircuit(request): 
    if request.POST.getlist('year')==[]:

        return download_errorcircuit_page(request, {'messages':['至少勾選一個年份']}) 

    download_ok = MyDownload(request).download_errorcircuit()
    print('file_path --> ',download_ok)
    zipfile_path = download_ok['zipfile_path']
    
    with open(zipfile_path, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    if 'download_errorcircuit' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=FaultCurrent.zip'
        return response
    elif 'download_errorcircuit_log' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=FaultCurrent_log.zip'
        return response
    else:
        return download_errorcircuit_page(request,{'messages':['下載失敗']})


def download_dynamic(request): 
    if request.POST.getlist('year')==[]:

        return download_dynamic_page(request, {'messages':['至少勾選一個年份']}) 

    download_ok = MyDownload(request).download_dynamic()
    print('file_path --> ',download_ok)
    zipfile_path = download_ok['zipfile_path']
    
    with open(zipfile_path, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    if 'download_dynamic' in request.POST:
        response['Content-Disposition'] = 'attachment; filename=Dynamic.zip'
        return response
    else:
        return download_errorcircuit_page(request,{'messages':['下載失敗']})

    # print(args)
    # if args["error"]:
    #     return download_dynamic_page(request, {'messages':[f'下載失敗\\n錯誤訊息:{args["error_messages"]}']})       
    # else:
    #     with open(args["file_path"], 'rb') as model_excel:
    #         result = model_excel.read()
    #     response = HttpResponse(result)
    #     response['Content-Disposition'] = 'attachment; filename=Dynamic.zip'

    #     # fileprocess.remove_file(args["file_path"])

    #     return response 


def download_idvfile_for_create(request): 

    args = MyDownload(request).download_idvfile_for_create()
    print(args)
    if args["error"]:
        return download_idvfile_for_create_page(request, {'messages':[f'下載失敗\\n錯誤訊息:{args["error_messages"]}']})       
    else:
        with open(args["file_path"], 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        response['Content-Disposition'] = 'attachment; filename=IDV_for_Create.zip'

        # fileprocess.remove_file(args["file_path"])

        return response         
    # try:
    #     return MyDownload(request).download_savefile()

    # except  Exception as e:
    #     print(e)
    #     # logger.error('USER: %s ACTION: %s MESSAGE: %s',
    #     #     request.user,   '按下下載電力潮流檔案按鈕', str(e)) 

    #     args = {    'mismatch':'下載失敗',
    #                 'messages':['下載失敗']}     

    #     return download_savefile_page(request,args)      
###
###===================================================
###                    取得filter npz資料的API
###===================================================
### 


def api_for_get_bus_data_of_dynamic(request):

    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')

    return GetData(f"../Data/User/{user}/filter/Powerflow/bus/{year}.npz").bus_data_for_api(f"../Data/User/{user}/filter/Powerflow/bus")

def api_for_get_bus_data(request):
    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/bus/{year}.npz").bus_data_for_api(f"../Data/User/{user}/filter/bus")    

def api_for_get_threewinding_data(request):
    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    fom_to_last_bus = request.GET.get('fom_to_last_bus')
    args = {
        'labeltype': labeltype,
        'fom_to_last_bus': fom_to_last_bus,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/three_winding_transformer/{year}.npz").three_winding_transformer_data_for_api(f"../Data/User/{user}/filter/three_winding_transformer")

def api_for_get_twowinding_data(request):
    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    fom_to_last_bus = request.GET.get('fom_to_last_bus')
    args = {
        'labeltype': labeltype,
        'fom_to_last_bus': fom_to_last_bus,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print('args-->',args)
    return GetData(f"../Data/User/{user}/filter/two_winding_transformer/{year}.npz").two_winding_transformer_data_for_api(f"../Data/User/{user}/filter/two_winding_transformer")


def api_for_get_machine_data(request):
    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    
    args = {
        'labeltype': labeltype,        
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/machine/{year}.npz").machine_data_for_api(f"../Data/User/{user}/filter/machine")    


def api_for_get_machine_bus_data_of_dynamic(request):
    year = request.GET.get('year')
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    print(year)
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter/Powerflow",
    }
    return GetData(f'../Data/User/{user}/filter/Powerflow/machine/{year}.npz').machine_data_for_api_of_dynamic(f'../Data/User/{user}/filter/Powerflow/machine')



def api_for_get_trip_line_data_of_dynamic(request):

    year = request.GET.get('year')
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    busfaultnum = request.GET.get('busfaultnum')
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter/Powerflow",
        'busfaultnum': busfaultnum
    }
    return GetData(f"../Data/User/{user}/filter/Powerflow/tripline/{year}.npz").trip_line_data_for_api(busfaultnum)


def api_for_get_zone_data(request):

    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/zone/{year}.npz").zone_data_for_api(f"../Data/User/{user}/filter/zone")    

def api_for_get_area_data(request):

    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/area/{year}.npz").area_data_for_api(f"../Data/User/{user}/filter/area")     

def api_for_get_owner_data(request):

    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/owner/{year}.npz").owner_data_for_api(f"../Data/User/{user}/filter/owner")    

def api_for_get_load_data(request):

    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/load/{year}.npz").load_data_for_api(f"../Data/User/{user}/filter/load")

def api_for_get_branch_data(request):

    year = request.GET.get('year',None)
    
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')
    fom_to_last_bus = request.GET.get('fom_to_last_bus')
    args = {
        'labeltype': labeltype,
        'fom_to_last_bus': fom_to_last_bus,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter",
        'savfiledir': f"../Data/User/{user}/SavFile",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter"
    }      
    print(args)
    return GetData(f"../Data/User/{user}/filter/branch/{year}.npz").branch_data_for_api(f"../Data/User/{user}/filter/branch")


###
###===================================================
###                    預覽頁面 的 刪除和編輯
###===================================================
###

##===================================================
##                    area
###===================================================
###
def delete_area(request, row):
    user = request.user
   
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/area.idv"
                , showdata_path=f"temp/{user}/writedata/show/area.idv"
                , row=row).area()

def edit_area(request, row):
    user = request.user
    data = json.loads(request.body)
    area_number = data.get('area_number')
    area_name = data.get('area_name')


      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/area.idv"
                , showdata_path=f"temp/{user}/writedata/show/area.idv"
                , row=row
                , edit_data_for_write = f"BAT_AREA_DATA,{area_number}, , , ,'{area_name}'\n"
                , edit_data_for_show = f"{area_number},'{area_name}'\n").area()


##===================================================
##                    zone
###===================================================
###
def delete_zone(request, row):
    user = request.user
   
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/zone.idv"
                , showdata_path=f"temp/{user}/writedata/show/zone.idv"
                , row=row).zone()

def edit_zone(request, row):
    user = request.user
    data = json.loads(request.body)
    zone_number = data.get('zone_number')
    zone_name = data.get('zone_name')


      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/zone.idv"
                , showdata_path=f"temp/{user}/writedata/show/zone.idv"
                , row=row
                , edit_data_for_write = f"BAT_ZONE_DATA,{zone_number},'{zone_name}'\n"
                , edit_data_for_show = f"{zone_number},'{zone_name}'\n").zone()



##===================================================
##                    owner
###===================================================
###
def delete_owner(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/owner.idv"
                , showdata_path=f"temp/{user}/writedata/show/owner.idv"
                , row=row).owner()

def edit_owner(request, row):
    user = request.user
    data = json.loads(request.body)
    owner_number = data.get('owner_number')
    owner_name = data.get('owner_name')


      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/owner.idv"
                , showdata_path=f"temp/{user}/writedata/show/owner.idv"
                , row=row
                , edit_data_for_write = f"BAT_OWNER_DATA,{owner_number},'{owner_name}'\n"
                , edit_data_for_show = f"{owner_number},'{owner_name}'\n").owner()

##===================================================
##                    bus
###===================================================
###
def delete_bus(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/bus.idv"
                , showdata_path=f"temp/{user}/writedata/show/bus.idv"
                , row=row).bus()

def edit_bus(request, row):
    user = request.user
    data = json.loads(request.body)
    busNumber = data.get('busNumber')
    busName = data.get('busName')
    code = data.get('code')
    areaNumber = data.get('areaNumber')
    zoneNumber = data.get('zoneNumber')
    ownerNumber = data.get('ownerNumber')
    baseKv = data.get('baseKv')
    voltage = data.get('voltage')
    angleDeg = data.get('angleDeg')
    normalVmax = data.get('normalVmax')
    normalVmin = data.get('normalVmin')
    emergencyVmax = data.get('emergencyVmax')
    emergencyVmin = data.get('emergencyVmin')

    # bus_data = f"BAT_BUS_DATA,{busNumber},'{busName}',{code},{areaNumber},{zoneNumber},'{ownerName}',{baseKv},{voltage},{angleDeg},{normalVmax},{normalVmin},{emergencyVmax},{emergencyVmin}\n"

    return    EditComponet(writedata_path=f"temp/{user}/writedata/bus.idv"
                , showdata_path=f"temp/{user}/writedata/show/bus.idv"
                , row=row
                , edit_data_for_write = f"BAT_BUS_DATA_4,{busNumber},0,{code},{areaNumber},{zoneNumber},{ownerNumber},{baseKv},{voltage},{angleDeg},{normalVmax},{normalVmin},{emergencyVmax},{emergencyVmin},'{busName}'\n"
                , edit_data_for_show = f"{busNumber},'{busName}',{code},{areaNumber},{zoneNumber},'{ownerNumber}',{baseKv},{voltage},{angleDeg},{normalVmax},{normalVmin},{emergencyVmax},{emergencyVmin}\n"
                ).bus()


##===================================================
##                    machine
###===================================================
###
def delete_machine(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/machine.idv"
                , showdata_path=f"temp/{user}/writedata/show/machine.idv"
                , row=row).machine()

def edit_machine(request, row):
    user = request.user
    data = json.loads(request.body)
    BUS_Number = data.get('busNumber')
    ID = data.get('id')
    MachineControlMode = data.get('machineControlMode')
    BASE = data.get('base')
    Pgen = data.get('pgen')
    Qgen = data.get('qgen')
    Qmax = data.get('qmax')
    Qmin = data.get('qmin')
    Pmax = data.get('pmax')
    Pmin = data.get('pmin')
    Mbase = data.get('mbase')
    RSource = data.get('rSource')
    XSource = data.get('xSource')
    R = data.get('r')
    SubtransientX = data.get('subtransientX')
    RNegative = data.get('rNegative')
    XNegative = data.get('xNegative')
    RZero = data.get('rZero')
    XZero = data.get('xZero')
    TransientX = data.get('transientX')
    SynchronousX = data.get('synchronousX')
    print('RSource-->',RSource)
    print('XSource -->',XSource)
    edit_data_for_write = f'BAT_PLANT_DATA,{BUS_Number},0,0,0,1.00,100.00\n'\
                        f'BAT_MACHINE_DATA_3,{BUS_Number},{ID},0,1,0,0,0,{MachineControlMode},{BASE},{Pgen},{Qgen},{Qmax},{Qmin},{Pmax},{Pmin},{Mbase},{RSource},{XSource},,,,,,,,,\n'\
                        f'BAT_NEWSEQ,;\n'\
                        f'BAT_SEQ_MACHINE_DATA_3,{BUS_Number},{ID},0,{R},{SubtransientX},{RNegative},{XNegative},{RZero},{XZero},{TransientX},{SynchronousX},0.0,0.0,0.0\n'
    print(edit_data_for_write)
    return    EditComponet(writedata_path=f"temp/{user}/writedata/machine.idv"
                , showdata_path=f"temp/{user}/writedata/show/machine.idv"
                , row=row
                , edit_data_for_write = edit_data_for_write
                , edit_data_for_show = f"{BUS_Number},{ID},{MachineControlMode},{BASE},{Pgen},{Qgen},{Qmax},{Qmin},{Pmax},{Pmin},{Mbase},{RSource},{XSource}"\
                                            f",{R},{SubtransientX},{RNegative},{SubtransientX},{XNegative},{RZero},{XZero},{TransientX},{SynchronousX}\n").machine()

##===================================================
##                    load
###===================================================

def delete_load(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/load.idv"
                , showdata_path=f"temp/{user}/writedata/show/load.idv"
                , row=row).load()

def edit_load(request, row):
    user = request.user
    data = json.loads(request.body)
    bus_number = data.get('busNumber')
    pload = data.get('pload')
    qload = data.get('qload')

      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/load.idv"
                , showdata_path=f"temp/{user}/writedata/show/load.idv"
                , row=row
                , edit_data_for_write = f"BAT_LOAD_DATA_6,{bus_number}, , , , , , , , ,{pload},{qload}, , , , , ,;\n"
                , edit_data_for_show = f"{bus_number},{pload},{qload}\n").load()

##===================================================
##                    branch
###===================================================

def delete_branch(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/branch.idv"
                , showdata_path=f"temp/{user}/writedata/show/branch.idv"
                , row=row).branch()

def edit_branch(request, row):
    user = request.user
    data = json.loads(request.body)

    FromBusNumber = data.get('fromBusNumber')
    ToBusNumber = data.get('toBusNumber')
    ID = data.get('id')
    LineR = data.get('lineR')
    LineX = data.get('lineX')
    ChargingB = data.get('chargingB')
    Length= data.get('length')
    RATE1 = data.get('rate1')
    NAME = data.get('name')
    R_Zero = data.get('rZero')
    X_Zero = data.get('xZero')
    B_Zero = data.get('bZero')

    edit_data_for_write = f"BAT_BRANCH_DATA_3,{FromBusNumber},{ToBusNumber},{ID}, , , , , , ,{LineR},{LineX},{ChargingB}, , , , ,{LineX}, , , , ,{RATE1}, , , , , , , , , , ,{NAME};\n"\
                            f"BAT_NEWSEQ,;\n"\
                            f"BAT_SEQ_BRANCH_DATA_3,{FromBusNumber},{ToBusNumber},{ID}, ,{R_Zero},{X_Zero},{B_Zero}, , , ;\n"

      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/branch.idv"
                , showdata_path=f"temp/{user}/writedata/show/branch.idv"
                , row=row
                , edit_data_for_write = edit_data_for_write
                , edit_data_for_show = f"{FromBusNumber},{ToBusNumber},{ID},{LineR},{LineX},{ChargingB},{RATE1},{R_Zero},{X_Zero},{B_Zero},{Length},{NAME}\n"
                ).branch()

##===================================================
##                    twowinding
###===================================================

def delete_twowinding(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/twowinding.idv"
                , showdata_path=f"temp/{user}/writedata/show/twowinding.idv"
                , row=row).branch()

def edit_twowinding(request, row):
    user = request.user

    data = json.loads(request.body)

    FromBusNumber = data.get('fromBusNumber')
    ToBusNumber = data.get('toBusNumber')
    ID = data.get('id')
    ControlledBus = data.get('controlledBus')
    Winding_int = data.get('windingIOCode')
    Impedance = data.get('impedanceIOCode')
    Admittance = data.get('admittanceIOCode')
    SpecifiedR = data.get('specifiedRPuOrWatts')
    SpecifiedX = data.get('specifiedXPu')
    Winding = data.get('winding')
    Wind1 = data.get('wind1')
    Wind2Ratio = data.get('wind2Ratio')
    Wind2 = data.get('wind2')
    RATE1 = data.get('rate1Mva')
    Name = data.get('name')
    if Name != '':
        Name = f"'{Name}'"
    Connection = data.get('connectionCode')
    R01 = data.get('r01Pu')
    X01 = data.get('x01Pu')


    edit_data_for_write = f"BAT_TWO_WINDING_DATA_6,{FromBusNumber},{ToBusNumber},{ID}, , , , , , , , ,{ControlledBus}, , , , ,{Winding_int},{Impedance},{Admittance},{SpecifiedR},,{SpecifiedX},{Winding},,{Wind1},{Wind2Ratio},{Wind2}, , , , , , , , , , , , , ,{RATE1}, , , , , , , , , , , , ,{Name}\n"\
                            f"BAT_NEWSEQ,;\n"\
                            f"BAT_SEQ_TWO_WINDING_DATA_3,{FromBusNumber},{ToBusNumber},{ID},{Connection}, , , , ,{R01},{X01}, , , , , ,;\n"

      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/twowinding.idv"
                , showdata_path=f"temp/{user}/writedata/show/twowinding.idv"
                , row=row
                , edit_data_for_write = edit_data_for_write
                , edit_data_for_show = f"{FromBusNumber},{ToBusNumber},{ID},{ControlledBus},{Winding_int},{Impedance},{Admittance},{SpecifiedR},{SpecifiedX},{Winding},{Wind1},{Wind2Ratio},{Wind2},{RATE1},{Name},{Connection},{R01},{X01}\n"
                ).twowinding()                                  

##===================================================
##                    threewinding
###===================================================

def delete_threewinding(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/threewinding.idv"
                , showdata_path=f"temp/{user}/writedata/show/threewinding.idv"
                , row=row).threewinding()

def edit_threewinding(request, row):
    user = request.user

    data = json.loads(request.body)
    FromBusNumber = data.get('fromBusNumber')
    ToBusNumber = data.get('toBusNumber')
    LastBusNumber = data.get('lastBusNumber')
    ID = data.get('id')
    Name = data.get('name')
    if Name != '':
        Name = f"'{Name}'"    
    Winding = data.get('windingIOCode')
    Impedance = data.get('impedanceIOCode')
    Admittance = data.get('admittanceIOCode')
    W12R = data.get('w12rPuOrWatts')
    W12X = data.get('w12xPu')
    W23R = data.get('w23rPuOrWatts')
    W23X = data.get('w23xPu')
    W31R = data.get('w31rPuOrWatts')
    W31X = data.get('w31xPu')
    Winding12MVABase = data.get('winding12MvaBase')
    Winding23MVABase = data.get('winding23MvaBase')
    Winding31MVABase = data.get('winding31MvaBase')
    ImpaedanceAdjustmentCode = data.get('impaedanceAdjustmentCode')
    connection = data.get('connection')
    R01 = data.get('r01Pu')
    X01 = data.get('x01Pu')
    R02 = data.get('r02Pu')
    X02 = data.get('x02Pu')
    R03 = data.get('r03Pu')
    X03 = data.get('x03Pu')



    edit_data_for_write =f"BAT_THREE_WND_IMPED_DATA_4,{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},,,,,{Winding},{Impedance},{Admittance},,,,,,{ImpaedanceAdjustmentCode},{W12R},{W12X},{W23R},{W23X},{W31R},{W31X},{Winding12MVABase},{Winding23MVABase},{Winding31MVABase},,,,,,,,,{Name},\n"\
                            f"BAT_NEWSEQ,;\n"\
                           f"BAT_SEQ_THREE_WINDING_DATA_3,{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},,,{connection},,,{R01},{X01},,,{R02},{X02},,,{R03},{X03},,;\n"

      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/threewinding.idv"
                , showdata_path=f"temp/{user}/writedata/show/threewinding.idv"
                , row=row
                , edit_data_for_write = edit_data_for_write
                , edit_data_for_show = f"{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},{Name},{Winding},{Impedance},{Admittance},{W12R},{W12X},{W23R},{W23X},{W31R},{W31X},{Winding12MVABase},{Winding23MVABase},{Winding31MVABase},{ImpaedanceAdjustmentCode},{connection},{R01},{X01},{R02},{X02},{R03},{X03}\n"
                ).threewinding()  


##===================================================
##                    threewinding_winding
###===================================================

def delete_threewinding_winding(request, row):

    user = request.user
    return      DeleteComponet(writedata_path=f"temp/{user}/writedata/threewinding_winding.idv"
                , showdata_path=f"temp/{user}/writedata/show/threewinding_winding.idv"
                , row=row).threewinding_winding()

def edit_threewinding_winding(request, row):
    user = request.user

    data = json.loads(request.body)
    FromBusNumber = data.get('fromBusNumber')
    ToBusNumber = data.get('toBusNumber')
    LastBusNumber = data.get('lastBusNumber')
    ID = data.get('id')
    Name = data.get('name')
    if Name != '':
        Name = f"'{Name}'"    
    Winding = data.get('windingIOCode')
    Impedance = data.get('impedanceIOCode')
    Admittance = data.get('admittanceIOCode')
    W12R = data.get('w12rPuOrWatts')
    W12X = data.get('w12xPu')
    W23R = data.get('w23rPuOrWatts')
    W23X = data.get('w23xPu')
    W31R = data.get('w31rPuOrWatts')
    W31X = data.get('w31xPu')
    Winding12MVABase = data.get('winding12MvaBase')
    Winding23MVABase = data.get('winding23MvaBase')
    Winding31MVABase = data.get('winding31MvaBase')
    ImpaedanceAdjustmentCode = data.get('impaedanceAdjustmentCode')
    connection = data.get('connection')
    R01 = data.get('r01Pu')
    X01 = data.get('x01Pu')
    R02 = data.get('r02Pu')
    X02 = data.get('x02Pu')
    R03 = data.get('r03Pu')
    X03 = data.get('x03Pu')



    edit_data_for_write =f"BAT_THREE_WND_IMPED_DATA_4,{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},,,,,{Winding},{Impedance},{Admittance},,,,,,{ImpaedanceAdjustmentCode},{W12R},{W12X},{W23R},{W23X},{W31R},{W31X},{Winding12MVABase},{Winding23MVABase},{Winding31MVABase},,,,,,,,,{Name},\n"\
                            f"BAT_NEWSEQ,;\n"\
                           f"BAT_SEQ_THREE_WINDING_DATA_3,{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},,,{connection},,,{R01},{X01},,,{R02},{X02},,,{R03},{X03},,;\n"

      
    return    EditComponet(writedata_path=f"temp/{user}/writedata/threewinding_winding.idv"
                , showdata_path=f"temp/{user}/writedata/show/threewinding_winding.idv"
                , row=row
                , edit_data_for_write = edit_data_for_write
                , edit_data_for_show = f"{FromBusNumber},{ToBusNumber},{LastBusNumber},{ID},{Name},{Winding},{Impedance},{Admittance},{W12R},{W12X},{W23R},{W23X},{W31R},{W31X},{Winding12MVABase},{Winding23MVABase},{Winding31MVABase},{ImpaedanceAdjustmentCode},{connection},{R01},{X01},{R02},{X02},{R03},{X03}\n"
                ).threewinding_winding()                 