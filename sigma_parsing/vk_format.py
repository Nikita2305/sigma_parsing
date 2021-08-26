import json
from threading import *
from sigma_parsing.data import *
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
total = 0
inside = 0
for account in accounts:
    user_id = account["id"]
    for friend_id in account["friends"]:
        total += 1
        inside += int(friend_id in id_dict)
        if ((friend_id in id_dict) and (not user_id in id_dict[friend_id]["friends"])):
            count += 1
            id_dict[friend_id]["friends"] += [user_id]
  
print("Simmitration statistics")      
print("Added: " + str(count))
print("Total: " + str(total))
print("Total_Delta_Percent: " + str(count / (count + total) * 100))
print("Inside: " + str(inside))
print("Inside_Delta_Percent: " + str(count / (count + inside) * 100))

print()
print()
print("Мир побольше(B) или поменьше(S)?")
world = set()
s = input()
if (s.lower()[0] == 'b'):
    for member in members:
        for vk_page in member["vk_pages"]:
           for friend_id in id_dict[vk_page]["friends"]:
                world.add(friend_id)
else:
    for member in members:
        for vk_page in member["vk_pages"]:
            world.add(vk_page if isinstance(vk_page, int) else vk_page["id"])

for member in members:
    for i in range(len(member["vk_pages"])):
        if (isinstance(member["vk_pages"][i], int)):
            member["vk_pages"][i] = copy.deepcopy(id_dict[member["vk_pages"][i]])
        member["vk_pages"][i]["friends"] = [x for x in id_dict[member["vk_pages"][i]["id"]]["friends"] if x in world]

with open(oname, 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

print("Done")
