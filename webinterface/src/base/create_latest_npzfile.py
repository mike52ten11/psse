import shutil
import numpy as np
from .search import SearchFiles

def update_and_save_npz(original_data, new_data, save_path):
    # 將原始資料和新資料轉為 NumPy 陣列
    orig_num = np.array(original_data["num"])
    orig_name = np.array(original_data["name"])
    orig_zonenum = np.array(original_data["zonenum"])
    orig_zonename = np.array(original_data["zonename"])

    new_num = np.array(new_data["num"])
    new_name = np.array(new_data["name"])
    new_zonenum = np.array(new_data["zonenum"])
    new_zonename = np.array(new_data["zonename"])

    # 使用 NumPy 的結構化陣列來管理資料
    dtype = [('num', orig_num.dtype), ('name', orig_name.dtype), 
             ('zonenum', orig_zonenum.dtype), ('zonename', orig_zonename.dtype)]
    
    # 將原始資料和新資料合併為結構化陣列
    orig_structured = np.array(list(zip(orig_num, orig_name, orig_zonenum, orig_zonename)), dtype=dtype)
    new_structured = np.array(list(zip(new_num, new_name, new_zonenum, new_zonename)), dtype=dtype)

    # 合併資料並根據 num 去重（保留新資料中的值）
    combined = np.concatenate([orig_structured, new_structured])
    _, unique_idx = np.unique(combined['num'], return_index=True)
    unique_data = combined[np.sort(unique_idx)]

    # 分離出各欄位
    final_num = unique_data['num']
    final_name = unique_data['name']
    final_zonenum = unique_data['zonenum']
    final_zonename = unique_data['zonename']

    # 保存為 .npz
    np.savez(save_path, num=final_num, name=final_name, zonenum=final_zonenum, zonename=final_zonename)

class CreateLatestNpzfile:
    def __init__(self, filter_dir):
        self.filter_dir = filter_dir

    def area_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        Num, Name = user_data_of_labeltype["num"], user_data_of_labeltype['name']
        mapping = dict(zip(Num, Name))


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            
            mapping.update(dict(zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'])))     
            


        Num = np.array(list(mapping.keys()))
        
        Name = np.array(list(mapping.values()))
        np.savez(f'{self.filter_dir}/latest.npz', name=Name, num=Num)        
        data_of_labeltype = [
            {'num': num, 'name': name}
            for num, name in zip(Num, Name)
        ]        
        
        return data_of_labeltype


    def zone_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        Num, Name = user_data_of_labeltype["num"], user_data_of_labeltype['name']
        mapping = dict(zip(Num, Name))


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            
            mapping.update(dict(zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'])))     
            


        Num = np.array(list(mapping.keys()))
        
        Name = np.array(list(mapping.values()))
        np.savez(f'{self.filter_dir}/latest.npz', name=Name, num=Num)        
        data_of_labeltype = [
            {'num': num, 'name': name}
            for num, name in zip(Num, Name)
        ]        
        
        return data_of_labeltype  

    def owner_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        Num, Name = user_data_of_labeltype["num"], user_data_of_labeltype['name']
        mapping = dict(zip(Num, Name))


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            
            mapping.update(dict(zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'])))     
            


        Num = np.array(list(mapping.keys()))
        
        Name = np.array(list(mapping.values()))
        np.savez(f'{self.filter_dir}/latest.npz', name=Name, num=Num)        
        data_of_labeltype = [
            {'num': num, 'name': name}
            for num, name in zip(Num, Name)
        ]        
        
        return data_of_labeltype 

    def bus_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
        if len(filterfiles)>1:
            for filterfile_name in filterfiles[1:len(filterfiles)]:
                
                new_data = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
                update_and_save_npz(user_data_of_labeltype, new_data, f'{self.filter_dir}/latest.npz')
            
            np.load(f"{self.filter_dir}/latest.npz")
            data_of_labeltype = [
                        {'num': int(num), 'name': name, "zonenum":int(zonenum), "zonename":zonename}
                        for num, name, zonenum,zonename in zip(filtervalue["num"]
                                        , filtervalue['name']
                                        ,filtervalue['zonenum']
                                        ,filtervalue['zonename'])
                    ]               
            
            return data_of_labeltype 
                           
        else:
            shutil.copyfile(f"{self.filter_dir}/{filterfile_name}.npz", f"{self.filter_dir}/latest.npz")


    def machine_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
        
        
        Num, Name, machine_id = user_data_of_labeltype["num"], user_data_of_labeltype['name'], user_data_of_labeltype['machine_id']
        
        mapping = {}
        for num, name, id_val in zip(Num, Name, machine_id):
            mapping[num] = [name, id_val]


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            new_entries = {num: [name, id_val] for num, name, id_val in zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'], user_data_of_labeltype['machine_id'])}
            
            mapping.update(new_entries)   
            


        Num = np.array(list(mapping.keys()))
        Name, machine_id = zip(*list(mapping.values()))
        Name = np.array(Name)
        machine_id = np.array(machine_id)

        np.savez(f'{self.filter_dir}/latest.npz', name=Name, num=Num, machine_id=machine_id)        
        data_of_labeltype = [
            {'num': num, 'name': name, 'machine_id': machine_id}
            for num, name, machine_id in zip(Num, Name, machine_id)
        ]        
        
        return data_of_labeltype

    def load_data(self):    
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        Num, Name = user_data_of_labeltype["num"], user_data_of_labeltype['name']
        mapping = dict(zip(Num, Name))


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            
            mapping.update(dict(zip(user_data_of_labeltype['num'], user_data_of_labeltype['name'])))     
            


        Num = np.array(list(mapping.keys()))
        
        Name = np.array(list(mapping.values()))
        np.savez(f'{self.filter_dir}/latest.npz', name=Name, num=Num)        
        data_of_labeltype = [
            {'num': num, 'name': name}
            for num, name in zip(Num, Name)
        ]        
        
        return data_of_labeltype 

    def branch_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        fromNum, fromName, toNum, toName, branchid = user_data_of_labeltype["fromnum"], user_data_of_labeltype['fromname'], user_data_of_labeltype['tonum'], user_data_of_labeltype['toname'], user_data_of_labeltype['id']
        mapping = {}
        for fromnum, fromname, tonum, toname, id_val in zip(fromNum, fromName, toNum, toName, branchid):
            mapping[fromnum] = [fromname, tonum, toname, id_val]


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            new_entries = {fromnum: [fromname, tonum, toname, id_val] for fromnum, fromname, tonum, toname, id_val in zip(user_data_of_labeltype['fromnum'], user_data_of_labeltype['fromname'], user_data_of_labeltype['tonum'], user_data_of_labeltype['toname'], user_data_of_labeltype['id'])}
            mapping.update(new_entries)     

            


        fromNum = np.array(list(mapping.keys()))
        
        
        fromName, toNum, toName, branchid = zip(*list(mapping.values()))
        fromName = np.array(fromName)
        toNum = np.array(toNum)
        toName = np.array(toName)
        branchid = np.array(branchid)

        np.savez(f'{self.filter_dir}/latest.npz', fromname=fromName, fromnum=fromNum, tonum=toNum, toname=toName, id=branchid)        
        data_of_labeltype = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname,'id':id}
                        for fromnum, fromname, tonum, toname,id in zip(fromNum,fromName , toNum, toName, branchid)
                    ]       
        
        return data_of_labeltype         

    def two_winding_transformer_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        fromNum, fromName, toNum, toName, transformerid, transformer_Name = user_data_of_labeltype["fromnum"], user_data_of_labeltype['fromname'], user_data_of_labeltype['tonum'], user_data_of_labeltype['toname'], user_data_of_labeltype['transformer_id'], user_data_of_labeltype['transformer_name']  
        mapping = {}
        for fromnum, fromname, tonum, toname, id_val, transformer_name in zip(fromNum, fromName, toNum, toName, transformerid, transformer_Name):
            mapping[f"{fromnum},{tonum}"] = [fromname,  toname, id_val, transformer_name]


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            new_entries = {f"{fromnum},{tonum}": [fromname,  toname, id_val, transformer_name] for fromnum, fromname, tonum, toname, id_val, transformer_name in zip(user_data_of_labeltype['fromnum'], user_data_of_labeltype['fromname'], user_data_of_labeltype['tonum'], user_data_of_labeltype['toname'], user_data_of_labeltype['transformer_id'],user_data_of_labeltype['transformer_name'])}
            mapping.update(new_entries)     

            


        fromNum_and_tonum = np.array(list(mapping.keys()))
        fromNum = [int(i.split(',')[0]) for i in fromNum_and_tonum]
        toNum  = [int(i.split(',')[1]) for i in fromNum_and_tonum]

        fromName, toName, transformerID, transformer_Name = zip(*list(mapping.values()))
        fromName = np.array(fromName)
        toName = np.array(toName)
        transformer_Name = np.array(transformer_Name)
        transformerID = np.array(transformerID)

        np.savez(f'{self.filter_dir}/latest.npz', fromname=fromName, fromnum=fromNum, tonum=toNum, toname=toName, transformer_id=transformerID, transformer_name=transformer_Name)        
        data_of_labeltype = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname,'transformer_id':transformerid,"transformer_name":transformer_name}
                        for fromnum, fromname, tonum, toname, transformerid, transformer_name in zip(fromNum,fromName , toNum, toName, transformerID, transformer_Name)
                    ]       
        
        return data_of_labeltype     

    def three_winding_transformer_data(self):
        filterfiles = SearchFiles({"sourcedir":self.filter_dir}).search_npzfiles()
        filterfile_name = filterfiles[0]
        user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")

        
        fromNum, fromName, toNum, toName, lastNum, lastName, transformerid, transformer_name = user_data_of_labeltype["fromnum"], user_data_of_labeltype['fromname'], user_data_of_labeltype['tonum'], user_data_of_labeltype['toname'], user_data_of_labeltype['lastnum'], user_data_of_labeltype['lastname'], user_data_of_labeltype['transformer_id'], user_data_of_labeltype['transformer_name'] 
        mapping = {}
        for fromnum, fromname, tonum, toname, lastnum, lastname, id_val, transformer_name in zip(fromNum, fromName, toNum, toName, lastNum, lastName, transformerid, transformer_name):
            mapping[fromnum] = [fromname, tonum, toname, lastnum, lastname, id_val, transformer_name]


        for filterfile_name in filterfiles[1:len(filterfiles)]:
            
            user_data_of_labeltype = np.load(f"{self.filter_dir}/{filterfile_name}.npz")
            new_entries = {fromnum: [fromname, tonum, toname, lastnum, lastname, id_val, transformer_name] for fromnum, fromname, tonum, toname, lastnum, lastname, id_val, transformer_name in zip(user_data_of_labeltype['fromnum'], user_data_of_labeltype['fromname'], user_data_of_labeltype['tonum'], user_data_of_labeltype['toname'], user_data_of_labeltype['lastnum'], user_data_of_labeltype['lastname'], user_data_of_labeltype['transformer_id'], user_data_of_labeltype['transformer_name'] )}
            mapping.update(new_entries)     

            


        fromNum = np.array(list(mapping.keys()))
        
        
        fromName, toNum, toName, lastNum, lastName, transformerID, transformer_Name = zip(*list(mapping.values()))
        fromName = np.array(fromName)
        toNum = np.array(toNum)
        toName = np.array(toName)
        lastNum = np.array(lastNum)
        lastName = np.array(lastName)
        transformer_Name = np.array(transformer_Name)
        transformerID = np.array(transformerID)

        np.savez(f'{self.filter_dir}/latest.npz', fromname=fromName, fromnum=fromNum, tonum=toNum, toname=toName, lastnum = lastNum, lastname = lastName, transformer_id=transformerID, transformer_name=transformer_Name)        
        data_of_labeltype = [
                        {'fromnum': int(fromnum), 'fromname': fromname,'tonum':int(tonum), 'toname':toname, 'lastnum':int(lastnum), 'lastname':lastname,'transformer_id':transformerid,'transformer_name':transformer_name}
                        for fromnum, fromname, tonum, toname, lastnum, lastname, transformerid, transformer_name in zip(fromNum,fromName , toNum, toName,lastNum, lastName,transformerID,transformer_Name)
                    ]       
        
        return data_of_labeltype            