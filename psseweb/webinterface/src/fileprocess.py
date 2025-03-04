import sys,os
import shutil
import subprocess
import re
import io

def run_pyfile_by_execmd(python_location: str, pyfile: str, args: str) -> str:

    return f"{python_location} {pyfile} {args}"


def How_many_rawfile(Folder_of_rawfile, fileextension = r'.sav'):
    
    return [_ for _ in os.listdir(Folder_of_rawfile) if _.endswith(fileextension)]


def Read_Raw_data(filename = './PSSEauto/testdata/112P-11109.raw'):
    # 開啟.raw文字檔並讀取內容
    with open(filename, 'rb') as file:
        raw_data = file.read()        
        
    return   raw_data

def Split_Raw_Data(data, from_which_Sign='\n'.encode("mbcs")):

    return data.split(from_which_Sign)

def Split_Label_name(data):
    data =  b' '.join(data)
    pattern = re.compile(b' END OF (.*?) DATA', re.S)
    return re.findall(pattern, data)

def Find_label_position(data, separated_by_X_sign):
    Index = []
    start = 0
    for i in range(len(data)):
        if data[i][0:3] == separated_by_X_sign:            
            Index.append([start,i])
            start=i
    return Index


def LabelName(data, separated_by_X_sign):
    # Split_data = Split_Raw_Data(data, from_which_Sign='\n'.encode(encode_type))
    Index_of_Label_Position = Find_label_position(data, separated_by_X_sign)
    labelname = Split_Label_name(data)
    LABEL = dict(zip(labelname,Index_of_Label_Position))
    return LABEL            

def copy_file(copied_file, target_file):    
    shutil.copy(copied_file, target_file)

def remove_file(myfile):
    if os.path.isfile(myfile):
        os.remove(myfile)
        
def remove_dir(dirname):
    shutil.rmtree(dirname,ignore_errors=True)


def execCmd(cmd):
    try:
        r = subprocess.run(cmd,capture_output=True, shell=True)
        if r.returncode == 0:
            # print(r.stdout.decode("mbcs"))
            return {"error":0,"return_value":r.stdout}
        else:
            error_message = r.stderr          
            # error_message = r.stderr.decode().strip()
            print(f"Error occurred: {error_message}")
            return {
                        "error":1
                        ,"return_value":{
                            "function":"subprocess.Popen in fileprocess.execCmd"
                            ,"front_message":f"執行失敗，{error_message}"
                            ,"backend_message":f'error_message -->{error_message}\n'\
                                                f'r.returncode --> {r.returncode}'
                        }
 
                    }
    except Exception as e:
        # print(f"An exception occurred: {e}")        
        return {
            "error":1
            ,"return_value":{
                    "function":"fileprocess.execCmd in Exception Block"
                    ,"front_message":"執行失敗"
                    ,"backend_message":e
                }
            }
        

# def execCmd(cmd):  
#     try:
        
#         # r = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         # r = subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
#         r = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
#         stdout, stderr =r.communicate()
   
#         # stdout = b'test'
#         # print('stdout >> ',r.stdout)
#         # print('stdout >> ',stdout)
#         # print('r.returncode >> ',r.returncode)
#         if r.returncode == 0:
            
#             return {"error":0,"ifreturn":1,"return_value":stdout}
#         else:
#             # error_message = r.stderr          
#             error_message = stderr.decode().strip()
#             print(f"Error occurred: {error_message}")
#             return {"error":1,"function":"subprocess.Popen in fileprocess.execCmd","front_message":"執行失敗","backend_message":error_message}
            
#     except Exception as e:
#         print(f"An exception occurred: {e}")        
#         return {"error":1,"function":"fileprocess.execCmd","front_message":"執行失敗","backend_message":e}

def writeFile(filename, data):
    try:  
        with open(filename, "ab")  as f:
            f.write(data)
        return {"error":0,"ifreturn":0} 
           
    except Exception as e:      
        print('ERROR',e)    
        return {
                "error":1
                ,"return_value":{
                    "function":"fileprocess.writeFile"
                    ,"front_message":"寫入失敗"
                    ,"backend_message":[e]
                }
            }

def writeFilestr(filename, data):
    try:  
        with open(filename, "a")  as f:
            f.write(data)
        return {"error":0,"ifreturn":0} 
           
    except Exception as e:      
        print('ERROR',e)    
        return {"error":1,"function":"fileprocess.writeFilestr","front_message":"寫入失敗","backend_message":[e]}

def readfile(path):
    try:
        with open(path) as f:
            returnlines = []
            for line in f.readlines():
                returnlines.append(line)
        return {"error":0,"ifreturn":1,"return_value":returnlines}
    except Exception as e:          
        return {"error":1,"function":"fileprocess.readfile","front_message":"讀取失敗","backend_message":e}        

def upload_file_use_writebyte(uploadpath,file):
    
    # f = open(f'{uploadpath}/{file}', "wb+")  
    with open(f'{uploadpath}/{file}', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # for data in file.chunks():      # 分塊寫入文件
        
    #     f.write(data)
        
    # f.close()        

