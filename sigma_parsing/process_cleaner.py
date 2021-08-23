import json
import sys

filename = "output/members.txt"

if len(sys.argv) >= 2:
    filename = sys.argv[1]

with open(filename) as f:
    members = json.load(f)

for member in members:
    member.pop("official_page")
    member.pop("processed")
    for account in member["vk_pages"]:
        account.pop("probability")

with open(filename, "w") as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
