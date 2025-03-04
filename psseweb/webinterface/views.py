import os




from webinterface.my_login import MyLogin
from webinterface.my_page import MyPage, DownloadPage
from webinterface.my_download import MyDownload
from webinterface.my_functions import MyFunctions
from webinterface.my_label_create import MyLabelCreate
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


 


###===========|----------------------------------|==================================================
###===========|         登入相關的Function        |==================================================
###===========|----------------------------------|==================================================


###
###===================================================
###                    註冊
###===================================================
###  
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login_page')
    template_name = 'sign_up.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '註冊成功！請登錄。')
        return response

      
###
###===================================================
###                    登入頁面
###===================================================
### 
def login_page(request):

    return MyLogin(request).login_page()


###
###===================================================
###                    處理登入頁面的按鈕
###===================================================
### 
def login(request):

    return MyLogin(request).mylogin()

###
###===================================================
###                    登出
###===================================================
### 
@login_required
def logout(request):
    return MyLogin(request).mylogout()

###
###===================================================
###                    忘記密碼
###===================================================
### 

def forget_password(request):
    return MyLogin(request).forget()

###===================================================================================
###===================================================================================
###===================================================================================





###
###===================================================
###                    首頁
###===================================================
### 

@login_required
def home(request):
    # args = MyFunctions(request).filter('115P')
    return MyPage(request).home_page()

###
###===================================================
###                    上傳頁面
###===================================================
### 
@login_required
def upload_page(request,*args):

    return MyPage(request,*args).upload_page()                                

    
@login_required
def upload(request, *args):
    args_of_upload = MyFunctions(request).upload(upload_what = 'savfile')


    sav_file = request.FILES.get("savfile",0)
    if not sav_file:
        return upload_page(request, {'messages':["沒有指定save 檔"]})    
    sav_file_name = str(sav_file)[0:4] 
    savfiles = [sav_file_name]   

    def background_task(user, savfiles):
        # args = MyFunctions(request).filter()
        # cache.set(f'upload_result_{request.user.username}', ['error'], 10)  # 10秒過期

        args = MyFunctions(request).filter(savfiles)
        # args={"messages":"成功"}
    #     # 使用 cache 存儲結果
        cache.set(f'upload_result_{user.username}', ['upload',args], 30)  # 30秒過期        
        # try:
        # # 執行任務
        #     args = MyFunctions(request).filter(savfiles)
            
        # #     # 使用 cache 存儲結果
        #     cache.set(f'upload_result_{user.username}', ['upload',args], 30)  # 30秒過期
        # except Exception as err:

        #     cache.set(f'upload_result_{request.user.username}', ['error',err], 10)  # 10秒過期
      
    if not args_of_upload["error"]:
        # 啟動後台線程
        thread = threading.Thread(target=background_task, args=(request.user, savfiles,))
        thread.start()

        args={"messages":["上傳成功，正在製作filter檔案"]}
        cache.set(f'upload_result_{request.user.username}', ['正在執行...請稍後',"waiting"], 600)  # 30秒過期
    else:
        
        print('args_of_upload-->',args_of_upload)
        cache.set(f'upload_result_{request.user.username}', ["error",f'{args_of_upload["return_value"]["backend_message"]}'], 600)  # 30秒過期        
        args = {'messages':[args_of_upload["return_value"]["front_message"]]}
    # 返回執行頁面
    return upload_page(request, args)



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



@login_required
def delete_sav(request):

    return upload_page(request, MyFunctions(request).delete_sav())                 
###
###===================================================
###                    idv執行頁面
###===================================================
### 
@login_required
def idv_execute_page(request, *args):

    return MyPage(request,*args).idv_execute_page()


###
###===================================================
###                    idv執行
###===================================================
### 



@login_required
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
@login_required
def upload_page_of_upload_powerflow(request, *args):

    return MyPage(request,*args).upload_page_of_upload_powerflow()

    
@login_required
def upload_powerflow(request, *args):
    args = MyFunctions(request).upload_powerflow(upload_what = 'savfile')
    sav_file = request.FILES.get("savfile",0)
    sav_file_name = str(sav_file)[0:4] 
    savfiles = [sav_file_name]   
    def background_task(user, savfiles):
        # args = MyFunctions(request).filter()
        # cache.set(f'upload_result_{request.user.username}', ['error'], 10)  # 10秒過期
    #     args = MyFunctions(request).filter_powerflow(savfiles)
        
    # #     # 使用 cache 存儲結果
    #     cache.set(f'upload_powerflow_result_{user.username}', ['upload_powerflow',args], 30)  # 30秒過期
  
        try:
        # 執行任務
            args = MyFunctions(request).filter_powerflow(savfiles)
            
        #     # 使用 cache 存儲結果
            cache.set(f'upload_powerflow_result_{user.username}', ['upload_powerflow',args], 30)  # 30秒過期
        except Exception as err:
            cache.set(f'upload_powerflow_result_{request.user.username}', ['error',err], 10)  # 10秒過期
                 
        finally:
            # 標記任務已完成
            cache.set(f'upload_powerflow_completed_{user.username}', True, 1800)
            print(f"Background task for {user.username} completed")   
       
    if sav_file:
        cache.set(f'upload_powerflow_completed_{request.user.username}', False, 1800)
        # 啟動後台線程
        thread = threading.Thread(target=background_task, args=(request.user, savfiles,))
        thread.start()

    
        cache.set(f'upload_powerflow_result_{request.user.username}', ['正在執行...請稍後',"waiting"], 600)  # 30秒過期
    else:
        args = {'messages':["沒有指定save 檔"]}
    # 返回執行頁面
    return upload_page_of_upload_powerflow(request, args)



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

@login_required
def delete_sav_powerflow(request):

    return upload_page_of_upload_powerflow(request, MyFunctions(request).delete_sav_powerflow())        

###
###===================================================
###                    powerflow執行頁面
###===================================================
### 
@login_required
def powerflow_page(request, *args):

    return MyPage(request,*args).powerflow_page()




@login_required
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
            

    # 啟動後台線程
    thread = threading.Thread(target=background_task, args=(request.user,))
    thread.start()

    
    cache.set(f'powerflow_result_{request.user.username}', ['正在執行...請稍後','跑潮流中'], 1800)  # 30秒過期
    cache.set(f'powerflowsub_result_{request.user.username}', ['正在執行...請稍後','跑分岐中'], 1800)
    # 返回執行頁面
    args = {"messages":['正在執行...請稍後']}

    return powerflow_page(request, args)

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
@login_required
def upload_page_of_upload_errorcircuit(request, *args):

    return MyPage(request,*args).upload_page_of_upload_errorcircuit()

    
@login_required
def upload_errorcircuit(request, *args):
    args = MyFunctions(request).upload_errorcircuit(upload_what = 'savfile')
    sav_file = request.FILES.get("savfile",0)
    sav_file_name = str(sav_file)[0:4] 
    savfiles = [sav_file_name]   
    def background_task(user, savfiles):
        # args = MyFunctions(request).filter()
        # cache.set(f'upload_result_{request.user.username}', ['error'], 10)  # 10秒過期
        args = MyFunctions(request).filter_errorcircuit(savfiles)
        
    #     # 使用 cache 存儲結果
        cache.set(f'upload_errorcircuit_result_{user.username}', ['upload_errorcircuit',args], 30)  # 30秒過期        
        # try:
        # # 執行任務
        #     args = MyFunctions(request).filter(savfiles)
            
        # #     # 使用 cache 存儲結果
        #     cache.set(f'upload_result_{user.username}', ['upload',args], 30)  # 30秒過期
        # except Exception as err:

        #     cache.set(f'upload_result_{request.user.username}', ['error',err], 10)  # 10秒過期
            
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

@login_required
def delete_sav_errorcircuit(request):

    return upload_page_of_upload_errorcircuit(request, MyFunctions(request).delete_sav_errorcircuit())        



###
###===================================================
###                    error circuit執行頁面
###===================================================
### 
@login_required
def errorcircuit_page(request, *args):

    return MyPage(request,*args).errorcircuit_page()




@login_required
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
@login_required
def dynamic_page(request, *args):
   
    return MyPage(request,*args).dynamic_page()




@login_required
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
@login_required
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

    return MyPage(request, args).prepare_writing_data_page()
###
###===================================================
###    用執行idv的funcuction 將預覽的內容(暫存idv檔) 寫入sav檔
###===================================================
### 

@login_required
def prepare_writing_data(request, *args):


    args = MyFunctions(request).upload(upload_what = 'writing_data')
    savfilelist = request.POST.getlist('year')

    def background_task(user, savfilelist):
        args = MyFunctions(request).write_idvfile_content_to_savfile(savfilelist)
        args_filter = MyFunctions(request).filter(savfilelist)
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
    args = {"messages":['正在執行...請稍後']}

    return prepare_writing_data_page(request, args)

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
            os.remove(result[1]['temp_idvpath'])
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
@login_required
def download_page(request):

    pag = MyPage(request)
    return pag.DownloadPage(pag.request).download_page()

@login_required
def download_savefile_page(request,*args):

    return DownloadPage(request,*args).download_savefile_page()


@login_required
def download_powerflow_page(request,*args):

    
    return DownloadPage(request,*args).download_powerflow_page()

@login_required
def download_errorcircuit_page(request,*args):
    
    return DownloadPage(request,*args).download_errorcircuit_page()

@login_required
def download_dynamic_page(request,*args):

    return DownloadPage(request,*args).download_dynamic_page()

@login_required
def download_idvfile_page(request,*args):
    pag = MyPage(request)
    return pag.DownloadPage(pag.request,*args).download_idvfile_page()


@login_required
def download_idvfile_for_create_page(request,*args):

    return DownloadPage(request,*args).download_idvfile_for_create_page()
###
###===================================================
###                    下載檔案
###===================================================
###
@login_required
def download_savefile(request):
    if request.POST.getlist('year')==[]:

        return download_savefile_page(request, {'messages':['至少勾選一個年份']}) 

    args = MyDownload(request).download_savefile()
    if args["error"]:
        return download_savefile_page(request, {'messages':['下載成功']})       
    else:
        with open(args["file_path"], 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        response['Content-Disposition'] = 'attachment; filename=SavFile.zip'

        fileprocess.remove_file(args["file_path"])

        return response             

@login_required
def download_powerflow(request): 
    if request.POST.getlist('year')==[]:

        return download_powerflow_page(request, {'messages':['至少勾選一個年份']}) 

    args = MyDownload(request).download_powerflow()
    if args["error"]:
        return download_powerflow_page(request, {'messages':[f'下載失敗\\n錯誤訊息:{args["error_messages"]}']})       
    else:
        with open(args["file_path"], 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        if args['download_what']=='download_powerflow':
            response['Content-Disposition'] = 'attachment; filename=Powerflow.zip'
        elif args['download_what']=='download_powerflow_log':
            response['Content-Disposition'] = 'attachment; filename=Powerflow_log.zip'
        else:
            return download_powerflow_page(request, {'messages':['下載失敗，no this buttom']}) 

        fileprocess.remove_file(args["file_path"])

        return response  

@login_required
def download_errorcircuit(request): 
    if request.POST.getlist('year')==[]:

        return download_errorcircuit_page(request, {'messages':['至少勾選一個年份']}) 

    args = MyDownload(request).download_errorcircuit()
    print(args)
    if args["error"]:
        return download_errorcircuit_page(request, {'messages':[f'下載失敗\\n錯誤訊息:{args["error_messages"]}']})       
    else:
        with open(args["file_path"], 'rb') as model_excel:
            result = model_excel.read()

        response = HttpResponse(result)

        if args['download_what']=='download_errorcircuit':
            response['Content-Disposition'] = 'attachment; filename=ErrorCircuit.zip'
        elif args['download_what']=='download_errorcircuit_log':
            response['Content-Disposition'] = 'attachment; filename=ErrorCircuit_log.zip'
        else:
            return download_powerflow_page(request, {'messages':['下載失敗，no this buttom']})         
        

        fileprocess.remove_file(args["file_path"])

        return response  

@login_required
def download_dynamic(request): 
    if request.POST.getlist('year')==[]:

        return download_dynamic_page(request, {'messages':['至少勾選一個年份']}) 

    args = MyDownload(request).download_dynamic()
    print(args)
    if args["error"]:
        return download_dynamic_page(request, {'messages':[f'下載失敗\\n錯誤訊息:{args["error_messages"]}']})       
    else:
        with open(args["file_path"], 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        response['Content-Disposition'] = 'attachment; filename=Dynamic.zip'

        # fileprocess.remove_file(args["file_path"])

        return response 

@login_required
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
    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter/Powerflow",
        'savfiledir': f"../Data/User/{user}/SavFile/Powerflow",
        'user': f'{user}',
        'targetdir': f"../Data/User/{user}/filter/Powerflow"
    }      
    print(args)
    return GetData().bus_data(args)

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
    return GetData().bus_data(args)    

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
    return GetData().three_winding_transformer_data(args)    

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
    return GetData().two_winding_transformer_data(args)    


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
    return GetData().machine_data(args)    


def api_for_get_machine_bus_data_of_dynamic(request):
    year = request.GET.get('year')
    user = request.GET.get('user')
    labeltype = request.GET.get('labeltype')

    args = {
        'labeltype': labeltype,
        'filterfiles': year,
        'filterdir': f"../Data/User/{user}/filter/Powerflow",
    }
    return GetData().machine_data(args)  



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
    return GetData().trip_line_data(args)


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
    return GetData().zone_data(args)    

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
    return GetData().area_data(args)     

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
    return GetData().owner_data(args)    

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
    return GetData().load_data(args)      

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
    return GetData().branch_data(args)      