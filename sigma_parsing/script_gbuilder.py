import json
from threading import *
import vk_api
from sigma_parsing.data import *
import time

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()

vk = vk_session.get_api()

with open("output/members.txt") as f:
    members = json.load(f)

users = []
i = 0
for member in members:
    i += 1
    print(i)
    if (i == 10):
        break
    users += vk.users.search(
        q=member["name"] + " " + member["surname"],
        count=5,
        city=104,
        age_from=12,
        age_to=19
    )["items"]
    time.sleep(0.3)
    users += vk.users.search(
        q=member["name"] + " " + member["surname"],
        count=5,
        city=104
    )["items"]
    time.sleep(0.3)

temp = []
ids = []
for user in users:
    if (not user["id"] in ids):
        ids += [user["id"]]
        temp += [user]
users = temp
    
with open('output/graph.txt', 'w') as f:
    print(json.dumps(users, ensure_ascii=False, indent=4), file=f)

