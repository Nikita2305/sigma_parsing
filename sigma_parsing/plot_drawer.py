import json
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

filename = "output/members.txt"

if len(sys.argv) >= 2:
    filename = sys.argv[1]

with open(filename) as f:
    members = json.load(f)

active = {}
for i in range(-1,1000):
    active[i] = 0

lst = []
for member in members:
    if (not "vk_id" in member):
        continue
    if (len(member["official_page"]) == 0):
        if(len(member["vk_pages"]) != 0):
            for acc in member["vk_pages"]:
                if(acc["id"] == int(member["vk_id"])):
                    if (len(member["vk_pages"]) == 0):
                        active[-1] = active[-1] + 1
                        continue
                    l = [len(account["friends"]) for account in member["vk_pages"]]
                    l.sort()
                    l = l[::-1]
                    lst += [(l, getstr(member["surname"]) + " " + getstr(member["name"]))]
                    break
lst.sort()

for l in lst:
    active[l[0][0]] = active[l[0][0]] + 1 

keys = list(active.keys())[:50]
values = list(active.values())[:50]
plt.bar(keys, values)
plt.ylabel("Number of people")
plt.xlabel("M1")
plt.savefig("output/M1.png")
plt.clf()

keys = list(active.keys())[:50]
values = list(active.values())[:50]
for i in reversed(range(1, len(keys))):
    values[i - 1] += values[i]
plt.bar(keys, values)
plt.ylabel("Number of people(cumulative)")
plt.xlabel("M1")
plt.savefig("output/M1_cumulative.png")
plt.clf()

X = np.array([l[0][0] for l in lst])
Y = np.array([(l[0][1] if len(l[0]) > 1 else 0) for l in lst])

fig, ax = plt.subplots()
hist, xbins, ybins, im = ax.hist2d(X, Y, bins=(30,30), range=[(0,30),(0,30)], cmin=1)

for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        ax.text(xbins[j]+0.5,ybins[i]+0.5, hist.T[i,j], 
                color="w", ha="center", va="center", fontweight="bold")


plt.savefig("output/M1_M2.png")
plt.show()
plt.clf()
