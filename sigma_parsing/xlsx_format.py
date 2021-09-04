import json
import re
import matplotlib.pyplot as plt
from sigma_parsing.utils import *
from sigma_parsing.vk import *
import time
import copy

def append_member(response, array, obj):
    obj["vk_id"] = response[0]["id"]
    array.append(obj)

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
vk = vk_collection(sleep=0.4)

with open("temp/xlsx_config.txt") as f:
    columns = json.load(f)

final = []

for member in members:
    OK = True
    for column in columns:
        if (not isinstance(member[column["field_name"]], str)):
            continue
        if (not re.search(column["data_pattern"], member[column["field_name"]]) and column["is_important"]):
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
    short_name = member["vk_id"][member["vk_id"].rfind("/") + 1:]
    vk.call("users.get",
            {"user_ids": short_name},
            append_member,
            array=final_final,
            obj=copy.deepcopy(member)
    )


with open(oname, 'w') as f:
    print(json.dumps(final_final, ensure_ascii=False, indent=4), file=f) 
