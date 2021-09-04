import vk_api
import json
import time
from cdifflib import CSequenceMatcher
from pathlib import Path
from sigma_parsing.utils import *

SIMILARITY_LIMIT = 0.93

def save_members(members):
    with open(oname, 'w') as f:
        print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

def save_accounts(accounts):
    with open("output/accounts.txt", "w") as f:
        print(json.dumps(accounts, ensure_ascii=False, indent=4), file=f)

def createDict(accounts):
    dct = dict()
    for account in accounts:
        dct[account["id"]] = account
    return dct

suffix = '.vksearch.txt'
members, filename = get_json_by_pattern("output/*processed*txt")
oname = get_file_name(filename, suffix)

with open("output/accounts.txt") as f:
    accounts = json.load(f)
dct = createDict(accounts)

new_ids = {}

for member in members:
    if (not member["processed"]):
        continue
    for friend in dct[member["official_page"]["id"]]["friends"]:
        friend_id = friend["id"]
        if (friend_id not in dct) and (friend_id not in new_ids):
            new_ids[friend_id] = friend

i = 0
print(len(new_ids))
for user_id in new_ids:
    user_key = new_ids[user_id]["first_name"] + " " + new_ids[user_id]["last_name"] 
    for member in members:
        member_key = member["name"] + " " + member["surname"]
        ratio1 = CSequenceMatcher(None, user_key, member_key).ratio()
        if (ratio1 >= SIMILARITY_LIMIT):
            member["vk_pages"].append(new_ids[user_id])
            accounts += [new_ids[user_id]]
            print(user_key, member_key, ratio1)
    i += 1
    if (i % 10 == 0):
        print("Status:" + str(i))

for member in members:
    for i in range(len(member["vk_pages"])):
        member["vk_pages"][i] = member["vk_pages"][i]["id"]
    # member.pop("processed")
    # member.pop("official_page")

save_members(members)
save_accounts(accounts)
