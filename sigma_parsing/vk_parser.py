import json
from threading import *
import vk_api
from sigma_parsing.data import *
import time
import copy
from pathlib import Path

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def save(members, accounts):
    with open('output/members02.txt', 'w') as f:
        print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
    with open("output/accounts.txt", "w") as f:
        print(json.dumps(accounts, ensure_ascii=False, indent=4), file=f)

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()

vk = vk_session.get_api()

files = [path for path in Path('./output').rglob('members0[1,2]*.txt')]
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
    if ("vk_pages" in member):
        continue 
    users = []
    for config in configs:
        local_config = copy.deepcopy(config)
        local_config["q"] = getstr(member["name"]) + " " + getstr(member["surname"])
        users += vk_session.method("users.search", local_config)["items"]
        time.sleep(PAUSE_TIME)
    # print(users)    
   
    member["vk_pages"] = []
    for user in users:
        if (not user["id"] in ids):
            ids += [user["id"]]
            accounts += [user]
            member["vk_pages"] += [user["id"]] 
    
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save(members, accounts)
save(members, accounts)

print("Accounts size: " + str(len(accounts)))
for i in range(len(accounts)):
    print("downloading friends: " + str(i))
    account = accounts[i]
    if ("friends" in account):
        continue

    try:
        account["friends"] = vk.friends.get(user_id=account["id"],)["items"]
    except:
        account["friends"] = [] 
    time.sleep(PAUSE_TIME)        

    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save(members, accounts)

save(members, accounts)

print("Done")
