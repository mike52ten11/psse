
def data_path_of_user_on_server(user):
    userdir = f"../Data/User/{user}"

    return {'user_dir':f"../Data/User/{user}",
            'savfile_dir':f"{userdir}/SavFile",
            'idvfile_dir':f'{userdir}/IDV',
            'dynamic_dir':f'{userdir}/Dynamic',
            'powerflow_dir':f'{userdir}/PowerFlow',
            'powerflowsub_dir':f'{userdir}/PowerFlowSub',
            'errorcircuit_dir':f'{userdir}/FaultCurrent',
            'filter_dir':f'{userdir}/filter',
            'excute_idvfile_dir':f'{userdir}/excute_idvfile'
            }  

