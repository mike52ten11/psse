import chardet


def check_encoding_type(checked_data):
     
    return chardet.detect(checked_data)['encoding']