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
            line = line.rstrip()

            # 最後固定6碼是第6欄
            last6 = line[-6:].strip()

            # 剩下的內容
            rest = line[:-6].strip()

            # 先抓出前4個數字欄位（可能是整數或浮點數）
            number_matches = re.findall(r'\d+\.\d+|\d+', rest)

            #if len(number_matches) < 4:
            #    print(f"⚠️ 數字欄位不足，跳過該行：{line}")
            #    continue
    
            # 前四欄（第1～4欄）
            col1 = number_matches[0]
            col2 = number_matches[1]
            col3 = number_matches[2]
            col4 = number_matches[3]

            # 從 rest 中把前4個數字移除，剩下的就是名稱欄位
            pattern = re.compile(r'\d+\.\d+|\d+')
            pos = 0
            count = 0
            while count < 4:
                m = pattern.search(rest, pos)
                if m:
                    pos = m.end()
                    count += 1
                else:
                    break

            # 名稱是從第4個數字之後到末端（扣掉最後6位）
            
            col5 = rest[pos:].strip()

            writevalue = [col1, col2, col3, col4, col5, last6]

            KA = float(col3) / math.sqrt(3) / float(last6) * 100
            if int(float(last6)) == 161:
                adj_KA = math.sqrt(1 + math.pow(1.414 * math.exp(-(377 * 3 / 60) / float(col4)), 2)) / 1.2 * KA
            else:
                adj_KA = math.sqrt(1 + math.pow(1.414 * math.exp(-(377 * 2 / 60) / float(col4)), 2)) / 1.3 * KA    

            writevalue += [KA, adj_KA, str(max(adj_KA, KA))]

            pd.DataFrame([writevalue]).to_csv(outputpath,
                                          mode='a', header=False, index=False,
                                          encoding='ansi')
        return {"error":0,"ifreturn":0}                                        
    except Exception as e:      
        print('ERROR',e)    
        return {"error":1,"function":"convert_program.convert_rel_to_excelFile"
                        ,"front_message":"轉csv檔失敗","backend_message":[e]}
                                 
# convert_rel_to_excelFile(relfile=r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\ErrorCircuit\115\115.rel'
#                         ,outputpath=r'D:\Mike\Work_space\業務\電力室合作\optimization\psseweb\User\621882\ErrorCircuit\115\Excel\115.csv')
