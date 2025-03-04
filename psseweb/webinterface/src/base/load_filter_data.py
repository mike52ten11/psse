import numpy as np


def load_filter_data(load_file): 

    np_data = np.load(load_file)
    Num, Name = np_data["num"], np_data['name']
     
    
    return [
        {'num': num, 'name': name}
        for num, name in zip(Num, Name)
    ]     
    