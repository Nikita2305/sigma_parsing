import json
import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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

with open(filename) as f:
    members = json.load(f)

lst = []
for member in members:
    if (len(member["vk_pages"]) == 0):
        continue
    l = [len(account["friends"]) for account in member["vk_pages"]]
    l.sort()
    l = l[::-1]
    lst += [(l, getstr(member["surname"]) + " " + getstr(member["name"]))]

print(len(members))
print(len(lst))

X = np.array([l[0][0] for l in lst])
Y = np.array([(l[0][1] if len(l[0]) > 1 else 0) for l in lst])
Z = np.array([len(l[0]) for l in lst])

fig, ax = plt.subplots()
hist, xbins, ybins, im = ax.hist2d(X, Y, bins=(30,30), range=[(0,30),(0,30)], cmin=1)

for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        ax.text(xbins[j]+0.5,ybins[i]+0.5, hist.T[i,j], 
                color="w", ha="center", va="center", fontweight="bold")

plt.savefig("output/M1_M2.png")
plt.show()
plt.clf()

fig, ax = plt.subplots()
hist, xbins, im = ax.hist(X, bins=30, range=(0,30))

plt.savefig("output/M1.png")
plt.show()
plt.clf()

fig, ax = plt.subplots()
hist, xbins, im = ax.hist(Y, bins=30, range=(0,30))

plt.savefig("output/M2.png")
plt.show()
plt.clf()

fig, ax = plt.subplots()
hist, xbins, im = ax.hist(Z, bins=10, range=(0,10))

plt.savefig("output/N.png")
plt.show()
plt.clf()
