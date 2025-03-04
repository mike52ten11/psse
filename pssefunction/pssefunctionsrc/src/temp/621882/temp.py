
# -*- coding: utf-8 -*-   


import sys, os
import configparser
import sys
print('現在位置-->',os.getcwd())


import numpy as np


try:    
    pssepy_PATH = os.environ.get('PSSE') 
    sys.path.append(pssepy_PATH)     
    import psse35
    # psse35.set_minor(3)
    import psspy
    psspy.psseinit()
    # import pssexcel
    import argparse
    import logging
except Exception as error: 
    print('error')
   
    raise ImportError(error)    


  
os.makedirs('../Data/User/621882/Dynamic/115P',exist_ok=True)





Source_rawFilename = f"../Data/User/621882/SavFile/Powerflow/115P.sav"
print(Source_rawFilename)


psspy.case(r"%s" %Source_rawFilename)

a = psspy.fnsl([1,0,0,1,1,1,-1,0])#第一次    
b = psspy.fnsl([1,0,0,1,1,0,0,0])#第二次[1,0,0,1,1,0,0,0]
c = psspy.fnsl([1,0,0,1,1,0,0,0])
# convert
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])
# ORDR
psspy.ordr(0)
# FACT
psspy.fact()
psspy.fact()
# TYSL
psspy.tysl(0)

psspy.purgmac(8442,'1')
psspy.purgmac(8443,'1')
psspy.purgmac(8444,'1')
psspy.purgmac(9137,'1')
psspy.purgmac(9138,'1')
psspy.purgmac(9586,'1')
psspy.purgmac(9587,'1')
psspy.purgmac(9588,'1')
psspy.purgmac(9589,'1')
psspy.purgmac(9594,'1')
psspy.purgmac(9596,'1')
psspy.purgmac(9597,'1')
psspy.purgmac(9598,'1')
psspy.purgmac(9599,'1')
psspy.purgmac(9600,'1')
psspy.purgmac(9602,'1')
psspy.purgmac(9603,'1')
psspy.purgmac(9604,'1')
psspy.purgmac(9147,'1')
psspy.shunt_data(9137,'12',1,[-23.78,0.0])
psspy.shunt_data(9138,'12',1,[-1,0.0])
psspy.shunt_data(9586,'12',1,[-25.0,0.0])
psspy.shunt_data(9587,'12',1,[-25.0,0.0])
psspy.shunt_data(9588,'12',1,[-25.0,0.0])
psspy.shunt_data(9589,'12',1,[-85.0,0.0])
psspy.shunt_data(9594,'12',1,[-12.7,0.0])
psspy.shunt_data(9596,'12',1,[-35.18,0.0])
psspy.shunt_data(9597,'12',1,[-35.18,0.0])
psspy.shunt_data(9598,'12',1,[-35.18,0.0])
psspy.shunt_data(9599,'12',1,[-35.18,0.0])
psspy.shunt_data(9600,'12',1,[-35.18,0.0])
psspy.shunt_data(9602,'12',1,[-5.6,0.0])
psspy.shunt_data(9603,'12',1,[-11.9,0.0])
psspy.shunt_data(9604,'12',1,[-2.4,0.0])
psspy.shunt_data(9147,'12',1,[-32,0.0])

psspy.dyre_new([1,1,1,1],f'../Data/User/621882/Dynamic/115P/P-11109.dyr',f"../Data/User/621882/Dynamic/115P/CC2",f"../Data/User/621882/Dynamic/115P/CT2",
f"../Data/User/621882/Dynamic/115P/CP2")
# 匯dll
psspy.addmodellibrary(f'../Data/User/621882/Dynamic/115P/dsusr35.dll')
# 調parameter
psspy.dynamics_solution_param_2([25,0,0,18807,7594,2461,1418,1],[1.000000,0.0001, 0.000333,0.033333,0.05,0.11667,1.000000,0.0005])
#建立out檔
psspy.change_channel_out_file(f"../Data/User/621882/Dynamic/115P/115P")
psspy.machine_array_channel([-1,1,11],'1','')
      
# # initial、Run to 1.0 sec
psspy.strt_2([0,0],f"../Data/User/621882/Dynamic/115P/115P.out")
psspy.run(0, 1.0,5,5,5)
# 對1500進行Bus fault
psspy.dist_3phase_bus_fault(230,0,1,0.0,[0.0,-0.2E+10])
# Run to 1.0667 sec
psspy.change_channel_out_file(f"../Data/User/621882/Dynamic/115P/115P.out")
psspy.run(0, 1.0665,5,5,5)
psspy.dist_branch_trip(230,220,'1')

# Run to 1.075 sec
psspy.change_channel_out_file(f"../Data/User/621882/Dynamic/115P/115P.out")
psspy.run(0, 1.705,5,5,5)
# Clear fault
psspy.dist_clear_fault(1)
# Run to 15 sec
psspy.run(0, 15,5,5,5)    
