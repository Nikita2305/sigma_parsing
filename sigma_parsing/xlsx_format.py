import json
import re
import matplotlib.pyplot as plt
import vk_api
from sigma_parsing.data import *
from pathlib import Path

def find_number(string):
    start = -1
    end = -2
    for i in range(len(string)):
        if ('0' <= string[i]  and string[i] <= '9'):
            end = i
            if (start == -1):
                start = i
    return string[start : end + 1]

files = [path for path in Path('./output').rglob('members01*.txt')]
if (len(files) >= 1):
    print("Type a number:")
    for i in range(len(files)):
        print(i, ":", files[i])
    i = int(input())
    with open(files[i % len(files)]) as f:
        members = json.load(f) 
else:
    print("No file")
    quit() 

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
vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()
vk = vk_session.get_api()
print("Waiting Time: " + str(len([member for member in members if not isinstance(member["vk_id"], int)])) + "s")
i = 0
for member in members:
    i += 1
    print("id found:" + str(i))
    if (isinstance(member["vk_id"], int)):
        continue
    if (i % 10 == 0):
        with open('output/members01_f.txt', 'w') as f:
            print(json.dumps(members, ensure_ascii=False, indent=4), file=f)         
    short_school = find_number(member["school"])
    member["school"] = (short_school if len(short_school) != 0 else member["school"])
    try:
        member["vk_id"] = vk.users.get(user_ids=member["vk_id"][member["vk_id"].rfind("/") + 1:])[0]["id"]
        time.sleep(0.4)
    except Exception:
        pass

with open('output/members01_f.txt', 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f) 
