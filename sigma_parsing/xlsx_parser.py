import openpyxl
from pathlib import Path
import json
import re
from sigma_parsing.utils import *

def format_spaces(string):
    if (isinstance(string, str)):
        return " ".join(string.split())
    return string

def log(string):
    print("__LOG__: " + str(string))

def find_cell_with_pattern(sheet, pattern):
    ret = []
    for i in range(1, 3):
        for j in range(1, 50):
            if (isinstance(sheet.cell(i, j).value, str) and re.search(pattern,
                                        format_spaces(sheet.cell(i, j).value.lower()))):
                ret += [(i, j)]
    return ret

def find_format(sheet):
    col = {}
    row = -1
    for column in columns:
        lst = find_cell_with_pattern(sheet, column["cell_pattern"])
        if (len(lst) != 1 or (row != -1 and row != lst[0][0])):
            log(column["cell_pattern"] + ": " + str(lst))    
            return -1, {}
        row = lst[0][0]
        col[column["field_name"]] = lst[0][1]
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

suffix = '.xlsxout.txt'
members_oname = get_file_name("output/members", suffix)

with open(xlsxconfig_iname) as f:
    columns = json.load(f)

xlsx_files = [path for path in Path(xlsx_path).rglob('*.xlsx')]
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

            for column in columns:
                col_number = column_interpret[column["field_name"]]
                value = format_spaces(sheet.cell(zero_row, col_number).value)
                if (column["field_name"] == "name" or
                                column["field_name"] == "surname"):
                    if (not isinstance(value, str) or not re.search(column["data_pattern"], value)):
                        OK = False
                user_dict[column["field_name"]] = str(value)
         
            if (not OK):
                break            

            user_id = find_user_id(members, user_dict) 
            if (user_id == -1):   
                members += [user_dict]
        log("Обработан")
    print()

print("Обработано: " + str(len(members)))
save_as_json(members, members_oname)
