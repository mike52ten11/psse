import os
import json

from django.http import JsonResponse

from ..src import fileprocess



class Delete:
    def __init__(self, request):
        self.request = request


    def action_of_delete_savfile(self):
        self.params = self.request.POST.get('params', '{}')
        self.params = json.loads(self.params) if self.params else {}
        if not self.params and self.request.content_type == 'application/json':
            self.params = json.loads(request.body)        
        # params = request.POST.get('params', '{}')
        # print('params -->',params)

        # params = json.loads(params) if params else {}
        # if not params and request.content_type == 'application/json':
        #     params = json.loads(request.body)
        
        # 从参数中获取各种目录信息
        savfilelist = self.params.get('savfilelist', '')
        print(savfilelist)

        savfile_dir = self.params.get('savfile_dir', 'default_savfile_dir')
        idvfile_dir = self.params.get('idvfile_dir', '')
        powerflow_dir = self.params.get('powerflow_dir', '')
        powerflowsub_dir = self.params.get('powerflowsub_dir', '')
        dynamic_dir = self.params.get('dynamic_dir', '')
        errorcircuit_dir = self.params.get('errorcircuit_dir', '')
        filter_dir = self.params.get('filter_dir', '')  
        try:    
            for removefile in savfilelist:
                print(f'{savfile_dir}/{removefile}.sav')
                #刪除勾選的檔案
                fileprocess.remove_file(f'{savfile_dir}/{removefile}.sav')
                fileprocess.remove_file(f'{savfile_dir}/{removefile}.raw')

                #刪除已有的IDV檔案
                fileprocess.remove_file(f'{idvfile_dir}/{removefile}.idv') 
                #刪除已有的電力潮流檔案
                fileprocess.remove_dir(f'{powerflow_dir}/{removefile}')
                #除電力潮流分岐檔案
                fileprocess.remove_dir(f'{powerflowsub_dir}/{removefile}')
                #刪除已有的故障電流檔案
                fileprocess.remove_dir(f'{errorcircuit_dir}/{removefile}')   
                #刪除已有的暫態檔案
                fileprocess.remove_dir(f'{dynamic_dir}/{removefile}') 

                #先刪除顯示檔案
                fileprocess.remove_file(f'{filter_dir}/area/area_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/bus/bus_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/branch/branch_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/load/load_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/owner/owner_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/zone/zone_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/machine/machine_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/tripline/tripline_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/three_winding_transformer/three_winding_transformer_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/two_winding_transformer/two_winding_transformer_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/two_winding_transformer/two_winding_transformer_{removefile}.npz')
                fileprocess.remove_file(f'{filter_dir}/fixedshunt/fixedshunt{removefile}.npz')


                fileprocess.remove_file(f'{filter_dir}/area/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/bus/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/area/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/load/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/owner/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/zone/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/machine/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/tripline/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/three_winding_transformer/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/two_winding_transformer/latest.npz')
                fileprocess.remove_file(f'{filter_dir}/fixedshunt/latest.npz')

            args = {'messages':['刪除成功']}
        except Exception as e: 
            print(e)
            args = {'messages':[f'刪除失敗 {e}']}
        
        return JsonResponse({'results':args}, 
                            json_dumps_params={'ensure_ascii': False},
                            safe=False)          

    def action_of_run_powerflow(self):
        pass

    def action_of_run_powerflow_sub(self):
        pass

    def action_of_run_errorcircuit(self):
        pass    

    def action_of_filter_all(self,filter_dir ,removefile_name):
        fileprocess.remove_file(f'{filter_dir}/area/area_{removefile_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/bus/bus_{removefile_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/load/load_{removefile_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/owner/owner_{removefile_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/zone/zone_{removefile_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/machine/machine_{removefile_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/tripline/tripline_{removefile_name}.npz')

        fileprocess.remove_file(f'{filter_dir}/area/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/bus/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/area/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/load/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/owner/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/zone/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/machine/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/tripline/latest.npz')                     

        