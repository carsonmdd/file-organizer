import os
import sys

def external_path(relative_path):
    '''Gets path for resource in same directory as exe file on Windows'''
    # If running as exe,
    if getattr(sys, 'frozen', False):
        exe_path = os.path.abspath(sys.executable)
        base_path = os.path.dirname(exe_path)
    # else running as script
    else:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

def new_path(path):
    '''Creates a unique path using a counter'''
    root, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f'{root}_{counter}{ext}'
        counter += 1
    return path