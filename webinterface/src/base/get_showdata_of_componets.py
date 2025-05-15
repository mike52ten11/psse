
import os
class GetShowDataOfComponents:
    def __init__(self,show_data_path):
        self.show_data_path = show_data_path

    def area(self):    
        prepare_writing_data_area = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r',encoding='ansi') as f:
                area_data = f.read().splitlines()
            print(area_data)    
            for i in range(len(area_data)):
                if area_data[i]!='':
                    data = area_data[i].split(',')
                    
                    prepare_writing_data_area.append({"row":i,"area_number":data[0], "area_name":data[1][1:-1]})

            # print(prepare_writing_data_area)
            return prepare_writing_data_area
        else:
            return []   

    def zone(self):    
        prepare_writing_data_zone = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r',encoding='ansi') as f:
                zone_data = f.read().splitlines()
            print(zone_data)    
            for i in range(len(zone_data)):
                if zone_data[i]!='':
                    data = zone_data[i].split(',')
                    
                    prepare_writing_data_zone.append({"row":i,"zone_number":data[0], "zone_name":data[1][1:-1]})

            # print(prepare_writing_data_area)
            return prepare_writing_data_zone
        else:
            return []       

    def owner(self):    
        prepare_writing_data_owner = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r',encoding='ansi') as f:
                owner_data = f.read().splitlines()
            print(owner_data)    
            for i in range(len(owner_data)):
                if owner_data[i]!='':
                    data = owner_data[i].split(',')
                    
                    prepare_writing_data_owner.append({"row":i,"owner_number":data[0], "owner_name":data[1][1:-1]})

            # print(prepare_writing_data_area)
            return prepare_writing_data_owner
        else:
            return []           

    def bus(self):    
        prepare_writing_data_bus = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r',encoding='ansi') as f:
                bus_data = f.read().splitlines()
             
            for i in range(len(bus_data)):
                if bus_data[i]!='':
                    data = bus_data[i].split(',')
                    
                    prepare_writing_data_bus.append({"row":i,
                                                    "bus_number":data[0], 
                                                    "bus_name":data[1][1:-1],
                                                    "code":data[2],
                                                    "area_number":data[3],
                                                    "zone_number":data[4],
                                                    "owner_number":data[5],
                                                    "base_kv":data[6],
                                                    "Voltage":data[7],
                                                    "angle_deg":data[8],
                                                    "normal_vmax":data[9],
                                                    "normal_vmin":data[10],
                                                    "emergency_vmax":data[11],
                                                    "emergency_vmin":data[12],  
                                                     }                                                                                 
                                                    )

            # print(prepare_writing_data_area)
            return prepare_writing_data_bus
        else:
            return []                         

    def load(self):    
        prepare_writing_data_load = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r',encoding='ansi') as f:
                load_data = f.read().splitlines()
            print(load_data)    
            for i in range(len(load_data)):
                if load_data[i]!='':
                    data = load_data[i].split(',')
                    
                    prepare_writing_data_load.append({"row":i,"bus_number":data[0]
                                                    , "pload":data[1]
                                                    , "qload":data[2]
                                                    }
                                                    )

            # print(prepare_writing_data_area)
            return prepare_writing_data_load
        else:
            return []     

    def machine(self):    

        prepare_writing_data_machine = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r', encoding='ansi') as f:
                machine_data = f.read().splitlines()
            print(machine_data)    
            for i in range(len(machine_data)):
                if machine_data[i] != '':
                    data = machine_data[i].split(',')
                    
                    prepare_writing_data_machine.append({
                        "row": i,
                        "bus_number": data[0],
                        "id": data[1],
                        "machine_control_mode": data[2],
                        "base": data[3],
                        "pgen": data[4],
                        "qgen": data[5],
                        "qmax": data[6],
                        "qmin": data[7],  # Note: Qmin is not in your data string, added as placeholder
                        "pmax": data[8],
                        "pmin": data[9],
                        "mbase": data[10],
                        "r_source": data[11],
                        "x_source": data[12],
                        "r": data[13],
                        "subtransient_x": data[14],
                        "r_negative": data[15],
                        "x_negative": data[16],
                        "r_zero": data[17],
                        "x_zero": data[18],
                        "transient_x": data[19],
                        "synchronous_x": data[20]
                    })

            return prepare_writing_data_machine
        else:
            return []

    def branch(self):    

        prepare_writing_data_branch = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r', encoding='ansi') as f:
                branch_data = f.read().splitlines()
            print(branch_data)    
            for i in range(len(branch_data)):
                if branch_data[i] != '':
                    data = branch_data[i].split(',')
                    if data[11]!="":
                       name = data[11][1:-1] 
                    else:
                        name =  data[11]                       
                    prepare_writing_data_branch.append({
                        "row": i,
                        "from_bus_number": data[0],
                        "to_bus_number": data[1],
                        "id": data[2],
                        "line_r": data[3],
                        "line_x": data[4],
                        "charging_b": data[5],
                        "rate1": data[6],
                        "r_zero": data[7],
                        "x_zero": data[8],
                        "b_zero": data[9],
                        "length": data[10],
                        "name": name
                    })

            return prepare_writing_data_branch
        else:
            return []   

    def twowinding(self):    

        prepare_writing_data_twowinding = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r', encoding='ansi') as f:
                twowinding_data = f.read().splitlines()
            print(twowinding_data)    
            for i in range(len(twowinding_data)):
                if twowinding_data[i] != '':
                    data = twowinding_data[i].split(',')
                    if data[14]!="":
                       name = data[14][1:-1] 
                    else:
                        name =  data[14]                    
                    prepare_writing_data_twowinding.append({
                        "row": i,
                        "from_bus_number": data[0],
                        "to_bus_number": data[1],
                        "id": data[2],
                        "controlled_bus": data[3],
                        "winding_i_o_code": data[4],
                        "impedance_i_o_code": data[5],
                        "admittance_i_o_code": data[6],
                        "specified_r_pu_or_watts": data[7],
                        "specified_x_pu": data[8],
                        "winding": data[9],
                        "wind_1": data[10],
                        "wind_2_ratio": data[11],
                        "wind_2": data[12],
                        "rate1_mva": data[13],
                        "name": name,
                        "connection_code": data[15],
                        "r01_pu": data[16],
                        "x01_pu": data[17]
                    })

            return prepare_writing_data_twowinding
        else:
            return []     
    def threewinding(self):
        prepare_writing_data_threewinding = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r', encoding='ansi') as f:
                threewinding_data = f.read().splitlines()
            print(threewinding_data)    
            for i in range(len(threewinding_data)):
                if threewinding_data[i] != '':
                    data = threewinding_data[i].split(',')
                    
                    if data[4]!="":
                       name = data[4][1:-1] 
                    else:
                        name =  data[4]  
                    prepare_writing_data_threewinding.append({
                        "row": i,
                        "from_bus_number": data[0],
                        "to_bus_number": data[1],
                        "last_bus_number": data[2],
                        "id": data[3],
                        "name":name,
                        "winding_i_o_code": data[5],
                        "impedance_i_o_code": data[6],
                        "admittance_i_o_code": data[7],
                        "w1_2r_pu_or_watts": data[8],
                        "w1_2x_pu": data[9],
                        "w2_3r_pu_or_watts": data[10],
                        "w2_3x_pu": data[11],
                        "w3_1r_pu_or_watts": data[12],
                        "w3_1x_pu": data[13],
                        "winding_1_2_mva_base": data[14],
                        "winding_2_3_mva_base": data[15],
                        "winding_3_1_mva_base": data[16],
                        "impaedance_adjustment_code": data[17],
                        "connection": data[18],
                        "r01_pu": data[19],
                        "x01_pu": data[20],
                        "r02_pu": data[21],
                        "x02_pu": data[22],
                        "r03_pu": data[23],
                        "x03_pu": data[24]
                    })

            return prepare_writing_data_threewinding
        else:
            return []              

    def threewinding_winding(self):
        prepare_writing_data_threewinding_winding = []
        if os.path.isfile(self.show_data_path):
            with open(self.show_data_path, 'r', encoding='ansi') as f:
                threewinding_winding_data = f.read().splitlines()
            print(threewinding_winding_data)    
            for i in range(len(threewinding_winding_data)):
                if threewinding_winding_data[i] != '':
                    data = threewinding_winding_data[i].split(',')
                    
                    prepare_writing_data_threewinding_winding.append({
                        "row": i,
                        "from_bus_number": data[0],
                        "to_bus_number": data[1],
                        "last_bus_number": data[2],
                        "bus_number_to_modify": data[3],
                        "tap_positions": data[4],
                        "impendance": data[5],
                        "controlled": data[6],
                        "ratio": data[7],
                        "nominal": data[8],
                        "angle": data[9],
                        "rmax": data[10],
                        "rmin": data[11],
                        "vmax": data[12],
                        "vmin": data[13],
                        "load_drop_1": data[14],
                        "load_drop_2": data[15],
                        "wnd_connect": data[16],
                        "rate1": data[17],
                        "rate2": data[18],
                        "rate3": data[19],
                        "rate4": data[20],
                        "rate5": data[21],
                        "rate6": data[22],
                        "rate7": data[23],
                        "rate8": data[24],
                        "rate9": data[25],
                        "rate10": data[26],
                        "rate11": data[27],
                        "rate12": data[28]
                    })

            return prepare_writing_data_threewinding_winding
        else:
            return []