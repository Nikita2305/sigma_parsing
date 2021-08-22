import json
import time

# At first solve the repeating ids problem.
# Point: we should not solve it by deleting same accounts. 

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def get_id_probability(members, user_id):
    sm = 0
    cnt = 0
    for member in members:
        if (member["processed"]):
            for account in member["vk_pages"]:
                if (account["id"] == user_id):
                    sm += account["probability"]
                    cnt += 1
    return sm / cnt
            

def process(members, processed_ids, member):
    member["processed"] = True
    total = 0
    for account in member["vk_pages"]:
        for friend_id in account["friends"]:
            total += (friend_id in processed_ids)
    mx = 0
    for account in member["vk_pages"]:
        count = 0
        for friend_id in account["friends"]:
            if (not friend_id in processed_ids):
                continue
            count += get_id_probability(members, friend_id)
        account["probability"] = (count / total if total != 0 else 0)
        mx = max(mx, account["probability"])
    print("Probability: " + str(mx))
    

# ---------- SETTINGS ------------ 
 
PROBABILITY_LIMIT = 0.8
PROCESSED_LIMIT = 0.0

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

processed_ids = set()
for member in members:
    if (len(member["vk_pages"]) == 0):
        continue
    l = [len(account["friends"]) for account in member["vk_pages"]]
    l.sort()
    l = l[::-1]
    if ((l[0] >= 10 and (len(l) == 1 or l[1] <= 1)) or (l[0] >= 5 and (len(l) == 1 or l[1] == 0))):
        member["processed"] = True
        for account in member["vk_pages"]:
            processed_ids.add(account["id"])
            if (len(account["friends"]) > 1):
                account["probability"] = 1
            else:
                account["probability"] = 0

print("base:")
print(len([member for member in members if ("processed" in member and member["processed"])]))

# ----------------- STARTING COMPUTING OTHERS --------------------- 

while(True):
    another_members = []
    for member in members:
        if (member["processed"]): 
            continue
        count = 0
        total = 0
        for account in member["vk_pages"]:
            total += len(account["friends"])
            for friend_id in account["friends"]:
                count += int(friend_id in processed_ids)
        if (total == 0):
            continue
        process_level = count / total
        another_members += [(process_level, member)]
    another_members.sort(key=(lambda x: x[0]))
    another_members = another_members[::-1]
    
    if (len(another_members) == 0 or another_members[0][0] < PROCESSED_LIMIT):
        print("Не обработано:" + str(len(another_members)))
        break
 
    process(members, processed_ids, another_members[0][1])
    print("Осталось: " + str(len(another_members)))
    print("Higher_process_level: " + str(another_members[0][0]))

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

print("Final:")
print(len([member for member in members if ("processed" in member and member["processed"])]))

with open('output/members.txt', 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
    print("Written")

print("Done")
