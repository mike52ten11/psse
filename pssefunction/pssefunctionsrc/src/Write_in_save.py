# -*- coding: utf-8 -*-
from py_to_idv  import  *
import numpy as np

def Write_in_save(Source_File,target_file,user,labeltype,idvpath,savefilename,args):
    # args = args[0]
    logger.info('args = %s', args) 
    logger.info(' type(args) = %s', type(args))
    if labeltype=="BUS":
        BUS_Number = int(args.get('BUSNumber'))

        Code = int(args.get('Code'))
        Area_Num = int(args.get('AreaNum'))
        Zone_Num = int(args.get('ZoneNum'))
        Owner_Num = int(args.get('OwnerNum'))
        
        Base_kV = float(args.get('BasekV'))
        Voltage = float(args.get('Voltage'))
        Angel = float(args.get('Angel'))
        Normal_Vmax = float(args.get('NormalVmax'))
        Normal_Vmin = float(args.get('NormalVmin'))
        Emergency_Vmax = float(args.get('EmergencyVmax'))
        Emergency_Vmin = float(args.get('EmergencyVmin'))

        

        BUS_Name = args.get('BUSName')

        psspy.case(r"%s" %Source_File) 
        ierr, buses = psspy.abusint(-1,2,string='NUMBER')
        # if BUS_Number in buses[0]:
        #     logger.error('repeat')
        #     return 'repeat'           
        logger.info('read savfile from Source_File sucess')
        psspy.bus_data_4(   BUS_Number #Bus Number
                            ,0 #固定值
                            ,[Code,Area_Num,Zone_Num,Owner_Num]#[Code,Area Num, Zone Num,Owner Num, ] #[_i,_i,_i,_i]  _i ==> int
                            ,[Base_kV,Voltage,Angel,Normal_Vmax,Normal_Vmin,Emergency_Vmax,Emergency_Vmin]
                            #[Base kV ,Voltage (pu),Angle (deg)Normal Vmax (pu),	Normal Vmin (pu),Emergency Vmax (pu),Emergency Vmin (pu)] #[_f,_f,_f,_f,_f,_f,_f] _f ==> float
                            ,BUS_Name)#Bus Name #_s _s==>string                      
        logger.info('write into savfile sucess')

        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')

        psspycommand =  {   'function':'bus_data_4',
                            'data':[str(BUS_Number), 
                                    '0',
                                    str(Code),str(Area_Num),str(Zone_Num),str(Owner_Num),
                                    str(Base_kV),str(Voltage),str(Angel),str(Normal_Vmax),str(Normal_Vmin),str(Emergency_Vmax),str(Emergency_Vmin),
                                    "'"+str(BUS_Name)+"'"],
                            'labeltype':'bus'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)
        logger.info('conver to idv sucess')



    elif labeltype=="Machine":
        BUS_Number = int(args.get('BusNumber'))
        ID = args.get('ID')
        # ID = '1'
        MachineControlMode = int(args.get('MachineControlMode'))
        BASE = int(args.get('BASE'))
        Pgen = float(args.get('Pgen'))
        Qgen = float(args.get('Qgen'))
        
        Qmax = float(args.get('Qmax'))
        Qmin = float(args.get('Qmin'))
        Pmax = float(args.get('Pmax'))
        Pmin = float(args.get('Pmin'))
        Mbase = float(args.get('Mbase'))
        RSource = float(args.get('RSource'))
        XSource = float(args.get('XSource'))

        #seq machine
        R = float(args.get('R'))        
        SubtransientX = float(args.get('SubtransientX'))
        RNegative = float(args.get('RNegative'))
        XNegative = float(args.get('XNegative'))
        RZero = float(args.get('RZero'))
        XZero = float(args.get('XZero'))
        TransientX = float(args.get('TransientX'))
        SynchronousX = float(args.get('SynchronousX'))


        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.plant_data_4(BUS_Number,0,[0,0],[1.00,100.00])
        psspy.machine_data_4(BUS_Number
                            ,ID
                            ,[1,1,0,0,0,MachineControlMode,BASE]#[1,Owner2,Owner3,Owner4,Owner5,MachineControlMode,BASE]
                            ,[ Pgen, Qgen, Qmax, Qmin, Pmax, Pmin, Mbase, RSource, XSource
                                ,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8]
                                #,RTrain,XTrain,Gentap,2.4,2.5,2.6,2.7,2.8
                            ,"")
        psspy.seq_machine_data_4(BUS_Number
                                ,ID
                                ,0
                                ,[ R, SubtransientX, RNegative, XNegative,RZero, XZero, TransientX, SynchronousX
                                ,0.0,0.0,0.0])
        psspycommand =  {   'function':'machine_data_4',
                            'data':[str(BUS_Number)
                                    ,str(ID)
                                    ,'0','1','0','0','0',str(MachineControlMode),str(BASE)
                                    ,str(Pgen),str(Qgen),str(Qmax),str(Qmin),str(Pmax),str(Pmin),str(Mbase),str(RSource),str(XSource)
                                    ,"","","","","","","",""
                                    ,""],
                            'labeltype':'machine'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)
        psspycommand =  {   'function':'seq_machine_data_4',
                            'data':[str(BUS_Number)
                                    ,str(ID)
                                    ,'0'
                                    ,str(R),str(SubtransientX),str(RNegative),str(XNegative),str(RZero),str(XZero),str(TransientX),str(SynchronousX)
                                    ,"0.0","0.0","0.0"],
                            'labeltype':'seq_machine'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)        
        logger.info('write into savfile sucess')

        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')

    elif labeltype=="LOAD":
        
        filter_data = np.load(f"User/{user}/filter/load/load_{savefilename}.npz")

        Bus_Number = int(args.get('BusNumber'))
        ID = filter_data['id'][np.where(filter_data['num']==Bus_Number)]
        logger.info('LOAD ID = %s',ID)
        logger.info('LOAD ID = %s',type(ID))
        if ID.size == 0:
            ID = '1'
            logger.info('LOAD ID = %s',ID)
        else:    
            logger.info('LOAD ID = %s','else')
            ID = ID[-1]
            ID = str(int(ID)+1)

        # ID = args.get('ID')
        Pload = float(args.get('Pload'))
        Qload = float(args.get('Qload'))

        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.load_data_6(Bus_Number
                        ,ID
                        ,[1,0,0,0,1,0,0]
                        ,[ Pload, Qload,0.0,0.0,0.0,0.0,0.0,0.0],"")
        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')   

        psspycommand =  {   'function':'load_data_6',
                            'data':[str(Bus_Number), 
                                    ID,
                                    ' ',' ',' ',' ',' ',' ',' ',
                                    str(Pload),str(Qload),' ',' ',' ',' ',' ',' ',],
                            'labeltype':'load'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)
        logger.info('conver to idv sucess')

    elif labeltype=="FIXEDSHUNT":
        Bus_Number = int(args.get('BusNumber'))
        ID = args.get('ID')
        G_Shunt = float(args.get('G_Shunt'))
        B_Shunt = float(args.get('B_Shunt'))
        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        
        psspy.shunt_data(Bus_Number
                        ,ID
                        ,1
                        ,[ G_Shunt,B_Shunt])
        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')   

        psspycommand =  {   'function':'shunt_data',
                            'data':[str(Bus_Number), 
                                    ID,
                                    ' ',
                                    str(G_Shunt),str(B_Shunt)],
                            'labeltype':'fixedshunt'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)
        logger.info('conver to idv sucess')

    elif labeltype=="BRANCH":
        FromBusNumber = int(args.get('FromBusNumber'))
        ToBusNumber = int(args.get('ToBusNumber'))
        ID = args.get('ID')
        LineR = float(args.get('LineR'))
        LineX = float(args.get('LineX'))
        ChargingB = float(args.get('ChargingB'))
        Length = float(args.get('Length')) 
        REAT1 = float(args.get('REAT1'))  
        NAME = args.get('NAME')

        #seq branch
        R_Zero = float(args.get('R_Zero')) 
        X_Zero = float(args.get('X_Zero'))  
        B_Zero = float(args.get('B_Zero'))

        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        
        psspy.branch_data_3(FromBusNumber
                    ,ToBusNumber
                    ,ID
                    ,[1,0,0,0,0,0]
                    ,[ LineR, LineX, ChargingB,0.0,0.0,0.0,0.0, Length,1.0,1.0,1.0,1.0]
                    ,[REAT1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                    ,NAME)
        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')   

        psspycommand =  {   'function':'branch_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    ID,
                                    ' ',' ',' ',' ',' ',' ',
                                    str(LineR),str(LineX),str(ChargingB),' ',' ',' ',' ',str(LineX),' ',' ',' ',' ',
                                    str(REAT1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                    "'"+NAME+"'"],
                            'labeltype':'branch'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)

        psspy.newseq()
        psspy.seq_branch_data_3(FromBusNumber
                                ,ToBusNumber
                                ,ID
                                ,0
                                ,[R_Zero,X_Zero,B_Zero,0,0,0])


        psspycommand =  {   'function':'seq_branch_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber), 
                                    ID,
                                    ' ',
                                    str(R_Zero),str(X_Zero),str(B_Zero),' ',' ',' '],
                            'labeltype':'seq_branch'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)

        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')   
        logger.info('conver to idv sucess')

    elif labeltype=="TRANSFORMER2Winding":
        FromBusNumber = int(args.get('FromBusNumber'))
        ToBusNumber = int(args.get('ToBusNumber'))
        ID = args.get('ID')

        ControlledBus = args.get('ControlledBus')
        if ControlledBus=='':
            ControlledBus = FromBusNumber
        else:
            ControlledBus = int(ControlledBus)

        Winding_int = int(args.get('Winding_int'))
        Impedance = int(args.get('Impedance'))
        Admittance = int(args.get('Admittance'))

        SpecifiedR = float(args.get('SpecifiedR'))
        SpecifiedX = float(args.get('SpecifiedX'))
        Winding = float(args.get('Winding'))
        Wind1 = float(args.get('Wind1'))

        Wind2Ratio = float(args.get('Wind2Ratio'))
        Wind2 = float(args.get('Wind2'))
        RATE1 = float(args.get('RATE1'))
        Name = args.get('Name')
        #seq 2winding
        Connection = int(args.get('Connection'))
        R01 = float(args.get('R01'))
        X01 = float(args.get('X01'))
        


        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        try:
            psspy.two_winding_data_6(FromBusNumber
                                    ,ToBusNumber
                                    ,ID
                                    ,[1,0,0,0,0,0,0,0,ControlledBus,0,0,0,0,Winding_int,Impedance,Admittance]
                                    ,[SpecifiedR, SpecifiedX, Winding, 1.0, Wind1,0.0, Wind2Ratio, Wind2,1.0,1.0,1.0,1.0,0.0,0.0,1.1,0.9,1.1,0.9,0.0,0.0,0.0]
                                    ,[ RATE1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                                    ,Name
                                    ,"")
        except Exception as e:
            
            print('Exception ERROR:',e)
            return e




        logger.info('write into savfile sucess')

        psspycommand =  {   'function':'two_winding_data_6',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    ID,
                                    ' ',' ',' ',' ',' ',' ',' ',' ',str(ControlledBus),' ',' ',' ',' ',str(Winding_int),str(Impedance),str(Admittance),
                                    str(SpecifiedR),str(SpecifiedX),str(Winding),' ',str(Wind1),' ',str(Wind2Ratio),str(Wind2),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                    str(RATE1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                                    "'"+Name+"'"],
                            'labeltype':'two_winding'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)

        #seq 2winding
        # try:
        #     psspy.newseq()
        #     psspy.seq_two_winding_data_3(FromBusNumber
        #                                 ,ToBusNumber
        #                                 ,ID
        #                                 ,[Connection,0,0]
        #                                 ,[0.0,0.0, R01, X01,0.0,0.0,0.0,0.0,0.0,0.0])
        # except Exception as e:
        #     print('Exception ERROR:',e)

        psspycommand =  {   'function':'seq_two_winding_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    ID,
                                    str(Connection),' ',' ',
                                    ' ',' ',str(R01),str(X01),' ',' ',' ',' ',' ',' ',],
                            'labeltype':'seq_two_winding'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)                        
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath='connection_temp_2w.idv')
        psspy.runrspnsfile(r"%s" %'connection_temp_2w.idv')

        psspy.save(r"%s" %target_file)
        os.remove('connection_temp_2w.idv')
        logger.info('save modificated data sucess')    


    elif labeltype=="TRANSFORMER3Winding":
        FromBusNumber = int(args.get('FromBusNumber'))
        
        ToBusNumber = int(args.get('ToBusNumber'))

        LastBusNumber = int(args.get('LastBusNumber'))
        
        ID = args.get('ID')

        #three_wnd_imped_data_4
        connection =int( args.get('connection'))
        
        Winding =int( args.get('Winding'))
        Impedance = int(args.get('Impedance'))
        Admittance = int(args.get('Admittance'))
        ImpaedanceAdjustmentCode = int(args.get('ImpaedanceAdjustmentCode'))
        
        W12R = float(args.get('W12R'))  if args.get('W12R')!="" else  0.0
        
        W12X = float(args.get('W12X')) if args.get('W12X')!=""  else  0.0    
            
        W23R = float(args.get('W23R')) if args.get('W23R')!=""else  0.0  
        
        W23X = float(args.get('W23X'))if args.get('W23X')!=""  else  0.0  
        
        W31R = float(args.get('W31R')) if args.get('W31R')!=""  else  0.0  
        
        W31X = float(args.get('W31X')) if args.get('W31X')!=""  else  0.0  
        

        Winding12MVABase = float(args.get('Winding12MVABase')) if args.get('Winding12MVABase')!=""  else  0.0   
        
        Winding23MVABase = float(args.get('Winding23MVABase')) if args.get('Winding23MVABase')!=""  else  0.0           
        
        Winding31MVABase = float(args.get('Winding31MVABase')) if args.get('Winding31MVABase')!=""  else  0.0           
        

        Name = args.get('Name')



        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.three_wnd_imped_data_4(FromBusNumber
                            ,ToBusNumber
                            ,LastBusNumber
                            ,ID
                            ,[0,0,0,0,Winding,Impedance,Admittance,1,0,0,0,0,ImpaedanceAdjustmentCode]
                            ,[W12R, W12X, W23R, W23X, W31R, W31X, Winding12MVABase, Winding23MVABase, Winding31MVABase,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0]
                            ,Name
                            ,"")  

        # print(args.get('R01'))
        if args.get('R01')!="":
            R01 = float(args.get('R01'))
        if args.get('X01')!="":            
            X01 = float(args.get('X01'))
        if args.get('R02')!="":            
            R02 = float(args.get('R02'))
        if args.get('X02')!="":            
            X02 = float(args.get('X02'))   
        if args.get('R03')!="":            
            R03 = float(args.get('R03'))
        if args.get('X03')!="":            
            X03 = float(args.get('X03'))

        # psspy.newseq()
        # psspy.seq_three_winding_data_3(FromBusNumber
        #                     ,ToBusNumber
        #                     ,LastBusNumber
        #                     ,ID
        #                     ,[0,0,connection]
        #                     ,[0,0, R01, X01,0,0, R02, X02,0,0,R03, X03,0,0]
        #                     )                     


        # try:
        #     psspy.three_wnd_imped_data_4(FromBusNumber
        #                         ,ToBusNumber
        #                         ,LastBusNumber
        #                         ,ID
        #                         ,[0,0,0,0,Winding,Impedance,Admittance,1,0,0,0,0,ImpaedanceAdjustmentCode]
        #                         ,[W12R, W12X, W23R, W23X, W31R, W31X, Winding12MVABase, Winding23MVABase, Winding31MVABase,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0]
        #                         ,Name
        #                         ,"")
        # except Exception as e:
        #     logger.error(e)
        #     print('Exception ERROR:',e)
        #     return e



        logger.info('write into savfile sucess')

        psspycommand =  {   'function':'three_wnd_imped_data_4',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    str(LastBusNumber),
                                    ID,
                                    ' ',' ',' ',' ',str(Winding),str(Impedance),str(Admittance),' ',' ',' ',' ',' ',str(ImpaedanceAdjustmentCode),
                                    str(W12R),str(W12X),str(W23R),str(W23X),str(W31R),str(W31X),str(Winding12MVABase),str(Winding23MVABase),str(Winding31MVABase),' ',' ',' ',' ',' ',' ',' ',' ',
                                    "'"+Name+"'",
                                    "' '"],
                            'labeltype':'three_wnd_imped_data_4'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)

        #seq_three_winding_data_3


           

        # try:

        logger.info('ok')                  
        # except Exception as e:
        #     logger.error(e)
        #     print('Exception ERROR:',e)
        #     return e
        #####################
        ##### 讀idv改connection ##### 
        #####################
        psspycommand =  {   'function':'seq_three_winding_data_3',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    str(LastBusNumber),
                                    ID,
                                    ' ',' ',str(connection)
                                    ,' ',' ',str(R01),str(X01),' ',' ',str(R02),str(X02),' ',' ',str(R03),str(X03),' ',' '                                    
                                    ],
                            'labeltype':'seq_three_winding_data_3'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)                             
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath='connection_temp_3w.idv')
        

        # #####################

        # RATE1 = float(args.get('RATE1')) if args.get('RATE1')!=""  else  0.0  
        
        # Controlled = int(args.get('Controlled')) if args.get('Controlled')!=""  else  0  
        # try:
            
        #     psspy.three_wnd_winding_data_5(FromBusNumber
        #                         ,ToBusNumber
        #                         ,LastBusNumber
        #                         ,ID
        #                         ,1
        #                         ,[33,0,Controlled,0,1,0]
        #                         ,[1.0,0.0,0.0,1.1,0.9,1.1,0.9,0.0,0.0,0.0]
        #                         ,[RATE1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        #                         )
        # except Exception as e:
            
        #     print('Exception ERROR:',e)
        #     return e


        # logger.info('write into savfile sucess')

        # psspycommand =  {   'function':'three_wnd_winding_data_5',
        #                     'data':[str(FromBusNumber), 
        #                             str(ToBusNumber),
        #                             str(LastBusNumber),
        #                             ID,
        #                             '1'
        #                             ,' ',' ',str(Controlled),' ',' ',' '
        #                             ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' '
        #                             ,str(RATE1),' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '
        #                             ],
        #                     'labeltype':'three_wnd_winding_data_5'
        #                 }
        # psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)
        
        psspy.runrspnsfile(r"%s" %'connection_temp_3w.idv')


        psspy.save(r"%s" %target_file)
        os.remove('connection_temp_3w.idv')
        logger.info('save modificated data sucess')

    elif labeltype=="TRANSFORMER3Winding_Winding":
        FromBusNumber = int(args.get('FromBusNumber'))
        
        ToBusNumber = int(args.get('ToBusNumber'))

        LastBusNumber = int(args.get('LastBusNumber'))        
        ID = args.get('ID')

        BusNumber = int(args.get('BusNumber'))
        if BusNumber==FromBusNumber:
            Winding = 1
        elif  BusNumber==ToBusNumber:
            Winding = 2
        else:
            Winding = 3       

        Controlled = int(args.get('Controlled')) if args.get('Controlled')!=""  else  0
        Tap_Positions = int(args.get('Tap_Positions')) if args.get('Tap_Positions')!=""  else 33
        Impendance = int(args.get('Impendance')) if args.get('Impendance')!=""  else  0

        RATE1 = float(args.get('RATE1')) if args.get('RATE1')!=""  else  0.0 
        RATE2 = float(args.get('RATE2')) if args.get('RATE2')!=""  else  0.0 
        RATE3 = float(args.get('RATE3')) if args.get('RATE3')!=""  else  0.0
        RATE4 = float(args.get('RATE4')) if args.get('RATE4')!=""  else  0.0
        RATE5 = float(args.get('RATE5')) if args.get('RATE5')!=""  else  0.0
        RATE6 = float(args.get('RATE6')) if args.get('RATE6')!=""  else  0.0
        RATE7 = float(args.get('RATE7')) if args.get('RATE7')!=""  else  0.0
        RATE8 = float(args.get('RATE8')) if args.get('RATE8')!=""  else  0.0
        RATE9 = float(args.get('RATE9')) if args.get('RATE9')!=""  else  0.0
        RATE10 = float(args.get('RATE10')) if args.get('RATE10')!=""  else  0.0
        RATE11 = float(args.get('RATE11')) if args.get('RATE11')!=""  else  0.0
        RATE12 = float(args.get('RATE12')) if args.get('RATE12')!=""  else  0.0

        Ratio =  float(args.get('Ratio')) if args.get('Ratio')!=""  else  1.0
        Nominal =  float(args.get('Nominal')) if args.get('Nominal')!=""  else  0.0
        Angle =  float(args.get('Angle')) if args.get('Angle')!=""  else  0.0
        Rmax = float(args.get('Rmax')) if args.get('Rmax')!=""  else  1.1
        Rmin = float(args.get('Rmin')) if args.get('Rmin')!=""  else  0.9
        Vmax = float(args.get('Vmax')) if args.get('Vmax')!=""  else  1.1
        Vmin = float(args.get('Vmin')) if args.get('Vmin')!=""  else  0.9
        Wnd_Connect = float(args.get('Wnd_Connect')) if args.get('Wnd_Connect')!=""  else  0.0
        Load_Drop_1 = float(args.get('Load_Drop_1')) if args.get('Load_Drop_1')!=""  else  0.0
        Load_Drop_2 = float(args.get('Load_Drop_2')) if args.get('Load_Drop_2')!=""  else  0.0
        
        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.three_wnd_winding_data_5(FromBusNumber
                                    ,ToBusNumber
                                    ,LastBusNumber
                                    ,ID
                                    ,Winding
                                    ,[Tap_Positions,Impendance,Controlled,0,1,0]
                                    ,[ Ratio, Nominal, Angle, Rmax, Rmin, Vmax, Vmin, Load_Drop_1, Load_Drop_2, Wnd_Connect]
                                    ,[ RATE1, RATE2, RATE3, RATE4, RATE5, RATE6, RATE7, RATE8, RATE9, RATE10, RATE11, RATE12]
                                )
        psspycommand =  {   'function':'three_wnd_winding_data_5',
                            'data':[str(FromBusNumber), 
                                    str(ToBusNumber),
                                    str(LastBusNumber),
                                    ID,
                                    str(Winding)
                                    ,str(Tap_Positions),str(Impendance),str(Controlled),' ',' ',' '
                                    ,str(Ratio),str(Nominal),str(Angle),str(Rmax),str(Rmin),str(Vmax),str(Vmin),str(Load_Drop_1),str(Load_Drop_2),str(Wnd_Connect)
                                    ,str(RATE1),str(RATE2),str(RATE3),str(RATE4),str(RATE5),str(RATE6),str(RATE7),str(RATE8),str(RATE9),str(RATE10),str(RATE11),str(RATE12)
                                    ],
                            'labeltype':'three_wnd_winding_data_5'
                        }                                
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)                             
        # psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath='connection_temp_3w.idv')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')
        
    elif labeltype=="AREA":
        AREA_Number = int(args.get('AREANumber'))
        AREA_Name = args.get('AREAName')

        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.area_data(AREA_Number,0,[0, 10.0],AREA_Name)
        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')        
        
    elif labeltype=="OWNER": 
        OWNER_Num = int(args.get('OWNERNumber'))
        OWNER_Name = args.get('OWNERName')

        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.owner_data(OWNER_Num,OWNER_Name)
        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')           

    elif labeltype=="ZONE":    

        ZONE_Num = int(args.get('ZONENumber'))
        ZONE_Name = args.get('ZONEName')

        psspy.case(r"%s" %Source_File)   
        logger.info('read savfile from Source_File sucess')
        psspy.zone_data(ZONE_Num,ZONE_Name)
        logger.info('write into savfile sucess')
        psspy.save(r"%s" %target_file)
        logger.info('save modificated data sucess')   

        psspycommand =  {   'function':'zone_data',
                            'data':[str(ZONE_Num), "'"+str(ZONE_Name)+"'"],
                            'labeltype':'zone'
                        }
        psspy_to_idv(psspycommand=psspycommand,userName=user,idvpath=idvpath)
        logger.info('conver to idv sucess')


    else:
        pass        



def ParseConfig():

    parser = argparse.ArgumentParser(description="路徑")
    parser.add_argument('-LabelT', '--Label_type', default="BUS", type=str, help='哪個Label')
    parser.add_argument('-SavF', '--Sav_File', default="112P-11109", type=str, help='sav檔檔名')
    parser.add_argument('-user', '--User_Folder', default="User/621882/", type=str, help='使用者資料夾路徑')
    parser.add_argument('-source', '--source_Folder', default="User/621882/", type=str, help='檔案來源資料夾路徑')
    parser.add_argument('-target', '--target_Folder', default="User/621882/", type=str, help='檔案目的地資料夾路徑')
    parser.add_argument('-WriteData', '--Write_Data', nargs='+' ,type=str, help='使用者要輸入的資料')


    args = parser.parse_args()

    labeltype = args.Label_type
    savfile = args.Sav_File
    userfolder =   args.User_Folder  
    sourcefolder = args.source_Folder
    targetfolder = args.target_Folder
    writedata = args.Write_Data
    


    return labeltype, savfile, userfolder, sourcefolder, targetfolder,writedata

if __name__ == '__main__':
    import sys, os
    import base64
    import json
    import argparse
    import logging
        
    
    from Log.LogConfig import Setlog

    labeltype, savfile, userfolder, sourcefolder, targetfolder, writedata= ParseConfig()
    

#######==================  解碼   args ================== ####### 
    encode_type = 'utf-8'
    writedata = writedata[0][2:-1]#因為b'編碼後的資料'，其中b'與最後的'被當成是str所以才解碼不出來

    print(writedata)
    str_dict = base64.b64decode(writedata).decode(encode_type)
    str_dict = json.loads(str_dict)
    logger = Setlog(logfolder= 'Log/'+str_dict.get('userName')+'/PSSELog/', level=logging.INFO,logger_name='psse')
    # logger = Setlog(logfolder = 'Log/'+str_dict.get('userName')+'/PSSELog/',logname='psse')

    Source_File = sourcefolder+savfile
    target_file = targetfolder+savfile
    idvpath = userfolder+'IDV/'+ savfile[0:4]+'.idv'

    logger.info('type(str_dict) = %s',type(str_dict))
    logger.info('user = %s, labeltype = %s',
                        str_dict.get('userName'),
                                        str_dict.get('labeltype'))
    logger.info('Source_File = %s',Source_File)
    logger.info('target_file = %s',target_file)    
    logger.info('str_dict = %s',str_dict)
#######==================  解碼     ================== #######  


    from Config.Load_PSSE_Location import Load_PSSE_Path
    Load_PSSE_Path()
    try:    
        import psse35
        psse35.set_minor(3)
        import psspy
        psspy.psseinit()
        # import pssexcel
        logger.info('import package sucess')
    except Exception as error: 
        
        logger.error(str(error))
        
        raise ImportError(error) 
    
    



    repeat = Write_in_save( Source_File = Source_File
                            ,target_file = target_file
                            ,user = str_dict.get('userName')
                            ,labeltype = labeltype
                            ,idvpath = idvpath
                            ,savefilename = savfile.split('.')[0][0:4]
                            ,args=str_dict)
    print(repeat)
  