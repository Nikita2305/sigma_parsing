import json
from threading import *
import time
from pathlib import Path
import copy
from sigma_parsing.utils import *

def createDict(accounts):
    dct = dict()
    for account in accounts:
        dct[account["id"]] = account
    return dct

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

suffix='.friendlists.txt'
members, filename = get_json_by_pattern("output/*vksearch*txt")
oname = get_file_name(filename,suffix)

with open("output/accounts.txt") as f:
    accounts = json.load(f)

id_dict = createDict(accounts) 

count = 0
inside = 0

for account in accounts:
    user_id = account["id"]
    for friend in account["friends"]:
        friend_id = friend["id"]
        inside += int(friend_id in id_dict)
        if ((friend_id in id_dict) and (not user_id in [f["id"] for f in id_dict[friend_id]["friends"]])):
            count += 1
            account_to_add = copy.deepcopy(account)
            account_to_add.pop("friends")
            id_dict[friend_id]["friends"].append(account_to_add)
  
print("Simmitration statistics")      
print("Added: " + str(count))
print("Inside: " + str(inside))
print("Inside_Delta_Percent: " + str(count / (count + inside) * 100))

with open("output/groups.txt") as f:
    groups = json.load(f)

print()
print()
print("Мир побольше(B) или поменьше(S)?")
world = set()
s = input()
if (s.lower()[0] == 'b'):
    for member in members:
        for vk_page in member["vk_pages"]:
           for friend in id_dict[vk_page]["friends"]:
                world.add(friend["id"])
else:
    for member in members:
        for vk_page in member["vk_pages"]:
            world.add(vk_page)

for member in members:
    for i in range(len(member["vk_pages"])):
        member_id = member["vk_pages"][i]
        member["vk_pages"][i] = copy.deepcopy(id_dict[member["vk_pages"][i]])
        member["vk_pages"][i]["groups"] = [group["id"] for group in groups if member_id in group["members"]]
        member["vk_pages"][i]["friends"] = [friend for friend in id_dict[member_id]["friends"] if friend["id"] in world]

with open(oname, 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

print("Done")
