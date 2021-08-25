import vk_api
import json
from sigma_parsing.data import *
import time
from cdifflib import CSequenceMatcher
from pathlib import Path

SIMILARITY_LIMIT = 0.93

with open("../members02.txt") as f:
    members = json.load(f)     

for i in range(len(members)):
    member_i_key = members[i]["name"] + members[i]["surname"]
    for j in range(i + 1, len(members)): 
        member_j_key = members[j]["name"] + members[j]["surname"]
        ratio = CSequenceMatcher(None, member_i_key, member_j_key).ratio()
        if (ratio >= SIMILARITY_LIMIT):
            print(member_i_key, member_j_key, ratio)
