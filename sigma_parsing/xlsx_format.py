import json
import re
import matplotlib.pyplot as plt
from sigma_parsing.utils import *

# from sigma_parsing.vk import *
from vk_parsing.exceptions import StopParsingError

import time
import copy

def append_member(response, array, obj):
    if (len(response) == 0):
        return
    obj["vk_id"] = response[0]["id"]
    array.append(obj)

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
vk = getParserInstance()

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
final_final = []
print("Waiting Time: " + str(len([member for member in members if not isinstance(member["vk_id"], int)])) + "s")
i = 0
SAVING_EVERY = 100
for member in members:
    i += 1
    print("id found:" + str(i))
    if (isinstance(member["vk_id"], int)):
        continue
    if (i % SAVING_EVERY == SAVING_EVERY - 1):
        save_as_json(final_final, members_oname)
    short_school = find_number(member["school"])
    member["school"] = (short_school if len(short_school) != 0 else member["school"])
    short_name = member["vk_id"][member["vk_id"].rfind("/") + 1:]
    try:
        vk.add_task("users.get",
            {"user_ids": short_name},
            append_member,
            (final_final, copy.deepcopy(member))
        )
    except StopParsingError as ex:
        print(f"stop: {ex}")
        quit()
    except Exception as ex:
        print(f"ignore: {ex}")

try:
    vk.execute_tasks()
except StopParsingError as ex:
    print(f"stop: {ex}")
    quit()
except Exception as ex:
    print(f"ignore: {ex}")

save_as_json(final_final, members_oname)
