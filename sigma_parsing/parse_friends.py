import vk_api
import json
import time
from cdifflib import CSequenceMatcher
from pathlib import Path
from sigma_parsing.utils import *

# Something doesn't work

SIMILARITY_LIMIT = 0.93

def createDict(accounts):
    dct = dict()
    for account in accounts:
        dct[account["id"]] = account
    return dct

suffix = '.vksearch.txt'
members, filename = get_json_by_pattern("output/*processed*txt")
members_oname = get_file_name(filename, suffix)

with open(accounts_oname) as f:
    accounts = json.load(f)
    dct = createDict(accounts)
with open(friends_oname) as f:
    friends = json.load(f)
    friends_dct = createDict(friends)

new_ids = []

for member in members:
    if (not member["processed"]):
        continue
    for friend_id in dct[member["official_page"]["id"]]["friends"]:
        if (friend_id not in dct) and (friend_id not in new_ids):
            new_ids.append(friend_id)

i = 0
print("New ids size:" + str(len(new_ids)))
for user_id in new_ids:
    user_key = friends_dct[user_id]["first_name"] + " " + friends_dct[user_id]["last_name"] 
    for member in members:
        member_key = member["name"] + " " + member["surname"]
        ratio1 = CSequenceMatcher(None, user_key, member_key).ratio()
        if (ratio1 >= SIMILARITY_LIMIT):
            member["vk_pages"].append(friends_dct[user_id])
            accounts.append(friends_dct[user_id])
            print(user_key, member_key, ratio1)
    i += 1
    if (i % 100 == 0):
        print("Status:" + str(i))

for member in members:
    for i in range(len(member["vk_pages"])):
        member["vk_pages"][i] = member["vk_pages"][i]["id"]
    # member.pop("processed")
    # member.pop("official_page")

save_as_json(members, members_oname)
save_as_json(accounts, accounts_oname)
