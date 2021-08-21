import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

with open("output/members.txt") as f:
    members = json.load(f)

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


active2 = {}
for l in lst:
    pair = (l[0][0], (l[0][1] if len(l[0]) > 1 else 0))
    active2[pair] = (active2[pair] if pair in active2 else 0) + 1
active2.pop((0,0))
active2.pop((1,0))

X = np.array([x[0] for x in active2.keys()])
Y = np.array([x[1] for x in active2.keys()])
Z = np.array(list(active2.values()))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=20, azim=250)

ax.set_xlabel("M1")
ax.set_xlim(15)
ax.set_ylabel("M2")
ax.set_ylim(15)
ax.set_zlabel("Number of people")
ax.set_title("All pairs (M1, M2), except (0, 0) and (1, 0)")

surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm)
plt.savefig("output/M1_M2.png")
plt.show()
plt.clf()
