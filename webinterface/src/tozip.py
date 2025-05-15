import os
import zipfile
from . import fileprocess
def to_zip(zipfolder,zipfilename, file):
    homedir = os.getcwd()
    os.makedirs(zipfolder, exist_ok=True)
    
    with zipfile.ZipFile(zipfolder+'/'+zipfilename+'.zip', mode='w') as zf:
        print('file -->',file)
        for f in file:
            # fileprocess.copy_file(f, zipfolder+zipfilename)            
            _, filename= os.path.split(f)  
            basepath, relative = f.split('AnonymousUser/')
            print('relative',f) 
            print('filename=',filename)
            # print('_=',_)
            # relative_path = os.path.relpath(f, zipfolder)
            # print(relative_path)
            # os.chdir(_)     
            zf.write(f, arcname=relative, compress_type=zipfile.ZIP_DEFLATED) 
            # fileprocess.remove_file(filename)
    # os.chdir(homedir)

    # with az.sevenzip.SevenZipArchive() as archive:
    #     # 添加第一個文件
    #     for f in file:
    #         _, filename= os.path.split(f)
    #         archive.create_entry(filename, f)



    #     # 創建並保存 7z 存檔
    #     archive.save(zipfilename+'.zip')



def powerflow_to_zip(years, zipfolder, zipfilename, powerflow_dir, powerflowsub_dir):
    # 定義電壓等級
    voltage_levels = ['161KV_N-1', '345KV_N-1', '345KV_N-2']
    

    # 建立壓縮檔
    with zipfile.ZipFile(f'{zipfolder}/{zipfilename}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for year in years:
            for voltage_level in voltage_levels:
                
                # powerflow 基礎資料夾路徑
                powerflow_base = f"{powerflow_dir}/{year}/{voltage_level}"
                print('powerflow_base',powerflow_base)
                # powerflowsub 基礎資料夾路徑（僅 345kv_n1）
                powerflowsub_base = f"{powerflowsub_dir}/{year}/{voltage_level}/close"
                
                # 處理 powerflow 資料夾中的 .acc 檔案
                if os.path.exists(powerflow_base):
                    for area_zone in os.listdir(powerflow_base):
                        powerflow_result_dir = os.path.join(powerflow_base, area_zone)
                        if os.path.isdir(powerflow_result_dir):
                            for root, _, files in os.walk(powerflow_result_dir):
                                for file in files:
                                    
                                    if file.endswith('.acc'):
                                        file_path = os.path.join(root, file)
                                        # 新的壓縮檔內路徑
                                        zip_path = f"{voltage_level}/{year}/powerflow/{area_zone}/{file}"
                                        zipf.write(file_path, zip_path)
                
                # 處理 powerflowsub 資料夾中的 .acc 檔案（若存在）
                if os.path.exists(powerflowsub_base):
                    for area_zone in os.listdir(powerflowsub_base):
                        powerflowsub_result_dir = os.path.join(powerflowsub_base, area_zone)
                        print('powerflowsub_dir --> ',powerflowsub_result_dir)
                        if os.path.isdir(powerflowsub_result_dir):
                            for root, _, files in os.walk(powerflowsub_result_dir):
                                for file in files:
                                    
                                    if file.endswith('.acc'):
                                        file_path = os.path.join(root, file)
                                        # 新的壓縮檔內路徑
                                        zip_path = f"{voltage_level}/{year}/powerflowsub/close/{area_zone}/{file}"
                                        zipf.write(file_path, zip_path)

    


def powerflow_to_zip__(zipfolder, zipfilename, file_list):
    os.makedirs(zipfolder, exist_ok=True)
    #PowerFlow → Data\User\AnonymousUser\PowerFlow\115P\115P.acc
    #PowerFlowSub → Data\User\AnonymousUser\PowerFlowSub\115P\345KV_N-1\close\Zone_1\3068.acc
    #因為PowerFlow沒有分電壓等級資料夾，所以要從PowerFlowSub先取得故要先分類檔案
    # 分類 PowerFlow / PowerFlowSub 檔案
    powerflow_files = []
    powerflowsub_files = []
    for f in file_list:
        path_parts = os.path.normpath(f).split(os.sep)
        if 'PowerFlowSub' in path_parts:
            powerflowsub_files.append(f)
        elif 'PowerFlow' in path_parts:
            powerflow_files.append(f)

    # 建立年度對應變電站層級字典
    year_to_voltage = {}
    for f in powerflowsub_files:
        path_parts = os.path.normpath(f).split(os.sep)
        try:
            idx = path_parts.index('PowerFlowSub')
            year = path_parts[idx + 1]
            voltage = path_parts[idx + 2]
            year_to_voltage[year] = voltage
        except Exception as e:
            print(f"️ 解析 PowerFlowSub 路徑失敗: {f}，錯誤: {e}")

    # 壓縮檔案
    with zipfile.ZipFile(os.path.join(zipfolder, f"{zipfilename}.zip"), mode='w') as zf:

        # 處理 PowerFlowSub 檔案
        for f in powerflowsub_files:
            path_parts = os.path.normpath(f).split(os.sep)
            try:
                idx = path_parts.index('PowerFlowSub')
                year = path_parts[idx + 1]
                voltage = path_parts[idx + 2]
                sub_path = os.path.join(*path_parts[idx + 3:])  # e.g. close/Zone_43/xxx.acc

                new_path = os.path.join(voltage, year, 'PowerFlowSub', sub_path)
                print(f"[Sub] 壓縮路徑: {new_path}")
                zf.write(f, arcname=new_path, compress_type=zipfile.ZIP_DEFLATED)

            except Exception as e:
                print(f"️ 處理 PowerFlowSub 檔案失敗: {f}，錯誤: {e}")

        # 處理 PowerFlow 檔案
        for f in powerflow_files:
            path_parts = os.path.normpath(f).split(os.sep)
            try:
                idx = path_parts.index('PowerFlow')
                year = path_parts[idx + 1]
                voltage = year_to_voltage.get(year)
                if not voltage:
                    print(f"️ 找不到年度 {year} 的變電站層級，請確認有對應 PowerFlowSub 資料")
                    continue

                filename = os.path.basename(f)
                new_path = os.path.join(voltage, year, 'PowerFlow', filename)
                print(f"[Flow] 壓縮路徑: {new_path}")
                zf.write(f, arcname=new_path, compress_type=zipfile.ZIP_DEFLATED)

            except Exception as e:
                print(f"️ 處理 PowerFlow 檔案失敗: {f}，錯誤: {e}")

# folder = "test/"     
# file = os.listdir(folder)
# for i in range(len(file)):
#     file[i] = os.path.join(folder,file[i]).replace('\\','/')+'/'+file[i]+'.rel'

# to_zip(file) 