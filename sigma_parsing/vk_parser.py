import json
from threading import *
import vk_api
import time
import copy
from pathlib import Path
from sigma_parsing.utils import *
from cdifflib import CSequenceMatcher
from sigma_parsing.vk import *

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def save_members(members):
    with open(oname, 'w') as f:
        print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

def save_accounts(accounts):
    with open("output/accounts.txt", "w") as f:
        print(json.dumps(accounts, ensure_ascii=False, indent=4), file=f)

def save_groups(groups):
    with open("output/groups.txt", "w") as f:
        print(json.dumps(groups, ensure_ascii=False, indent=4), file=f)


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

def assign_friends(response, account):
    account["friends"] = response["items"]

suffix='.vksearch.txt'
members, filename = get_json_by_pattern('output/*xlsxout*txt', 'output/*vksearch*txt')
oname = get_file_name(filename,suffix)
vk = vk_collection(sleep=0.4)

with open("temp/vk_config.txt") as f:
    config = json.load(f)

try:
    with open("output/accounts.txt") as f:
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
        save_members(members)
        save_accounts(accounts)
vk.execute_tasks()
save_members(members)
save_accounts(accounts)

try:
    with open("output/groups.txt") as f:
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
    time.sleep(5)
    groups.append({"id": g_id, "members": users, "processed": False})  
    save_groups(groups)

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
    save_groups(groups)

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
            assign_friends,
            account=account
    ) 
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save_accounts(accounts)
vk.execute_tasks()
save_accounts(accounts)

print("Done")
