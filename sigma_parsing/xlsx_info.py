import json
import re
import matplotlib.pyplot as plt
from pathlib import Path
from sigma_parsing.utils import *

suffix = '.xlsxout.png'
members, filename = get_json_by_pattern("output/*xlsxout*txt")
oname = get_file_name(filename, suffix)

with open("temp/xlsx_config.txt") as f:
    fields = json.load(f)

bug_data = {field["field"]: 0 for field in fields}

for member in members:
    for field in fields:
        try:
            if (re.search(field["pattern"], member[field["field"]])):
                bug_data[field["field"]] += 1
        except Exception:
            pass

for x in bug_data:
    bug_data[x] = bug_data[x] / len(members) * 100

plt.figure()
plt.title("Data cleanness")
plt.ylabel("%")
plt.yticks([i for i in range(0, 101, 10)])
plt.bar(bug_data.keys(), bug_data.values())
plt.savefig(oname)
plt.show()
