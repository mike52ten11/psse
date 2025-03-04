

from .src import fileprocess
import os
class run:

    def __init__(self, args):
        self.user = args['username']
        self.userfolder = f"../Data/User/{self.user}"
        self.yearlist = args['yearlist']

    def idv(self):
        message = []
        for year in self.yearlist:
            args =  f" --Source_SavFileName {self.userfolder}/SavFile/{year}.sav"\
                    f" --Target_SavFileName {self.userfolder}/SavFile/{year}.sav"\
                    f" --User_Folder {self.userfolder}"\
                    f" --User_name {self.user}"\
                    f" --IDV_Path {self.userfolder}/excute_idvfile/temp.idv"
            
            print(os.getcwd())
            cmd = fileprocess.run_pyfile_by_execmd(python_location='python'
                                        ,pyfile='webinterface/src/runidv.py'
                                        ,args=args)
            print(cmd)
            result = fileprocess.execCmd(cmd)
            # print(result)
            if result['error']:
                message.append(f'{year} 失敗')
            else:
                message.append(f'{year} 成功')    
        return {'messages':['，'.join(message)]}    

    def powerflow(self):    
        return_of_RUN_PowerFlow = run_powerflow.RUN_PowerFlow(username=username
                                                            ,yearlist=yearlist
                                                            ,convergence_thread_hold=convergence_thread_hold
                                                            
                                                            ,zone=zone
                                                            ,minbasekv=minbasekv
                                                            ,maxbasekv=maxbasekv
                                                            ,confile_type=confile_type)
