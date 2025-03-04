

from ..src.write_to_save import write_area

def writeFile(filename, data):  
    f = open(filename, "a")  
    f.write(data)  
    f.close()  

class WriteData:

    def __init__(self,params):

        self.savfiles = params.get('savfiles')    
        self.savfile_dir = params.get('savfile_dir')
        self.target_dir = params.get('target_dir')
        self.idvfile_path = params.get('idvfile_path')
        self.args = params.get('args')

    def use_idv_function_to_write_data(self): 
        print('self.savfiles -->',self.savfiles )
        print('self.savfile_dir -->',self.savfile_dir )
        print('self.idvfile -->',self.idvfile_dir )
        print('self.args -->',self.args )
        
        results = write_area(self.savfiles
                            , self.savfile_dir
                            ,self.target_dir 
                            ,self.idvfile_dir
                            ,self.args
                            )
        print(results)            
        return results            



