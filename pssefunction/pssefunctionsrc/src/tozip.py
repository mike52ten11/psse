import os
import zipfile
from . import fileprocess
def to_zip(zipfolder,zipfilename, file):
    homedir = os.getcwd()
    os.makedirs(zipfolder, exist_ok=True)
    
    with zipfile.ZipFile(zipfolder+'/'+zipfilename+'.zip', mode='w') as zf:
        print(file)
        for f in file:
            # fileprocess.copy_file(f, zipfolder+zipfilename)            
            _, filename= os.path.split(f)  
            print('f=',f) 
            print('filename=',filename)
            print('_=',_)
            relative_path = os.path.relpath(f, zipfolder)
            print(relative_path)
            # os.chdir(_)     
            zf.write(f, arcname=relative_path, compress_type=zipfile.ZIP_DEFLATED) 
            # fileprocess.remove_file(filename)
    # os.chdir(homedir)

    # with az.sevenzip.SevenZipArchive() as archive:
    #     # 添加第一個文件
    #     for f in file:
    #         _, filename= os.path.split(f)
    #         archive.create_entry(filename, f)



    #     # 創建並保存 7z 存檔
    #     archive.save(zipfilename+'.zip')



# folder = "test/"     
# file = os.listdir(folder)
# for i in range(len(file)):
#     file[i] = os.path.join(folder,file[i]).replace('\\','/')+'/'+file[i]+'.rel'

# to_zip(file) 