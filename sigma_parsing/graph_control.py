import json
import sys
import functools
from pathlib import Path
import matplotlib.pyplot as plt

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

files = [path for path in Path('./output').rglob('members04*.txt')]
if (len(files) >= 1):
    print("Type a number:")
    for i in range(len(files)):
        print(i, ":", files[i])
    i = int(input())
    filename = files[i % len(files)]
    with open(filename) as f:
        members = json.load(f) 
else:
    print("No file")
    quit()


total = 0;
selected_but_not_match = 0;
selected_and_match = 0;
not_selected = 0;
not_selected_but_search_successful = 0;

lst = []
for member in members:
    if (not "vk_id" in member):
        continue
    total += 1
    if (len(member["official_page"]) == 0):
        not_selected += 1
        if(len(member["vk_pages"]) != 0):
            for acc in member["vk_pages"]:
                if(acc["id"] == int(member["vk_id"])):
                    not_selected_but_search_successful += 1
                    break
    elif (member["official_page"]["id"] == int(member["vk_id"])):
        print("== ",member["official_page"]["id"]," ",int(member["vk_id"]))
        selected_and_match += 1
    else:
        print("!= ",member["official_page"]["id"]," ",int(member["vk_id"]))
        selected_but_not_match +=1
    if (len(member["vk_pages"]) != 0):
        l = [len(account["friends"]) for account in member["vk_pages"]]
        l.sort()
        l = l[::-1]
        lst += [(l, getstr(member["surname"]) + " " + getstr(member["name"]))]
lst.sort()

dct = { "selected_but_not_match": selected_but_not_match,
        "selected_and_match": selected_and_match, 
        "not_selected_not_found": not_selected - not_selected_but_search_successful,
        "not_selected_but_search_successful": not_selected_but_search_successful}

print(dct)

fig1, ax1 = plt.subplots()
plt.title("Control stats")
wedges, texts, autotexts = ax1.pie(dct.values(), labels=dct.keys(), autopct='%1.2f%%')
ax1.axis('equal')
fig1.set_size_inches(12, 8.5)
plt.savefig("output/research04.png")
plt.show()

print("m2>0 ",len([l for l in lst if (l[0][1] if len(l[0]) > 1 else 0) > 0]))
