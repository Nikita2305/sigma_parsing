import json
import openpyxl
import sys
from pathlib import Path

def getstr(var):
    if (isinstance(var, str)):
        return var
    return ""

def is_official(members, user_id):
    for member in members:
        if (member["processed"] and member["official_page"]["id"] == user_id):
            return True
    return False

filename = "output/members.txt"

if len(sys.argv) >= 2:
    filename = sys.argv[1]

with open(filename) as f:
    users = json.load(f)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Edges"
ws["A1"] = "Source"
ws["B1"] = "Target"
ws["C1"] = "Type"
edge = 2
ids = []
for user in users:
    if (len(user["official_page"]) == 0):
        if(len(user["vk_pages"]) != 0):
            for acc in user["vk_pages"]:
                if(acc["id"] == int(user["vk_id"])):
                    user["processed"] = True
                    user["official_page"] = acc
                    user["special_case"] = True
                    print(acc)
                    break
    if (not user["processed"]):
        continue
    account = user["official_page"]
    id1 = account["id"]
    if (id1 in ids):
        continue
    ids += [id1]
    for id2 in account["friends"]:
        if (not is_official(users,id2)):
            continue
        ws["A"+str(edge)] = str(id1)
        ws["B"+str(edge)] = str(id2)
        ws["C"+str(edge)] = "Undirected"
        edge += 1

ws = wb.create_sheet("Vertices")
ws["A1"] = "Id"
ws["B1"] = "Label"
ws["C1"] = "Olymps"
ws["D1"] = "School"
ws["E1"] = "SpecialCase"
usr = 2
ids = []

print("=================")

for user in users:
    if (not user["processed"]):
        continue
    account = user["official_page"]
    id1 = account["id"]
    if (id1 in ids):
        continue
    ids += [id1]
    ws["A"+str(usr)] = str(id1)
    ws["B"+str(usr)] = getstr(user["name"]) + " " + getstr(user["surname"])
    ws["C"+str(usr)] = ""
    ws["D"+str(usr)] = getstr(user["school"])
    ws["E"+str(usr)] = 1 if "special_case" in user else 0
    usr += 1
wb.save("output/graph.xlsx")
