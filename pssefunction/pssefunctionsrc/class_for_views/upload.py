import os
import json
import subprocess
from django.http import JsonResponse

from ..src import fileprocess
from ..src.base.run_pyfile_by_execmd import Run_pyfile_by_execmd

class Upload:
    def __init__(self, request):
        self.request = request
        self.uploaded_file = request.FILES['file']
        self.params = request.POST.get('params', '{}')
        self.params = json.loads(self.params) if self.params else {}
        if not self.params and request.content_type == 'application/json':
            self.params = json.loads(request.body)

    def upload_savfile(self):
        savfile_path = self.params.get('savfile_path', '')
        sav_file_name = self.params.get('sav_file_name', self.uploaded_file.name)
        savfile_dir = self.params.get('savfile_dir', 'default_savfile_dir')
        idvfile_dir = self.params.get('idvfile_dir', '')
        powerflow_dir = self.params.get('powerflow_dir', '')
        powerflowsub_dir = self.params.get('powerflowsub_dir', '')
        dynamic_dir = self.params.get('dynamic_dir', '')
        errorcircuit_dir = self.params.get('errorcircuit_dir', '')
        filter_dir = self.params.get('filter_dir', '')
        print('savfile_dir -->',savfile_dir)
        # try:
        os.makedirs(f'{savfile_dir}', exist_ok = True)
        
        os.makedirs(f'{idvfile_dir}', exist_ok = True)
        os.makedirs(f'{powerflow_dir}', exist_ok = True)
        os.makedirs(f'{powerflowsub_dir}', exist_ok = True)
        os.makedirs(f'{powerflowsub_dir}', exist_ok = True)
        os.makedirs(f'{dynamic_dir}', exist_ok = True)
        os.makedirs(f'{filter_dir}', exist_ok = True)

        with open(savfile_path, 'wb+') as destination:
            for chunk in self.uploaded_file.chunks():
                destination.write(chunk)
        cmd = Run_pyfile_by_execmd(python_location= "python"
                                            ,pyfile= "pssefunctionsrc/src/base/to_raw.py"
                                            ,args=f"--Sav_File {sav_file_name} "\
                                                f"--savfiledir {savfile_dir} "\
                                                f"--target_dir {savfile_dir}")    
        print('cmd-->',cmd)

        r = subprocess.run(cmd,capture_output=True, shell=True)
        if r.returncode != 0:

            
            
            error_message = r.stderr.decode('big5').strip()          
            
            print(f"Error occurred: {error_message}")
            return JsonResponse({
                        "error":1
                        ,"return_value":{
                            "function":"subprocess.Popen in upload.py"
                            ,"front_message":f"轉成raw檔失敗，{error_message}"
                            ,"backend_message":f'error_message -->{error_message}\n'\
                                                f'r.returncode --> {r.returncode}'
                        }
 
                    }
                )
        fileprocess.remove_file(f'{idvfile_dir}/{sav_file_name}.idv')
        fileprocess.remove_dir(f'{powerflow_dir}/{sav_file_name}')
        fileprocess.remove_dir(f'{powerflowsub_dir}/{sav_file_name}')
        fileprocess.remove_dir(f'{errorcircuit_dir}/{sav_file_name}')
        fileprocess.remove_file(f'{filter_dir}/area/area_{sav_file_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/bus/bus_{sav_file_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/load/load_{sav_file_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/owner/owner_{sav_file_name}.npz')
        fileprocess.remove_file(f'{filter_dir}/zone/zone_{sav_file_name}.npz')

        fileprocess.remove_file(f'{filter_dir}/area/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/load/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/owner/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/zone/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/branch/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/bud/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/fixedshunt/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/machine/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/three_winding_transformer/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/tripline/latest.npz')
        fileprocess.remove_file(f'{filter_dir}/two_winding_transformer/latest.npz')

        return JsonResponse({
            "error":0,
            'message': '檔案接收成功',
            'file_path': savfile_path
        })
        # except Exception as e:
        #     print('ERROR: ',e)
        #     return JsonResponse({'error': str(e)}, status=500)

    def upload_dynamicfile(self):
        
        dynamicfile_path = self.params.get('dynamicfile_path', '')
        dynamic_dir = self.params.get('dynamicfile_dir', '')
        
        try:
            os.makedirs(f'{dynamic_dir}', exist_ok = True)
            with open(dynamicfile_path, 'wb+') as destination:
                for chunk in self.uploaded_file.chunks():
                    destination.write(chunk)
            return JsonResponse({
                'message': '檔案接收成功',
                'file_path': dynamicfile_path
            })
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    def upload_idvfile(self):
        excute_idvfile_path = self.params.get('excute_idvfile_path', '')
        excute_idvfile_dir = self.params.get('excute_idvfile_dir', '')
        try:
            os.makedirs(f'{excute_idvfile_dir}', exist_ok = True)
            with open(excute_idvfile_path, 'wb+') as destination:
                for chunk in self.uploaded_file.chunks():
                    destination.write(chunk)
            return JsonResponse({
                'message': '檔案接收成功',
                'file_path': excute_idvfile_path
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def upload_idvfile_of_writata(self):
        idvfile_path = self.params.get('idvfile_path', '')
        idvfile_dir = self.params.get('idvfile_dir', '')
        
        try:
            os.makedirs(f'{idvfile_dir}', exist_ok = True)
            with open(idvfile_path, 'wb+') as destination:
                for chunk in self.uploaded_file.chunks():
                    destination.write(chunk)
            return JsonResponse({
                'message': '檔案接收成功',
                'file_path': idvfile_path
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)            
