def convert_rel_to_excelFile(relfile,outputpath):
    import os
    import re
    import csv
    import pandas as pd
    import math

    try:
        with open(relfile, 'r', encoding='ansi') as file:
            content = file.read()
            lines = [line for line in content.split('\n') if line.strip()]
        if os.path.exists(outputpath):
            os.remove(outputpath) 
        for line in lines:
            txt = re.split(r'\s{1,}', line[0:-6])
            # print('line[-6:]-->',line[-6:])
            
            writevalue = [_ for _ in txt+[line[-6:]] if _ != '']
            # print('writevalue-->',writevalue)

            KA = float(writevalue[2])/math.sqrt(3)/float(line[-6:])*100
            if int(float(line[-6:]))==161:
               adj_KA =  math.sqrt(1 + math.pow(1.414*math.exp(-(377*3/60)/float(writevalue[3])), 2) )/1.2*KA
            else:
               adj_KA =  math.sqrt(1 + math.pow(1.414*math.exp(-(377*2/60)/float(writevalue[3])), 2) )/1.3*KA    
            # print(KA)
            
            writevalue = writevalue + [KA]+ [adj_KA]+ [str(max(adj_KA,KA))]
            # print(writevalue)

            pd.DataFrame([writevalue]).to_csv(outputpath
                                        , mode='a', header=False, index=False
                                        ,encoding='ansi')
        
        # print(math.sqrt(1 + math.pow(1.414*math.exp(-(377*3/60)/26.6167), 2) )/1.2*(122.5652/math.sqrt(3)/161*100))                    
        return {"error":0,"ifreturn":0}                                        
    except Exception as e:      
        print('ERROR',e)    
        return {"error":1,"function":"convert_program.convert_rel_to_excelFile"
                        ,"front_message":"轉csv檔失敗","backend_message":[e]}
                                 
# convert_rel_to_excelFile(relfile=r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\ErrorCircuit\115\115.rel'
#                         ,outputpath=r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\ErrorCircuit\115\Excel\115.csv')