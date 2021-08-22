import json

with open("output/members.txt") as f:
    members = json.load(f)

for member in members:
    try:
        member.pop("official_page")
    except:
        pass
    try:
        member.pop("processed")
    except:
        pass
    for account in member["vk_pages"]:
        try:
            account.pop("probability")
        except:
            pass

with open("output/members.txt", "w") as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
