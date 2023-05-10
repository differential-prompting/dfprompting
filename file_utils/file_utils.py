import os.path
import re
from os import path, makedirs


def read_file(file_path):
    """Reads the contents of a file and returns it as a string."""
    with open(file_path, "r", encoding='utf-8') as file:
        contents = file.read()
    return contents

def write_file(file_path, file_name,contents):
    """Writes the specified contents to a file."""
    if not path.exists(file_path):
        makedirs(path.dirname(file_path), exist_ok=True)
    with open(file_path+'/'+file_name, "w", encoding='utf-8') as file:
        file.write(contents)

def clean_codes(path):
    codes = read_file(path)
    x = re.findall("```([\s\S]*?)```", codes)
    try:
        write_file(os.path.dirname(path),'generated01.py',x[0].replace('python','').replace('```',''))
        write_file(os.path.dirname(path),'generated02.py',x[1].replace('python','').replace('```',''))
    except Exception as e:
        print(path + ':( --- crash when clean code')
