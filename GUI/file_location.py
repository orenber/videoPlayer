import os


def full_file(file_folder: list=[])->str:
    return os.path.abspath(os.path.join(*file_folder))






