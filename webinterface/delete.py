from django.http import JsonResponse

class Deleteprocess:
    def __init__(self, path, row):
        self.path = path
        self.row = int(row)

    def area(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def zone(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")  
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def owner(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")   
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def bus(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines) 

    def machine(self):
        print(self.row)
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row*4,"\n")
        lines.insert(self.row*4,"\n")    
        lines.insert(self.row*4,"\n")
        lines.insert(self.row*4,"\n")        
        del lines[(self.row+1)*4:(self.row+1)*4+4]
        print(lines)
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def load(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)    

    def branch(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()

        lines.insert(self.row*3,"\n")    
        lines.insert(self.row*3,"\n")
        lines.insert(self.row*3,"\n")

        del lines[(self.row+1)*3:(self.row+1)*3+3]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def twowinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()

        lines.insert(self.row*3,"\n")    
        lines.insert(self.row*3,"\n")
        lines.insert(self.row*3,"\n")

        del lines[(self.row+1)*3:(self.row+1)*3+3]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)  

    def threewinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()

        lines.insert(self.row*3,"\n")    
        lines.insert(self.row*3,"\n")
        lines.insert(self.row*3,"\n")

        del lines[(self.row+1)*3:(self.row+1)*3+3]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)                       

    def threewinding_winding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)  

class DeleteShowprocess:
    def __init__(self, path, row):
        self.path = path
        self.row = int(row)

    def area(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def zone(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")  
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def owner(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")   
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def bus(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines) 

    def machine(self):
        print(self.row)
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        print(lines)
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def load(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)    

    def branch(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)

    def twowinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)            

    def threewinding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)            
 
    def threewinding_winding(self):
        with  open(self.path,"r",encoding='ansi') as f:
            lines = f.readlines()
        lines.insert(self.row,"\n")    
        del lines[self.row+1]
        with open(self.path,"w",encoding='ansi') as f:
            f.writelines(lines)    

class DeleteComponet:
    def __init__(self, writedata_path, showdata_path, row):
        self.writedata_path = writedata_path
        self.showdata_path = showdata_path
        self.row = row
    

    def area(self):
        Deleteprocess(path = self.writedata_path, row = self.row).area()
        DeleteShowprocess(path = self.showdata_path, row = self.row).area()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'area 刪除成功'])
                })

    def zone(self):
        Deleteprocess(path = self.writedata_path, row = self.row).zone()
        DeleteShowprocess(path = self.showdata_path, row = self.row).zone()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'zone 刪除成功'])
                })  

    def owner(self):
        Deleteprocess(path = self.writedata_path, row = self.row).owner()
        DeleteShowprocess(path = self.showdata_path, row = self.row).owner()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'owner 刪除成功'])
                })   

    def bus(self):
        Deleteprocess(path = self.writedata_path, row = self.row).bus()
        DeleteShowprocess(path = self.showdata_path, row = self.row).bus()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'bus 刪除成功'])
                })  

    def machine(self):
        Deleteprocess(path = self.writedata_path, row = self.row).machine()
        DeleteShowprocess(path = self.showdata_path, row = self.row).machine()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'machine 刪除成功'])
                })   

    def load(self):
        Deleteprocess(path = self.writedata_path, row = self.row).load()
        DeleteShowprocess(path = self.showdata_path, row = self.row).load()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'load 刪除成功'])
                })      

    def branch(self):
        Deleteprocess(path = self.writedata_path, row = self.row).branch()
        DeleteShowprocess(path = self.showdata_path, row = self.row).branch()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'branch 刪除成功'])
                })     

    def twowinding(self):
        Deleteprocess(path = self.writedata_path, row = self.row).twowinding()
        DeleteShowprocess(path = self.showdata_path, row = self.row).twowinding()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'twowinding 刪除成功'])
                })        

    def threewinding(self):
        Deleteprocess(path = self.writedata_path, row = self.row).threewinding()
        DeleteShowprocess(path = self.showdata_path, row = self.row).threewinding()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'threewinding 刪除成功'])
                })     

    def threewinding_winding(self):
        Deleteprocess(path = self.writedata_path, row = self.row).threewinding_winding()
        DeleteShowprocess(path = self.showdata_path, row = self.row).threewinding_winding()
       
        return  JsonResponse({
                    'status': 'success',
                    'message': '<br>'.join([f'threewinding_winding 刪除成功'])
                })                                                                    

