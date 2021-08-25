import vk_api
import json
from sigma_parsing.data import *
import time
from cdifflib import CSequenceMatcher
from pathlib import Path

SIMILARITY_LIMIT = 0.93

def save(members, accounts):
    with open('output/members02.txt', 'w') as f:
        print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
    with open("output/accounts.txt", "w") as f:
        print(json.dumps(accounts, ensure_ascii=False, indent=4), file=f)


def createDict(accounts):
    dct = dict()
    for account in accounts:
        dct[account["id"]] = account
    return dct

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()
vk = vk_session.get_api()

with open("output/accounts.txt") as f:
    accounts = json.load(f)
dct = createDict(accounts)

files = [path for path in Path('./output').rglob('members02*.txt')]
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
new_ids = {}

for account in accounts:
    for friend_id in account["friends"]:
        if (friend_id not in dct) and (friend_id not in new_ids):
            new_ids[friend_id] = {}

keys = list(new_ids.keys())
QUERY_SIZE = 1000
queries = len(keys) // QUERY_SIZE
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
        user_key = new_ids[user_id]["first_name"] + new_ids[user_id]["last_name"] 
    except:
        continue
    # print(user_key)
    for member in members:
        member_key = member["name"] + member["surname"]
        ratio = CSequenceMatcher(None, user_key, member_key).ratio()
        if (ratio >= SIMILARITY_LIMIT):
            member["vk_pages"] += [user_id]
            accounts += [new_ids[user_id]]
            print(user_key, member_key, ratio)
    i += 1
    if (i % 10 == 0):
        print("Status:" + str(i))
        save(members, accounts)
    

save(members, accounts)
