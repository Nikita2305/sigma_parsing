import json
from threading import *
import vk_api
from sigma_parsing.data import *
import time

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()

vk = vk_session.get_api()

with open("output/members.txt") as f:
    members = json.load(f)

users = []
all_ids = []
size = len(members) 
COUNT = 5
PAUSE_TIME = 0.4
SAVING_EVERY = 10
print ("Waiting time ~" + str(size * 2) + "seconds")
for i in range(size):
    print("pages: " + str(i))
    if ("vk_pages" in members[i].keys()):
        continue
    name=getstr(members[i]["name"])
    surname=getstr(members[i]["surname"])
    users = vk.users.search(
        q=name + " " + surname,
        count=COUNT,
        city=104,
        age_from=12,
        age_to=19
    )["items"]
    time.sleep(PAUSE_TIME)
    users += vk.users.search(
        q=name + " " + surname,
        count=COUNT,
        city=104
    )["items"]
    time.sleep(PAUSE_TIME)
    
    temp = []
    ids = []
    for user in users:
        if (not user["id"] in ids):
            ids += [user["id"]]
            temp += [user]
    all_ids += ids
    users = temp
    members[i]["vk_pages"] = users
    
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        with open('output/members.txt', 'w') as f:
            print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

with open('output/members.txt', 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

for i in range(size):
    print("friends: " + str(i))
    users = members[i]["vk_pages"]
    if (len(users) == 0 or "friends" in users[0].keys()):
        continue 
    for user in users:
        user["friends"] = []
        if (user["is_closed"]):
            continue
        userid=user["id"]
        try:
            friends = [x for x in vk.friends.get(user_id=userid,)["items"] if (x in all_ids)]
            user["friends"] = friends
        except:
            user["friends"] = []
        time.sleep(PAUSE_TIME)

    members[i]["vk_pages"] = users  
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        with open('output/members.txt', 'w') as f:
            print(json.dumps(members, ensure_ascii=False, indent=4), file=f)


with open('output/members.txt', 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)

print("Done")
