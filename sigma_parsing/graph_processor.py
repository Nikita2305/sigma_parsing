import json
import time

def get_prob(obj):
    if ("probability" in obj.keys()):
        return obj[probability]
    return -1

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def get_member(members, user_id):
    for member in members:
        for account in member["vk_pages"]:
            if (account["id"] == user_id):
                return member

def get_account(member, user_id):
    for account in member["vk_pages"]:
        if (account["id"] == user_id):
            return account

def process(members, member):
    member["processed"] = True
    total = 0
    for account in member["vk_pages"]:
        for friend_id in account["friends"]:
            friend = get_member(members, friend_id)
            if (friend["processed"]):
                total += 1
    for account in member["vk_pages"]:
        count = 0
        for friend_id in account["friends"]:
            friend = get_member(members, friend_id)
            if (friend["processed"]):
                count += get_account(friend, friend_id)["probability"]
        account["probability"] = count / total 

# ---------- SETTINGS ------------ 
 
PROBABILITY_LIMIT = 0.8
PROCESSED_LIMIT = 0.6

with open("output/members.txt") as f:
    members = json.load(f)

# ----------- COUNTING BASE -----------

for member in members:
    if (not "processed" in member):
        member["processed"] = False
    if (not "official_page" in member):
        member["official_page"] = dict()
    for account in member["vk_pages"]:
        if (not "probability" in account):
            account["probability"] = 0

for member in members:
    accounts = member["vk_pages"];
    if (len(accounts) == 0):
        continue
    l = [len(account["friends"]) for account in accounts]
    l.sort()
    l = l[::-1]
    if ((l[0] >= 10 and (len(l) == 1 or l[1] <= 1)) or (l[0] >= 5 and (len(l) == 1 or l[1] == 0))):
        member["processed"] = True
        for account in accounts:
            if (len(account["friends"]) > 1):
                account["probability"] = 1
            else:
                account["probability"] = 0

print("base:")
print(len([member for member in members if ("processed" in member and member["processed"])]))

# ----------------- STARTING COMPUTING OTHERS --------------------- 

while(True):
    print("START")
    TOTAL = 0
    i = 0
    for member in members:
        i += 1
        if (i % 1000 == 0):
            print(i)
        if (member["processed"]): 
            continue
        count = 0
        total = 0
        for account in member["vk_pages"]:
            total += len(account["friends"])
            for friend_id in account["friends"]:
                count += int(get_member(members, friend_id)["processed"])
        if (total == 0):
            continue
        if (count / total >= PROCESSED_LIMIT):
            TOTAL += 1
            process(members, member)
        
    print("CYCLE:" + str(TOTAL))
    if (TOTAL == 0):
        break

# --------- SETTING OFFICIAL PAGE ----------

for member in members:
    if (not member["processed"]):
        continue
    member["processed"] = False
    for account in member["vk_pages"]:
        if (account["probability"] >= PROBABILITY_LIMIT):
            member["official_page"] = account
            member["processed"] = True
            break

with open('output/members.txt', 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
    print("Written")

print("Done")
