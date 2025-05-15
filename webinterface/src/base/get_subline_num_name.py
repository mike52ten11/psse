import numpy as np
import sys,os
import re

def writeFile(filename, data, encodingtype='ansi'):  
    with open(filename, "w", encoding=encodingtype) as file:
        file.write(data)


def subline_345kv_logic(zonenum, areanum, allbus):

    subline_345kv_num = {3068, 3069, 3070, 3071}
    area_set = set()
    zone_set = set()

    if zonenum==[]:
        for area in areanum:

            index = np.where(allbus["areanum"]==area)
            area_set.update(set( allbus["num"][index].astype(int) ).intersection( subline_345kv_num ))
        
        return area_set

    elif areanum==[]:
        for zone in zonenum:

            index = np.where(allbus["zonenum"]==zone)
            zone_set.update(set( allbus["num"][index].astype(int) ).intersection( subline_345kv_num ))
        
        return zone_set
     
    else:

        for area in areanum:

            index = np.where(allbus["areanum"]==area)
            area_set.update(set( allbus["num"][index].astype(int) ).intersection( subline_345kv_num ))
        
        for zone in zonenum:

            index = np.where(allbus["zonenum"]==zone)
            zone_set.update(set( allbus["num"][index].astype(int) ).intersection( subline_345kv_num ))        
    
        return area_set.intersection(zone_set)
       
def subline_161kv_logic(zonenum, areanum, allbus):

    patternlist = [r'分',r'A',r'B']
    other_conditionlist = [r'1',r'2']
    area_set = set()
    zone_set = set()

    if zonenum==[]:
        for area in areanum:
            
            index = np.where(allbus["areanum"]==area)
            
            for busnumindex in index[0]:
                busnum = allbus["num"][busnumindex].astype(int)
                
                if (busnum>7269 or busnum==7269) and (busnum<7999 or busnum==7999):
                    busname = allbus["name"][busnumindex]
                    for other_condition in other_conditionlist:
                        if re.search(other_condition, busname):
                            area_set.add(busnum)

        return area_set

    elif areanum==[]:
        for zone in zonenum:

            index = np.where(allbus["zonenum"]==zone)            
            for busnumindex in index[0]:
                
                busnum = allbus["num"][busnumindex].astype(int)
                
                if (busnum>7269 or busnum==7269) and (busnum<7999 or busnum==7999):
                    busname = allbus["name"][busnumindex]
                    for other_condition in other_conditionlist:
                        if re.search(other_condition, busname):
                            zone_set.add(busnum)
        return zone_set
     
    else:
        all_busname = allbus["name"][0]
        for area in areanum:

            index = np.where(allbus["areanum"]==area)
            for busnumindex in index:
                for busnum in allbus["num"][busnumindex].astype(int):
                    if (busnum>7269 or busnum==7269) and (busnum<7999 or busnum==7999):
                        busname = all_busname[busnumindex]
                        for other_condition in other_conditionlist:
                            if re.search(other_condition, busname):
                                area_set.add(busnum)

        for zone in zonenum:

            index = np.where(allbus["zonenum"]==zone)            
            for busnumindex in index:
                busnum = allbus["num"][busnumindex].astype(int)
                if (busnum>7269 or busnum==7269) and (busnum<7999 or busnum==7999):
                    busname = allbus["name"][busnumindex]
                    for other_condition in other_conditionlist:
                        if re.search(other_condition, busname):
                            zone_set.add(busnum)

        return area_set.intersection(zone_set)

        
def create_subline_npz(target,zonenum, areanum, minbasekv, maxbasekv, filterfile):

    os.makedirs(target,exist_ok=True)
    busnum_and_name_from_filterfile = np.load(filterfile)
    
    if maxbasekv==345.0:
        subline_busnumber_set = subline_345kv_logic(zonenum = zonenum, areanum = areanum, allbus = busnum_and_name_from_filterfile)
    else:
        subline_busnumber_set = subline_161kv_logic(zonenum = zonenum, areanum = areanum, allbus = busnum_and_name_from_filterfile)
    # zonenum zonename areanum  areaname 

    subline_busname_list = []
    
    if subline_busnumber_set:
            
        for busnum in subline_busnumber_set:
            index = np.where(busnum_and_name_from_filterfile["num"].astype(int)==busnum)
            subline_busname_list.append(busnum_and_name_from_filterfile["name"][index][0])
        
        np.savez(f'{target}/分歧線的BusName與BusNum.npz', busname=subline_busname_list
                        , busnum = list(subline_busnumber_set)) 

    else:
        np.savez(f'{target}/分歧線的BusName與BusNum.npz', busname=subline_busname_list
                        , busnum = [])
    print(subline_busname_list)

    # logger_filter_busname.info(f'FUNCTION:psspy.bsys(1,1,[ {minbasekv}, {maxbasekv}],0,[],0,[],0,[],1,{zonenum})，MESSAGE:找到的分歧線{name}')

    writeFile(f'{target}/分歧線的BusName.txt', ','.join(subline_busname_list))



if __name__ == '__main__':

    target = f"../Data/User/AnonymousUser/PowerFlowSub/122P/161KV_N-1/close/area=,zone=43"
    zonenum = ['43']
    areanum = []
    minbasekv = 161.0
    maxbasekv = 161.0
    filterfile = f'../Data/User/AnonymousUser/filter/PowerFlow/bus/bus_122P.npz'
    create_subline_npz  (   target = target, 
                            zonenum = zonenum, 
                            areanum = areanum, 
                            minbasekv = minbasekv, 
                            maxbasekv = maxbasekv, 
                            filterfile = filterfile
                        )



    



