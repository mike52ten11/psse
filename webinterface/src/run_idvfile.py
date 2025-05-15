


import sys, os   
pssepy_PATH = os.environ.get('PSSE') 
sys.path.append(pssepy_PATH)    
import psse35
# psse35.set_minor(3)
import psspy
psspy.psseinit()
# import pssexcel
import argparse
import logging



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-idvfile', '--idv_file', default='User/621882', type=str, help='idv檔路徑')
    args = parser.parse_args()
    
    idvfile = args.idv_file
    psspy.runrspnsfile(f'{idvfile}')