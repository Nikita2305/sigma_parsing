import vk_api
import json
from sigma_parsing.data import *
import time
from cdifflib import CSequenceMatcher
from pathlib import Path
from sigma_parsing.utils import *

SIMILARITY_LIMIT = 0.93

def save(members, accounts):
    with open(oname, 'w') as f:
        print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
    with open("output/accounts.txt", "w") as f:
        print(json.dumps(accounts, ensure_ascii=False, indent=4), file=f)


def createDict(accounts):
    dct = dict()
    for account in accounts:
        dct[account["id"]] = account
    return dct

vk_session, vk = init_vk()
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
    for friend_id in dct[member["official_page"]["id"]]["friends"]:
        if (friend_id not in dct) and (friend_id not in new_ids):
            new_ids[friend_id] = {}

keys = list(new_ids.keys())
QUERY_SIZE = 1000
queries = (len(keys) + 1) // QUERY_SIZE
print("Q:", len(keys))
for i in range(queries):
    print("query:" + str(i))
    local_keys = [str(x) for x in keys[i * QUERY_SIZE : (i + 1) * QUERY_SIZE]]
    if (len(local_keys) == 0):
        continue
    response = vk.users.get(user_ids=",".join(local_keys), fields = "bdate,schools")
    for item in response:
        new_ids[item["id"]] = item
    time.sleep(0.4)

i = 0
print(len(new_ids))
for user_id in new_ids:
    try:
        user_key = new_ids[user_id]["first_name"] + " " + new_ids[user_id]["last_name"] 
    except:
        continue
    for member in members:
        member_key = member["name"] + " " + member["surname"]
        ratio1 = CSequenceMatcher(None, user_key, member_key).ratio()
        if (ratio1 >= SIMILARITY_LIMIT):
            member["vk_pages"] += [user_id]
            accounts += [new_ids[user_id]]
            print(user_key, member_key, ratio1)
    i += 1
    if (i % 10 == 0):
        print("Status:" + str(i))
    
save(members, accounts)
    # print(user_key)
