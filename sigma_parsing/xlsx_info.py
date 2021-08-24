import json
import re
import matplotlib.pyplot as plt
from pathlib import Path

files = [path for path in Path('./output').rglob('members01*.txt')]
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


with open("temp/xlsx_config.txt") as f:
    fields = json.load(f)

bug_data = {field["field"]: 0 for field in fields}

for member in members:
    for field in fields:
        try:
            if (re.search(field["pattern"], member[field["field"]])):
                bug_data[field["field"]] += 1
        except Exception:
            pass
'''
for member in members:
    if (member["vk_id"].find("vk.com") == -1):
        continue
    short_school = find_number(member["school"])
    member["school"] = (short_school if len(short_school) != 0 else member["school"])
    member["vk_id"] = member["vk_id"][member["vk_id"].rfind("/") + 1:]
'''
 
for x in bug_data:
    bug_data[x] = bug_data[x] / len(members) * 100

plt.figure()
plt.title("Data cleanness")
plt.ylabel("%")
plt.yticks([i for i in range(0, 101, 10)])
plt.bar(bug_data.keys(), bug_data.values())
plt.savefig("output/research01.png")
plt.show()
