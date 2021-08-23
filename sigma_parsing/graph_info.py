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

files = [path for path in Path('./output').rglob('members03*.txt')]
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


active = {}
for i in range(-1,1000):
    active[i] = 0

lst = []
for member in members:
    if (len(member["vk_pages"]) == 0):
        active[-1] = active[-1] + 1
        continue
    l = [len(account["friends"]) for account in member["vk_pages"]]
    l.sort()
    l = l[::-1]
    lst += [(l, getstr(member["surname"]) + " " + getstr(member["name"]))]
lst.sort()

for l in lst:
    active[l[0][0]] = active[l[0][0]] + 1 

keys = list(active.keys())[:50]
values = list(active.values())[:50]
plt.bar(keys, values)
plt.ylabel("Number of people")
plt.xlabel("M1")
plt.savefig("output/research03_1.png")
plt.clf()

keys = list(active.keys())[:50]
values = list(active.values())[:50]
for i in reversed(range(1, len(keys))):
    values[i - 1] += values[i]
plt.bar(keys, values)
plt.ylabel("Number of people(cumulative)")
plt.xlabel("M1")
plt.savefig("output/research03_2.png")
plt.clf()

X = np.array([l[0][0] for l in lst])
Y = np.array([(l[0][1] if len(l[0]) > 1 else 0) for l in lst])

fig, ax = plt.subplots()
hist, xbins, ybins, im = ax.hist2d(X, Y, bins=(30,30), range=[(0,30),(0,30)], cmin=1)

for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        ax.text(xbins[j]+0.5,ybins[i]+0.5, hist.T[i,j], 
                color="w", ha="center", va="center", fontweight="bold")

plt.show()
plt.clf()
