import json
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
from pathlib import Path
from sigma_parsing.utils import *

suffix = ".friendlists.png"
members, filename = get_json_by_pattern("output/*friendlists*txt")
oname = get_file_name(filename,suffix)

active = {}
for i in range(-1,1000):
    active[i] = 0

lst = []
for member in members:
    # if (member["processed"] or (not member["vk_id"] in [account["id"] for account in member["vk_pages"]])):
        # continue
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
plt.savefig(oname)
oname = get_new_file_name(oname, suffix) 
plt.clf()

keys = list(active.keys())[:50]
values = list(active.values())[:50]
for i in reversed(range(1, len(keys))):
    values[i - 1] += values[i]
plt.bar(keys, values)
plt.ylabel("Number of people(cumulative)")
plt.xlabel("M1")
plt.savefig(oname)
oname = get_new_file_name(oname, suffix)
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
