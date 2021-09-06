import json
import vk_api
from pathlib import Path
import re

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def get_json_by_pattern(*patterns):
    files = []
    for pattern in patterns:
        new_files = [path for path in Path('.').rglob(pattern)]
        files += [f for f in new_files if f not in files]
    if (len(files) >= 1):
        print("Type a number:")
        for i in range(len(files)):
            print(i, ":", files[i])
        try:
            i = int(input())
        except:
            print('Никита не хочет чтобы тут были маты, но бля чел, ну как можно было блять провалить задачу ввести число??? Ну даже если бы ты ввел число побольше чем надо, ладно, мы бы по модулю взяли, даже отрицательное НО БЛЯТЬ ЧИСЛО ЧЕЛ ЧИСЛО))))')
            quit()
        with open(files[abs(i % len(files))]) as f:
            return (json.load(f),str(files[abs(i % len(files))]).split('.')[0])
    else:
        print("No file")
        quit()

def get_file_name(oldname,suffix):
    fname=''
    print('You are about to output to '+oldname+suffix)
    if Path(oldname+suffix).is_file():
        print("ALERT: You're going to rewrite existing file")
    print('Is it OK? ( ͡° ͜ʖ ͡°) [Y/n]: ', end='')
    repl=input()
    if(len(repl) > 0 and repl[0] in ['n','N']):
        fname=input('Input desired filename (like: output/my_members): ')+suffix
    else:
        fname=oldname+suffix 
    if Path(fname).is_file():
        print("ALERT: Existing file has been rewritten")
    return fname 

def get_new_file_name(filename, suffix):
    full_name = filename[:len(filename) - len(suffix)]
    print(full_name)
    if re.search(".*\([0-9]+\)",full_name):
        name = full_name[:full_name.rfind("(")]
        number = int(full_name[full_name.rfind("(") + 1:-1])
        return name + "(" + str(number + 1) + ")" + suffix
    return full_name + "(1)" + suffix
