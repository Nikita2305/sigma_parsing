import json
import sys
import functools
from sklearn import tree
import numpy as np
from sklearn.tree import export_text

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

def to_features(member):
    feat = []
    feat.append(len(member["vk_pages"]))
    l = [(len(account["friends"]), not account["is_closed"] or account["can_access_closed"]) for account in member["vk_pages"]]
    l.sort(reverse=True)
    feat.append(l[0][0] if len(l) > 0 else 0)
    feat.append(l[1][0] if len(l) > 1 else 0)
    feat.append(1 if len(l) > 0 and l[0][1] else 0)
    feat.append(1 if len(l) > 1 and l[1][1] else 0)
    return feat
    
def to_class(member):
    vk_id = member["vk_id"]
    pages = member["vk_pages"]
    if(len(pages) >= 2 and pages[1]["id"] == vk_id):
        return "M2-case"
    elif(len(pages) >= 1 and pages[0]["id"] == vk_id):
        return "M1-case"
    else:
        return "Undefined"

x = [to_features(member) for member in members]
y = [to_class(member) for member in members]

clf = tree.DecisionTreeClassifier(max_depth=6)
clf = clf.fit(x, y)

r = export_text(clf, feature_names=["n","m1","m2","open1","open2"])
print(r)

if len(sys.argv) >= 3:
    filename2 = sys.argv[2]
    with open(filename2) as f:
        members2 = json.load(f)
    for mem in members2:
        if not mem["processed"]:
            continue
        res = clf.predict_proba([to_features(mem)])
        l = [(len(account["friends"]), not account["is_closed"] or account["can_access_closed"],account["id"]) for account in mem["vk_pages"]]
        l.sort(reverse=True, key = lambda tup : (tup[0],tup[1]))
        print(res," ",l[0][2] if len(l) > 0 else ""," ",l[1][2] if len(l) > 1 else ""," processed:",mem["official_page"]["id"] if mem["processed"] else "NO")
