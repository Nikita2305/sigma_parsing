import vk_api
import json
from sigma_parsing.data import *
import time
from cdifflib import CSequenceMatcher
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

SIMILARITY_LIMIT = 0.93

with open("../accounts.txt") as f:
    accounts = json.load(f)     

x = np.array([len(account["friends"]) for account in accounts if "friends" in account])
print(sum(x) / len(x))

fig,ax = plt.subplots()
hist, xbins, im = ax.hist(x, bins=100, range=(0,1000))
plt.ylabel("Number of people")
plt.xlabel("size(friends)")
plt.yscale('log', nonpositive='clip')
plt.show()

