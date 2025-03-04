def checkfilename(raw_file):

    if str(raw_file).split('.')[-1]!='sav':
        messages = {'ifok':False
                    ,'show_message':['請上傳.sav'],
                    'error_message':'使用者副檔名給'+str(raw_file).split('.')[-1]}
        return messages

    try:
        check_filename = int(str(raw_file)[0:3])
        if str(raw_file)[3]=='P' or str(raw_file)[3]=='L':
            messages = {'ifok':True
                    ,'show_message':['']
                    ,'error_message':['']}
            return messages
        else:
            messages = {'ifok':False
                        ,'show_message':['上傳失敗 檔案第4個字需P 或 L 例:112Pxx.sav。']
                        ,'error_message':['']}
            return messages    
    except Exception as e:
        messages = {'ifok':False
                    ,'show_message':['上傳失敗 檔案前3個需數字，例:112Pxx.sav。']
                    ,'error_message':str(e)}

        return messages