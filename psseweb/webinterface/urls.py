"""psseweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from webinterface import views

urlpatterns = [
###
###===================================================
###                    註冊
###===================================================
###  
    path('sign_up/', views.SignUpView.as_view(), name = "sign_up"),
    
###
###===================================================
###                    忘記密碼
###===================================================
### 
    path('forget_password/',views.forget_password, name='forget_password'),  
###
###===================================================
###                    登入
###===================================================
###  
    path('', views.login_page, name='login_page'),    
    path('login_page', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

###
###===================================================
###                    首頁
###===================================================
###
    path('home/', views.home, name = "home"),

    path('idv_execute_page/', views.idv_execute_page, name = "idv_execute_page"),
    path('idv_execute/', views.idv_execute, name = "idv_execute"),
    path('idv_execute_status/', views.idv_execute_status, name='idv_execute_status'),    


    path('upload_page/', views.upload_page, name = "upload_page"),
    path('upload/', views.upload, name = "upload"),
    path('upload_status/', views.upload_status, name='upload_status'), 


    path('delete_sav/', views.delete_sav, name='delete_sav'), 
    
    path('upload_page_of_upload_powerflow/', views.upload_page_of_upload_powerflow, name='upload_page_of_upload_powerflow'),
    path('upload_powerflow/', views.upload_powerflow, name = "upload_powerflow"),
    path('upload_powerflow_status/', views.upload_powerflow_status, name='upload_powerflow_status'), 
    path('delete_sav_powerflow/', views.delete_sav_powerflow, name='delete_sav_powerflow'),

    path('powerflow_page/', views.powerflow_page, name = "powerflow_page"),
    path('powerflow/', views.powerflow, name = "powerflow"),
    path('powerflow_status/', views.powerflow_status, name='powerflow_status'),   
    path('powerflowsub_status/', views.powerflowsub_status, name='powerflowsub_status'), 



    path('upload_page_of_upload_errorcircuit/', views.upload_page_of_upload_errorcircuit, name='upload_page_of_upload_errorcircuit'),
    path('upload_errorcircuit/', views.upload_errorcircuit, name = "upload_errorcircuit"),
    path('upload_errorcircuit_status/', views.upload_errorcircuit_status, name='upload_errorcircuit_status'), 
    path('delete_sav_errorcircuit/', views.delete_sav_errorcircuit, name='delete_sav_errorcircuit'),

    path('errorcircuit_page/', views.errorcircuit_page, name = "errorcircuit_page"),
    path('errorcircuit/', views.errorcircuit, name = "errorcircuit"),
    path('errorcircuit_status/', views.errorcircuit_status, name='errorcircuit_status'),   



    path('dynamic_page/', views.dynamic_page, name = "dynamic_page"),
    path('dynamic/', views.dynamic, name = "dynamic"),
    path('dynamic_status/', views.dynamic_status, name='dynamic_status'),

###
###===================================================
###                    下載檔案的頁面
###===================================================
### 
    path('home/download_page/', views.download_page, name='download_page'),
    path('home/download_powerflow_page/', views.download_powerflow_page, name='download_powerflow_page'), 
    path('home/download_errorcircuit_page/', views.download_errorcircuit_page, name='download_errorcircuit_page'), 
    path('home/download_savefile_page/', views.download_savefile_page, name='download_savefile_page'),
    path('home/download_idvfile_page/', views.download_idvfile_page, name='download_idvfile_page'),  
    path('home/download_dynamic_page/', views.download_dynamic_page, name='download_dynamic_page'),    
    path('home/download_idvfile_for_create_page/', views.download_idvfile_for_create_page, name='download_idvfile_for_create_page'),    

###
###===================================================
###                    下載檔案
###===================================================
### 
    path('home/download_savefile/', views.download_savefile, name='download_savefile'),
    path('home/download_powerflow/', views.download_powerflow, name='download_powerflow'),
    path('home/download_errorcircuit/', views.download_errorcircuit, name='download_errorcircuit'),
    path('home/download_dynamic/', views.download_dynamic, name='download_dynamic'),
    path('home/download_idvfile_for_create/', views.download_idvfile_for_create, name='download_idvfile_for_create'),
    
###===================================================
###                    取得filter npz資料的API
###===================================================
### 
    path('api/bus-list-of-dynamic/', views.api_for_get_bus_data_of_dynamic, name='buslist-of-dynamic'),
    path('api/machine-list-of-dynamic/', views.api_for_get_machine_bus_data_of_dynamic, name='machinelist-of-dynamic'),
    path('api/trip-line-list-of-dynamic/', views.api_for_get_trip_line_data_of_dynamic, name='tripline-of-dynamic'),
    
    path('api/area-list/', views.api_for_get_area_data, name='arealist'),
    path('api/branch-list/', views.api_for_get_branch_data, name='branchlist'),
    path('api/bus-list/', views.api_for_get_bus_data, name='buslist'),
    path('api/load-list/', views.api_for_get_load_data, name='loadlist'),
    path('api/machine-list/', views.api_for_get_machine_data, name='machinelist'),
    path('api/owner-list/', views.api_for_get_owner_data, name='ownerlist'),
    path('api/threewinding-list/', views.api_for_get_threewinding_data, name='threewindinglist'),
    path('api/twowinding-list/', views.api_for_get_twowinding_data, name='twowindinglist'),
    
    path('api/zone-list/', views.api_for_get_zone_data, name='zonelist'),
###===================================================
###                   新增sav資料的頁面
###===================================================
### 
    path('home/select_which_Label/<str:selection_Label>', views.select_which_Label, name = 'select_Label'),        

# ###
# ###===================================================
# ###                    預覽寫入的內容 的頁面
# ###===================================================
# ###
#     path('home/prepare_writing_data_page/', views.prepare_writing_data_page, name = 'prepare_writing_data_page'),
###
###===================================================
###    用執行idv的funcuction 將預覽的內容 寫入sav檔
###===================================================
### 
    path('prepare_writing_data/', views.prepare_writing_data, name = 'prepare_writing_data'),
    path('prepare_writing_data_page/', views.prepare_writing_data_page, name = "prepare_writing_data_page"),
    path('prepare_writing_data_status/', views.prepare_writing_data_status, name='prepare_writing_data_status'),  
###===================================================
###                   新增sav資料
###===================================================
###     
    path('home/write_to_savfile/area/', views.write_to_savfile_for_area, name='write_to_savfile_for_area'),
    path('home/write_to_savfile/zone/', views.write_to_savfile_for_zone, name='write_to_savfile_for_zone'),
    path('home/write_to_savfile/owner/', views.write_to_savfile_for_owner, name='write_to_savfile_for_owner'),
    path('home/write_to_savfile/bus/', views.write_to_savfile_for_bus, name='write_to_savfile_for_bus'),
    path('home/write_to_savfile/machine/', views.write_to_savfile_for_machine, name='write_to_savfile_for_machine'),
    path('home/write_to_savfile/load/', views.write_to_savfile_for_load, name='write_to_savfile_for_load'),
    path('home/write_to_savfile/branch/', views.write_to_savfile_for_branch, name='write_to_savfile_for_branch'),
    path('home/write_to_savfile/twowinding/', views.write_to_savfile_for_twowinding, name='write_to_savfile_for_twowinding'),
    path('home/write_to_savfile/threewinding/', views.write_to_savfile_for_threewinding, name='write_to_savfile_for_threewinding'),
    path('home/write_to_savfile/threewinding_winding/', views.write_to_savfile_for_threewinding_winding, name='write_to_savfile_for_threewinding_winding'),

]
