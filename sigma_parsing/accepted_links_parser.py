import vk_api
import json
from data import *
import time

def getstr(var):
    try:
        return str(var)
    except:
        return ""

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()

vk = vk_session.get_api()

with open("temp/links.txt") as links:
    short_names = []

    while True:
        line = links.readline()
        if not line:
            break
        name = line[line.rfind('/') + 1:]
        if (line.rfind('/') != -1):
            short_names += [name]

ans = [str(user["id"]) for user in vk.users.get(user_ids=",".join(short_names))]

with open("output/members.txt") as f:
    members = json.load(f)

size = 0

for member in members:
    if (len(member["vk_pages"]) == 0):
        continue
    sm = 0
    for account in member["vk_pages"]:
        if (getstr(account["id"]) in ans):
            account["probability"] = 1
            sm += 1
    if (sm > 1):
        print(getstr(member["name"]) + " " + getstr(member["surname"]) + " - same_ids in one list")
        for account in member["vk_pages"]:
            account["probability"] = 0
        break
    if (sm == 1):
        member["processed"] = True 
        size += 1
        for account in member["vk_pages"]:
            if (not "probability" in account.keys()):
                account["probability"] = 0


with open("output/members.txt", "w") as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f) 

print("Added: " + str(size))
