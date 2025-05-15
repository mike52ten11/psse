    
def Load_PSSE_Path():    
    import configparser
    import sys
    config = configparser.ConfigParser()
    config.read('webinterface/src/Config/config.ini')
    # r"""C:\Program Files\PTI\PSSE35\35.3\PSSPY37"""
    pssepy_PATH=config[r"PSSE"][r"psse"]
    sys.path.append(pssepy_PATH)
    