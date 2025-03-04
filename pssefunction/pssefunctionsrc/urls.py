from django.urls import path
from .views import (    powerflow
                        ,powerflowsub
                        ,errorcircuit
                        ,dynamic
                        ,filter_label
                        ,filter_dispaly
                        ,get_filter_data
                        ,run_idv                        
                        ,filter_labelfile
                        ,filter_all_label
                        ,upload_savfile
                        ,upload_dynamicfile
                        ,upload_idvfile
                        ,upload_idvfile_of_writata
                                                
                        ,delete_savfile

                        ,download_savfile
                        ,download_powerflow
                        ,download_errorcircuit
                        ,download_dynamic
                        ,download_idvfile_for_create
                        
                        ,find_savfile
                        ,find_acc_files_in_dir
                        ,find_rel_files_in_dir
                        ,find_out_files_in_dir

                        ,write_data_to_savfile
                    )


urlpatterns = [
    path('powerflow/', powerflow, name='powerflow'),
    path('powerflowsub/', powerflowsub, name='powerflowsub'),
    path('errorcircuit/', errorcircuit, name='errorcircuit'),    
    path('dynamic/', dynamic, name='dynamic'),
    path('idv/', run_idv, name='idv'),

    path('filter/', filter_label, name='filter'),
    path('filter_all/', filter_all_label, name='filter_all'),

    path('filter_dispaly/', filter_dispaly, name='filter_dispaly'),
    path('get_filter_data/', get_filter_data, name='get_filter_data'),
    path('find_savfile/', find_savfile, name='find_savfile'),
    path('find_acc_files_in_dir/', find_acc_files_in_dir, name='find_acc_files_in_dir'),
    path('find_rel_files_in_dir/', find_rel_files_in_dir, name='find_rel_files_in_dir'),
    path('find_out_files_in_dir/', find_out_files_in_dir, name='find_out_files_in_dir'),
    path('filter_labelfile/', filter_labelfile, name='filter_labelfile'),

    

    path('upload_savfile/', upload_savfile, name='upload_savfile'),
    path('upload_dynamicfile/', upload_dynamicfile, name='upload_dynamicfile'),
    path('delete_savfile/', delete_savfile, name='delete_savfile'),
    path('upload_idvfile/', upload_idvfile, name='upload_idvfile'),
    path('upload_idvfile_of_writata/', upload_idvfile_of_writata, name='upload_idvfile_of_writata'),


    path('download_savfile/', download_savfile, name='download_savfile'),
    path('download_powerflow/', download_powerflow, name='download_powerflow'),
    path('download_errorcircuit/', download_errorcircuit, name='download_errorcircuit'),
    path('download_dynamic/', download_dynamic, name='download_dynamic'),
    path('download_idvfile_for_create/', download_idvfile_for_create, name='download_idvfile_for_create'),

    path('write_data_to_savfile/', write_data_to_savfile, name='write_data_to_savfile')
]