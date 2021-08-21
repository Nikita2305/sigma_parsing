import json

with open("output/members.txt") as f:
    members = json.load(f)

for member in members:
    member.pop("official_page")
    member.pop("processed")
    for account in member["vk_pages"]:
        account.pop("probability")

with open("output/members.txt", "w") as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
