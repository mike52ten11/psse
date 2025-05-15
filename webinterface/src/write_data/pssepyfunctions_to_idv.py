

import os
def writeFile(filename, data):  
    f = open(filename, "a")  
    f.write(data)  
    f.close()  

def create_idvfile(idvfilepath, writedata):
    try:
        writeFile(idvfilepath, writedata)
        return {"error":0
                    ,"return_value":{
                        "front_message":f"寫入idv檔成功"
                    }}
    except Exception as e:    
        print(e)
        return {
                    "error":1
                    ,"return_value":{
                        "function":"psspy_to_idv in area"
                        ,"front_message":f"寫入失敗"
                        ,"backend_message":f'error_message -->{e}\n'
                    }

                }    


class psspy_to_idv:
    def __init__(self,psspycommand,idvpath):
        self.idvcoomand = psspycommand['function']
        self.data = psspycommand['data']
        self.labeltype = psspycommand['labeltype']
        self.idvpath = idvpath
        os.makedirs(self.idvpath,exist_ok=True)
    def area(self):


        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/area.idv", writedata=writedata)

    def zone(self):

        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/zone.idv", writedata=writedata)

    def owner(self):

        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/owner.idv", writedata=writedata)

    def bus(self):

        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/bus.idv", writedata=writedata)

    def machine(self):
        # writedata = 'BAT_PLANT_DATA,'+data[0]+',0,0,0,1.00,100.00\n'
        # create_idvfile(idvfilepath=f"{self.idvpath}/temp.idv", writedata=writedata) 
        if self.labeltype=='machine':
            writedata = f'BAT_PLANT_DATA,{self.data[0]},0,0,0,1.00,100.00\n'
            create_idvfile(idvfilepath=f"{self.idvpath}/machine.idv", writedata=writedata)    
            parrameter = ','.join(self.data)   
            writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n" 
            create_idvfile(idvfilepath=f"{self.idvpath}/machine.idv", writedata=writedata)
        else:
            writedata = 'BAT_NEWSEQ,;\n' 
            create_idvfile(idvfilepath=f"{self.idvpath}/machine.idv", writedata=writedata)
            
            parrameter = ','.join(self.data)
    
            writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"        
            create_idvfile(idvfilepath=f"{self.idvpath}/machine.idv", writedata=writedata)                 
    def load(self):

        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter};\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/load.idv", writedata=writedata)

    def branch(self):   
        if self.labeltype=='branch':
            parrameter = ','.join(self.data)
            writedata = f"BAT_{self.idvcoomand.upper()},{parrameter};\n"
            create_idvfile(idvfilepath=f"{self.idvpath}/branch.idv", writedata=writedata) 

        elif self.labeltype=='seq_branch':
            parrameter = ','.join(self.data)    
            writedata = f"BAT_NEWSEQ,;\nBAT_{self.idvcoomand.upper()},{parrameter};\n"
            create_idvfile(idvfilepath=f"{self.idvpath}/branch.idv", writedata=writedata)           
        else:
            raise AssertionError("no this labeltype")
            pass    
            
    def twowinding(self):
        if self.labeltype=='twowinding':
            parrameter = ','.join(self.data)
            writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
            create_idvfile(idvfilepath=f"{self.idvpath}/twowinding.idv", writedata=writedata)
        elif self.labeltype=='seq_twowinding':
            parrameter = ','.join(self.data)    
            writedata = f"BAT_NEWSEQ,;\nBAT_{self.idvcoomand.upper()},{parrameter};\n"
            create_idvfile(idvfilepath=f"{self.idvpath}/twowinding.idv", writedata=writedata)           
        else:
            raise AssertionError("no this labeltype")
            pass   
    def twowinding_edit(self):    

        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/twowinding_edit.idv", writedata=writedata)
        
    def threewinding(self):
        if self.labeltype=='three_wnd_imped_data_4':
            parrameter = ','.join(self.data)
            writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
            create_idvfile(idvfilepath=f"{self.idvpath}/threewinding.idv", writedata=writedata)
        elif self.labeltype=='seq_three_winding_data_3':
            parrameter = ','.join(self.data)    
            writedata = f"BAT_NEWSEQ,;\nBAT_{self.idvcoomand.upper()},{parrameter};\n"
            create_idvfile(idvfilepath=f"{self.idvpath}/threewinding.idv", writedata=writedata)           
        else:
            raise AssertionError("no this labeltype")
            pass         

    def threewinding_winding(self):

        parrameter = ','.join(self.data)
        writedata = f"BAT_{self.idvcoomand.upper()},{parrameter}\n"
        create_idvfile(idvfilepath=f"{self.idvpath}/threewinding_winding.idv", writedata=writedata)
               
# def psspy_to_idv(psspycommand,idvpath):
#     # import logging       
#     # from Log.LogConfig import Setlog   

#     # logger = Setlog(logfolder= 'Log/'+userName+'/convert_idv_Log/', level=logging.INFO,logger_name='psse')
#     idvcoomand = psspycommand['function']
#     data = psspycommand['data']

#     parrameter = ','.join(data)
#     writedata = f"BAT_{idvcoomand.upper()},{parrameter}\n"
#     try:
#         writeFile(idvpath, writedata)
#         return {"error":0
#                     ,"return_value":{
#                         "front_message":f"執行成功"
#                     }}
#     except Exception as e:    
#         print(e)
#         return {
#                     "error":1
#                     ,"return_value":{
#                         "function":"psspy_to_idv in area"
#                         ,"front_message":f"執行失敗"
#                         ,"backend_message":f'error_message -->{e}\n'
#                     }
 
#                 }    
#     # try:
#     #     idvcoomand = psspycommand['function']
#     # except Exception as e:    
#     #     print(e)
#     # try:
#     #     data = psspycommand['data']
#     # except Exception as e:    
#     #     print(e)

#     # try:
#     #     labeltype = psspycommand['labeltype']
#     # except Exception as e:    
#     #     logger.error('convert faild occur %s',str(e))  


    

    
