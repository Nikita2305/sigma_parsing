import json
import os

with open("output/members.txt") as f:
    members = json.load(f)

size = 5
for member in members:
    if (not "processed" in member):
        continue
    if (member["processed"] and member["official_page"]["probability"] == 1):
        os.system("google-chrome vk.com/id" + str(member["official_page"]["id"]))
        size -= 1
        if (size == 0):
            quit()
