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
    for i in range(1, 20):
        for j in range(1, 50):
            if (isinstance(sheet.cell(i, j).value, str) and
                    re.search(pattern, format_spaces(sheet.cell(i, j).value.lower()))):
                    # pattern == ):
                ret += [(i, j)]
    return ret

def find_format(sheet):
    col = {}
    mn = 1000000
    mx = -1
    for column in columns:
        lst = find_cell_with_pattern(sheet, column["cell_pattern"])
        log(lst)
        if (len(lst) != 1):
            log(column["cell_pattern"] + ": " + str(lst))    
            return -1, {}
        mn = min(lst[0][0], mn)
        mx = max(lst[0][0], mx)
        col[column["field_name"]] = lst[0][1]
    if (mx - mn > 1):
        return -1, {}
    return mx, col

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

def find_olymp(olymplist, olymp):
    for x in olymplist:
        if (x["olymp"] == olymp["olymp"]):
            return True
    return False 

suffix = '.xlsxout.txt'
members_oname = get_file_name("output/members", suffix)

with open(xlsxconfig_iname) as f:
    columns = json.load(f)

xlsx_files = [path for path in Path(xlsx_path).rglob('*.xlsx')]
members = []

for xlsx_file in xlsx_files:
    fname = str(xlsx_file)
    subject = fname[fname.find('_')+1:fname.rfind('.xlsx')]
    wb = openpyxl.load_workbook(xlsx_file)
    for sheet in wb:
        description = format_spaces(sheet.title)
        class_number = find_number(description)  
        log(subject + ", class:" + class_number)
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
          
                event_dict = {"olymp": subject, "class": class_number, "status": user_dict["status"]}
                # user_dict["status"] = "just not empty string"

                user_id = find_user_id(members, user_dict) 
                if (user_id == -1):   
                    user_dict["diplomas"] = [event_dict]
                    members += [user_dict]
                else:
                    if (not find_olymp(members[user_id]["diplomas"], event_dict)):
                        members[user_id]["diplomas"] += [event_dict]
            log("Обработан")
    print()

print("Обработано: " + str(len(members)))
save_as_json(members, members_oname)
