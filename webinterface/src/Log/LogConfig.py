import logging
import os

def Setlog(logfolder, level=logging.INFO,logger_name='system'):
    os.makedirs(logfolder, exist_ok = True)
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(logfolder+logger_name+'.log', mode='a')
    fileHandler.setFormatter(formatter)

    vlog = logging.getLogger(logger_name)
    vlog.setLevel(level)
    vlog.addHandler(fileHandler)

    return vlog

# def Setlog(logfolder = 'Log/', logname='system'):

#     os.makedirs(logfolder, exist_ok = True) 
#     logging.basicConfig(
#         filename=logfolder+logname+'.log',
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S'
#     )
#     logger = logging.getLogger(logname)
#     file_handler = logging.FileHandler(logname+'.log')
#     logger.addHandler(file_handler) 
#     return logger