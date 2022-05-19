import json
import re
import matplotlib.pyplot as plt
from sigma_parsing.utils import *

import time
import copy

def find_number(string):
    start = -1
    end = -2
    for i in range(len(string)):
        if ('0' <= string[i]  and string[i] <= '9'):
            end = i
            if (start == -1):
                start = i
    return string[start : end + 1]

suffix = ".xlsxout.txt"
members, filename = get_json_by_pattern('output/*xlsxout*txt')
members_oname = get_file_name(filename,suffix)

with open(xlsxconfig_iname) as f:
    columns = json.load(f)

final = []

for member in members:
    OK = True
    for column in columns:
        if (not isinstance(member[column["field_name"]], str)):
            continue
        if (not re.search(column["data_pattern"], member[column["field_name"]]) and column["is_important"]):
            OK = False
    if(OK):
        final += [member]

members = final
for member in members:
    short_school = find_number(member["school"])
    member["school"] = (short_school if len(short_school) != 0 else member["school"])

save_as_json(members, members_oname)
