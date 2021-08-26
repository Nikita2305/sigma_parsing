import json
from threading import *
import vk_api
from sigma_parsing.data import *
import time
import copy
from pathlib import Path
from sigma_parsing.utils import *

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

suffix='.vksearch.txt'

vk_session, vk = init_vk()

members, filename = get_json_by_pattern('output/*xlsxout*txt') # TODO: add vksearch
oname = get_file_name(filename,suffix)

def save(members, accounts):
    with open(oname, 'w') as f:
        print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
    with open("output/accounts.txt", "w") as f:
        print(json.dumps(accounts, ensure_ascii=False, indent=4), file=f)

with open("temp/vk_config.txt") as f:
    configs = json.load(f)

try:
    with open("output/accounts.txt") as f:
        accounts = json.load(f)
except Exception:
    accounts = []
ids = [account["id"] for account in accounts]

PAUSE_TIME = 0.4
SAVING_EVERY = 10
print ("Members size: " + str(len(members)))
for i in range(len(members)):
    print("downloading page: " + str(i))
    member = members[i] 
    if ("vk_pages" in member): # for savings
        continue 
    users = []
    for config in configs:
        local_config = copy.deepcopy(config)
        local_config["q"] = getstr(member["name"]) + " " + getstr(member["surname"])
        users += vk_session.method("users.search", local_config)["items"]
        time.sleep(PAUSE_TIME)
   
    member["vk_pages"] = []
    for user in users:
        if (not user["id"] in member["vk_pages"]):
            member["vk_pages"] += [user["id"]]
        if (not user["id"] in ids):
            accounts += [user]
            ids += [user["id"]]
    
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save(members, accounts)
save(members, accounts)

print("Accounts size: " + str(len(accounts)))
for i in range(len(accounts)):
    print("downloading friends: " + str(i))
    account = accounts[i]
    if ("friends" in account): # for savings
        continue
    account["friends"] = []
    try:
        a_id = account["id"]
        account["friends"] = vk.friends.get(user_id=a_id,)["items"]
    except:
        try:
            account["friends"] = vk.friends.get(user_id=account,)["items"]
        except:
            account["friends"] = [] 

    time.sleep(PAUSE_TIME)        

    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save(members, accounts)

save(members, accounts)

print("Done")
