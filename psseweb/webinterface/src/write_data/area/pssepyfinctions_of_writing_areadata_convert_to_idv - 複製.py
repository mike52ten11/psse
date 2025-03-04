
def writeFile(filename, data):  
    f = open(filename, "a")  
    f.write(data)  
    f.close()  


def psspy_to_idv(psspycommand,idvpath):
    # import logging       
    # from Log.LogConfig import Setlog   

    # logger = Setlog(logfolder= 'Log/'+userName+'/convert_idv_Log/', level=logging.INFO,logger_name='psse')
    idvcoomand = psspycommand['function']
    data = psspycommand['data']

    parrameter = ','.join(data)
    writedata = f"BAT_{idvcoomand.upper()},{parrameter}\n"
    try:
        writeFile(idvpath, writedata)
        return {"error":0
                    ,"return_value":{
                        "front_message":f"執行成功"
                    }}
    except Exception as e:    
        print(e)
        return {
                    "error":1
                    ,"return_value":{
                        "function":"psspy_to_idv in area"
                        ,"front_message":f"執行失敗"
                        ,"backend_message":f'error_message -->{e}\n'
                    }
 
                }    
    # try:
    #     idvcoomand = psspycommand['function']
    # except Exception as e:    
    #     print(e)
    # try:
    #     data = psspycommand['data']
    # except Exception as e:    
    #     print(e)

    # try:
    #     labeltype = psspycommand['labeltype']
    # except Exception as e:    
    #     logger.error('convert faild occur %s',str(e))  


    

    
