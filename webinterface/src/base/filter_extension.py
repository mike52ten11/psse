import os

def find_any_extension(targer_folder,extension=".acc"):

    acc_files = []

    for root, dirs, files in os.walk(targer_folder):
        for file in files:
            if file.endswith(extension):
                acc_files.append(os.path.join(root, file))
    print(acc_files)            
    return acc_files
