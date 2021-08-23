import openpyxl
from pathlib import Path
import json
import re

def format_spaces(string):
    if (isinstance(string, str)):
        return " ".join(string.split())
    return string

def log(string):
    print("__LOG__: " + str(string))

def find_substring(sheet, string):
    ret = []
    for i in range(1, 3):
        for j in range(1, 50):
            if (isinstance(sheet.cell(i, j).value, str) and format_spaces(sheet.cell(i, j).value.lower()).find(string.lower()) != -1):
                ret += [(i, j)]
    return ret

def find_format(sheet):
    col = {}
    row = -1
    for field in fields:
        lst = find_substring(sheet, field["substring"])
        if (len(lst) != 1 or (row != -1 and row != lst[0][0])):
            log(field["substring"] + ": " + str(lst))    
            return -1, {}
        row = lst[0][0]
        col[field["field"]] = lst[0][1]
    return row, col

def find_number(string):
    start = -1
    end = -2
    for i in range(len(string)):
        if ('0' <= string[i]  and string[i] <= '9'):
            end = i
            if (start == -1):
                start = i
    return string[start : end + 1]

def find_user_id(userlist, user):
    for i in range(len(userlist)):
        if (userlist[i]["name"] == user["name"] and
                userlist[i]["surname"] == user["surname"]):
            return i
    return -1

with open("temp/xlsx_config.txt") as f:
    fields = json.load(f)

xlsx_files = [path for path in Path('./temp/temp').rglob('*.xlsx')]
members = []

for xlsx_file in xlsx_files:
    fname = str(xlsx_file)
    log(fname)
    wb = openpyxl.load_workbook(xlsx_file)
    sheet = wb["Parse"]
    zero_row, column_interpret = find_format(sheet)
    if (zero_row == -1):
        log("Формат не найден")
    else:
        while (True):
            zero_row += 1
            user_dict = {}
            OK = True

            for field in fields:
                col_number = column_interpret[field["field"]]
                value = format_spaces(sheet.cell(zero_row, col_number).value)
                if (field["field"] == "name" or field["field"] == "surname"):
                    if (not isinstance(value, str) or not re.search(field["pattern"], value)):
                        OK = False
                user_dict[field["field"]] = str(value)
         
            if (not OK):
                break            

            user_id = find_user_id(members, user_dict) 
            if (user_id == -1):   
                members += [user_dict]
        log("Обработан")
    print()

print("Обработано: " + str(len(members)))
with open('output/members01.txt', 'w') as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
