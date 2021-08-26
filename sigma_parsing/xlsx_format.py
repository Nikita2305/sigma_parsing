import json
import re
import matplotlib.pyplot as plt
import vk_api
from sigma_parsing.data import *
from pathlib import Path
from sigma_parsing.utils import *
import time

def find_number(string):
    start = -1
    end = -2
    for i in range(len(string)):
        if ('0' <= string[i]  and string[i] <= '9'):
            end = i
            if (start == -1):
                start = i
    return string[start : end + 1]

suffix = ".xlsxout.txt"
members, filename = get_json_by_pattern('output/*xlsxout*txt')
oname = get_file_name(filename,suffix)
vk_session, vk = init_vk()

with open("temp/xlsx_config.txt") as f:
    fields = json.load(f)

final = []

for member in members:
    OK = True
    for field in fields:
        if (not isinstance(member[field["field"]], str)):
            continue
        if (not re.search(field["pattern"], member[field["field"]]) and field["important"]):
            OK = False
    if(OK):
        final += [member]

members = final
final_final = []
print("Waiting Time: " + str(len([member for member in members if not isinstance(member["vk_id"], int)])) + "s")
i = 0
for member in members:
    i += 1
    print("id found:" + str(i))
    if (isinstance(member["vk_id"], int)):
        continue
    if (i % 10 == 0):
        with open(oname, 'w') as f:
            print(json.dumps(final_final, ensure_ascii=False, indent=4), file=f)         
    short_school = find_number(member["school"])
    member["school"] = (short_school if len(short_school) != 0 else member["school"])
    try:
        member["vk_id"] = vk.users.get(user_ids=member["vk_id"][member["vk_id"].rfind("/") + 1:])[0]["id"]
        time.sleep(0.4)
        final_final += [member]
    except Exception as e:
        print(e)
        pass

with open(oname, 'w') as f:
    print(json.dumps(final_final, ensure_ascii=False, indent=4), file=f) 
