import json
import sys
import functools

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

filename = "output/members.txt"

if len(sys.argv) >= 2:
    filename = sys.argv[1]

with open(filename) as f:
    members = json.load(f)

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

#print(functools.reduce(lambda x,l : x+(1 if (l[0][1] if len(l[0]) > 1 else 0) > 0 else 0),lst,0))

print("total:",total)
print("selected_but_not_match:",selected_but_not_match)
print("selected_and_match:",selected_and_match)
print("not_selected:",not_selected)
print("not_selected_but_search_successful:",not_selected_but_search_successful)

print("m2>0 ",len([l for l in lst if (l[0][1] if len(l[0]) > 1 else 0) > 0]))
