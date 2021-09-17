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

suffix='.friendlists.txt'
members, filename = get_json_by_pattern("output/*vksearch*txt")
members_oname = get_file_name(filename,suffix) 

with open(accounts_oname) as f:
    accounts = json.load(f)

with open(friends_oname) as f:
    friends = json.load(f)
    friends_ids = {f["id"] for f in friends}

with open(groups_oname) as f:
    groups = json.load(f)

id_dict = createDict(accounts) 

count = 0
inside = 0

for account in accounts:
    if not account["id"] in friends_ids: # Полезно в случае, если этот аккаунт приватный
        friend_to_add = copy.deepcopy(account)
        friend_to_add.pop("friends")
        friends.append(friend_to_add)
        friends_ids.add(friend_to_add["id"])
    user_id = account["id"]
    for friend_id in account["friends"]:
        inside += int(friend_id in id_dict)
        if ((friend_id in id_dict) and (not user_id in id_dict[friend_id]["friends"])):
            count += 1  
            id_dict[friend_id]["friends"].append(user_id)
 
print("Simmitration statistics")      
print("Added: " + str(count))
print("Inside: " + str(inside))
print("Inside_Delta_Percent: " + str(count / (count + inside) * 100))

world = set()
for member in members:
    for vk_page_id in member["vk_pages"]:
        world.add(vk_page_id)

for member in members:
    for i in range(len(member["vk_pages"])):
        member_id = member["vk_pages"][i]
        member["vk_pages"][i] = copy.deepcopy(id_dict[member["vk_pages"][i]])
        member["vk_pages"][i]["groups"] = [group["id"] for group in groups if member_id in group["members"]]
        member["vk_pages"][i]["friends"] = [friend_id for friend_id in id_dict[member_id]["friends"] if friend_id in world]

save_as_json(friends, friends_oname)
save_as_json(members, members_oname)

print("Done")
