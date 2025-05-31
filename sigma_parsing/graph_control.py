import json
import sys
import functools
from pathlib import Path
import matplotlib.pyplot as plt
import copy
import os
from threading import Thread
from sigma_parsing.utils import *

def execute_string(string):
     T = Thread(target=os.system, args = (string,))
     T.start()

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

suffix = ".processed.png"
members, filename = get_json_by_pattern("output/*processed*txt")
oname = get_file_name(filename, suffix)

# ============= ID STATS ================

dct_id = { "selected_but_not_match": set(),
        "selected_and_match": set(), 
        "not_selected_not_found": set(),
        "not_selected_but_search_successful": set()}
dct_sch = copy.deepcopy(dct_id)

lst = []
for i in range(len(members)):
    member = members[i]
    if (not "vk_id" in member):
        continue
    if (len(member["official_page"]) == 0):
        OK = False
        if(len(member["vk_pages"]) != 0):
            for acc in member["vk_pages"]:
                if(acc["id"] == int(member["vk_id"])):
                    OK = True 
                    break
        if (OK):
            dct_id["not_selected_but_search_successful"].add(i)
        else:
            dct_id["not_selected_not_found"].add(i)
    elif (member["official_page"]["id"] == int(member["vk_id"])):
        print("== ",member["official_page"]["id"]," ",int(member["vk_id"]))
        dct_id["selected_and_match"].add(i)
    else:
        print("!= ",member["official_page"]["id"]," ",int(member["vk_id"]))
        dct_id["selected_but_not_match"].add(i)
    if (len(member["vk_pages"]) != 0):
        l = [len(account["friends"]) for account in member["vk_pages"]]
        l.sort()
        l = l[::-1]
        lst += [(l, getstr(member["surname"]) + " " + getstr(member["name"]))]
lst.sort()

# for i in dct_id["not_selected_not_found"]:
    # print(members[i]["name"] + " " + members[i]["surname"])
    # os.system("nohup google-chrome vk.com/id" + str(members[i]["vk_id"]))
# quit()

print("Stat by Id:" + str(dct_id))

fig1, ax1 = plt.subplots()
plt.title("Control stats by Id(more precise)")
values = [len(dct_id[key]) for key in dct_id.keys()]
wedges, texts, autotexts = ax1.pie(values, labels=dct_id.keys(), autopct=make_autopct(values))
ax1.axis('equal')
fig1.set_size_inches(12, 8.5)
plt.savefig(oname)
plt.show()
plt.clf()

# ================== SCHOOL STATS ====================

for i in range(len(members)):
    member = members[i]
    try:
        int(member["school"])
    except Exception:
        pass
        # continue
    if (len(member["official_page"]) == 0 or
                    (not "schools" in member["official_page"]) or
                    len(member["official_page"]["schools"]) == 0):
        if (len(member["official_page"]) == 0):
            such_school = 0
            for account in member["vk_pages"]:
                if (not "schools" in account):
                    continue
                such_school += len([1 for school in account["schools"] if
                                            (school["name"].find(member["school"]) != -1)])
            if (such_school > 0):
                dct_sch["not_selected_but_search_successful"].add(i)
            
    elif (len([1 for school in member["official_page"]["schools"] if (school["name"].find(member["school"]) != -1)]) > 0):
        print("== ",member["official_page"]["id"]," ",int(member["vk_id"]))
        dct_sch["selected_and_match"].add(i)
    else:
        print("!= ",member["official_page"]["id"]," ",int(member["vk_id"]))
        dct_sch["selected_but_not_match"].add(i)
 

print("Stat by School:" + str(dct_sch))

fig1, ax1 = plt.subplots()
plt.title("Control stats by school(less precise)")
values = [len(dct_sch[key]) for key in dct_sch.keys()]
wedges, texts, autotexts = ax1.pie(values, labels=dct_sch.keys(), autopct=make_autopct(values))
ax1.axis('equal')
fig1.set_size_inches(12, 8.5)
plt.show()
plt.clf()


# ===================== Comparing Stats =======================

keys = []
values = []
for key1 in dct_id.keys():
    for key2 in dct_sch.keys():
        keys += [key2 + "\n" + key1]
        values += [len(dct_id[key1] & dct_sch[key2])]
keys1 = []
values1 = []

print("Comparing: ")
print()
for i in range(len(keys)):
    if (values[i] != 0):
        keys1 += [keys[i]]
        values1 += [values[i]]
        print(keys[i], ": ", values[i])

fig1, ax1 = plt.subplots()
plt.title("Stats differences in format:\n {School_status}\n {Id_status}")
wedges, texts, autotexts = ax1.pie(values1, labels=keys1, autopct=make_autopct(values1))
ax1.axis('equal')
fig1.set_size_inches(12, 8.5)
plt.show()
plt.clf()

print("M2 > 0: ",len([l for l in lst if (l[0][1] if len(l[0]) > 1 else 0) > 0]), " times")
