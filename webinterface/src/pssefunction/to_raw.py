# File:"C:\psseweb\to_raw.py", generated on THU, FEB 13 2025   9:36, PSS(R)E release 35.01.00


import sys, os


def ParseConfig():
    import argparse
    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-SavF', '--Sav_FileName', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-sourcesavfile', '--savfiledir', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-TargetDir', '--target_dir', default="User/621882/", type=str, help='檔案來源資料夾路徑')

    args = parser.parse_args()

    savfile_name = args.Sav_FileName
    savfiledir = args.savfiledir
    target_dir = args.target_dir
    source_savfile = f"{savfiledir}/{savfile_name}.sav"
    targetfile = f"{target_dir}/{savfile_name}.raw"

    return source_savfile, targetfile


if __name__ == '__main__':

    source_savfile, targetfile = ParseConfig()
    
    pssepy_PATH = os.environ.get('PSSE') 
    sys.path.append(pssepy_PATH)            
    import psse35
    # psse35.set_minor(3)
    import psspy
    psspy.psseinit() 
    psspy.case(r"%s" %source_savfile)    
    psspy.rawd_2(0,1,[1,1,1,0,0,0,0],0,r"%s" %targetfile)