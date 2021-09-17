import json
from threading import *
import vk_api
import time
import copy
from pathlib import Path
from sigma_parsing.utils import *
from cdifflib import CSequenceMatcher
from sigma_parsing.vk import *

def append_accounts(response, array, id_array, member): 
    for user in response["items"]:
        if (not user["id"] in member["vk_pages"]):
            member["vk_pages"].append(user["id"])
        if (not user["id"] in ids):
            accounts.append(user)
            ids.append(user["id"])

def append_group_members(response, array):
    if (len(response["items"]) == 0):
        return False
    for member in response["items"]:
        array.append(member)
    return True

def append_friends(response, account, friends_array, friend_set): 
    for friend in response["items"]:
        account["friends"].append(friend["id"])
        if not friend["id"] in friend_set:
            friend_set.add(friend["id"])
            friends_array.append(friend)

suffix='.vksearch.txt'
members, filename = get_json_by_pattern('output/*xlsxout*txt', 'output/*vksearch*txt')
members_oname = get_file_name(filename,suffix)
vk = vk_collection(sleep=0.4)

with open(vkconfig_iname) as f:
    config = json.load(f)

try:
    with open(accounts_oname) as f:
        accounts = json.load(f)
except Exception:
    accounts = []
ids = [account["id"] for account in accounts]

SIMILARITY_LIMIT = 0.93
SAVING_EVERY = 100
print ("Members size: " + str(len(members)))
for i in range(len(members)):
    print("downloading page: " + str(i))
    member = members[i] 
    if ("vk_pages" in member):
        continue 
    member["vk_pages"] = []
    for account_pattern in config["accounts"]:
        local_pattern = copy.deepcopy(account_pattern)
        local_pattern["q"] = getstr(member["name"]) + " " + getstr(member["surname"])
        local_pattern["fields"] = config["fields"]
        vk.add_task("users.search",
                local_pattern,
                append_accounts,
                array=accounts,
                id_array=ids,
                member=member
        )   
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save_as_json(members, members_oname)
        save_as_json(accounts, accounts_oname)
vk.execute_tasks()
save_as_json(members, members_oname)
save_as_json(accounts, accounts_oname)

try:
    with open(groups_oname) as f:
        groups = json.load(f)
except Exception:
    groups = []

for i in range(len(config["groups"])): 
    g_id = config["groups"][i]
    print("downloading group " + str(g_id))
    if (g_id in [group["id"] for group in groups]):
        continue
    j = 0
    users = [] 
    while(True):
        print("Status " + str(j * 1000))
        OK = vk.direct_call("groups.getMembers",
                        {"group_id": g_id,
                        "offset": j*1000,
                        "count": 1000,
                        "fields": config["fields"]},
                    append_group_members,
                    array=users
        )
        if (not OK):
            break
        j += 1
    groups.append({"id": g_id, "members": users, "processed": False})  
    save_as_json(groups, groups_oname)

for group in groups:
    print("processing " + group["id"])
    if (group["processed"]):
        continue 
    for member in members:
        member_key = member["name"] + " " + member["surname"]
        member_ids = [account for account in member["vk_pages"]]
        for user in group["members"]:
            user_key = user["first_name"] + " " + user["last_name"]
            ratio1=CSequenceMatcher(None, user_key, member_key).ratio()
            if (ratio1 >= SIMILARITY_LIMIT):
                if (not user["id"] in member_ids):
                    member["vk_pages"].append(user["id"])
                    member_ids.append(user["id"])
                if (not user["id"] in ids):
                    accounts.append(user)
                    ids.append(user["id"])
    group["processed"] = True
    save_as_json(groups, groups_oname)

try:
    with open(friends_oname) as f:
        friends = json.load(f)
except Exception:
    friends = []
friend_set = {friend["id"] for friend in friends}

print("Accounts size: " + str(len(accounts)))
for i in range(len(accounts)):
    print("downloading friends: " + str(i))
    account = accounts[i] 
    if ("friends" in account): # for savings
        continue
    account["friends"] = []
    vk.add_task("friends.get",
                {"user_id": account["id"],
                "fields": config["fields"]},
            append_friends,
            account=account,
            friends_array=friends,
            friend_set=friend_set
    ) 
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save_as_json(accounts, accounts_oname)
        save_as_json(friends, friends_oname)
vk.execute_tasks()
save_as_json(accounts, accounts_oname)
save_as_json(friends, friends_oname)

print("Done")
