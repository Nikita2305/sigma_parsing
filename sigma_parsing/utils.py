import json
from sigma_parsing.data import *
import vk_api
from pathlib import Path

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

# return (vk_session, vk) 
def init_vk():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    vk = vk_session.get_api()
    return (vk_session,vk)

# return (json.load(inpfile), inpfilename)
def get_json_by_pattern(patt):
    files = [path for path in Path('.').rglob(patt)]
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
    print('Problems? ( ͡° ͜ʖ ͡°) [Y/n]: ', end='')
    repl=input()
    if(repl in ['n','N','т','Т']):
        fname=oldname+suffix
    else:
        fname=input('Input desired filename (no path, no format): ')
    return fname 
