from django.http import JsonResponse

class EditProcess:
    def __init__(self, path, row, edit_data):
        self.path = path
        self.row = int(row)
        self.edit_data = edit_data

    def area(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def zone(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def owner(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def bus(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines) 

    def machine(self):
        print(self.row)
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row*4,self.edit_data)
        print(lines) 
        print('len(lines)-->', len(lines))
        del lines[self.row*4+1: self.row*4+5]
        print(lines)
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def load(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)    

    def branch(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert((self.row)*3,self.edit_data)   
        print(lines) 
        del lines[self.row*3+1:self.row*3+4]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def twowinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert((self.row)*3,self.edit_data)   
        print(lines) 
        del lines[self.row*3+1:self.row*3+4]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)      

    def threewinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert((self.row)*3,self.edit_data)   
        print(lines) 
        del lines[self.row*3+1:self.row*3+4]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)                    

    def threewinding_winding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines) 

class EditShowProcess:
    def __init__(self, path, row, edit_data):
        self.path = path
        self.row = int(row)
        self.edit_data = edit_data

    def area(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def zone(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def owner(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def bus(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines) 

    def machine(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def load(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines) 

    def branch(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def twowinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)
            

    def threewinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)
            
    def threewinding_winding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,self.edit_data)    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

class EditComponet:
    def __init__(self, writedata_path, showdata_path, row, edit_data_for_write, edit_data_for_show):
        self.writedata_path = writedata_path
        self.showdata_path = showdata_path
        self.row = row
        self.edit_data_for_write = edit_data_for_write
        self.edit_data_for_show = edit_data_for_show
    

    def area(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).area()

        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).area()       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'area 編輯成功'])
                })        
    def zone(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).zone()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).zone()       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'zone 編輯成功'])
                })  

    def owner(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).owner()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).owner()       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'owner 編輯成功'])
                })   

    def bus(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).bus()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).bus()       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'bus 編輯成功'])
                })  

    def machine(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).machine()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).machine()      
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'machine 編輯成功'])
                })   

    def load(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).load()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).load()       
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'load 編輯成功'])
                })

    def branch(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).branch()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).branch()       
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'branch 編輯成功'])
                }) 

    def twowinding(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).twowinding()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).twowinding()       
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'twowinding 編輯成功'])
                })                                 

    def threewinding(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).threewinding()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).threewinding()       
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'threewinding 編輯成功'])
                })    

    def threewinding_winding(self):
        EditProcess(path = self.writedata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_write
                    ).threewinding_winding()
        EditShowProcess(path = self.showdata_path
                    , row = self.row
                    , edit_data=self.edit_data_for_show
                    ).threewinding_winding()       
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'threewinding_winding 編輯成功'])
                })    
                              