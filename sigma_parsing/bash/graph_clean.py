import json

files = [path for path in Path('./output').rglob('members04*.txt')]
if (len(files) >= 1):
    print("Type a number:")
    for i in range(len(files)):
        print(i, ":", files[i])
    i = int(input())
    filename = files[i % len(files)]
    with open(filename) as f:
        members = json.load(f) 
else:
    print("No file")
    quit()


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

with open(filename, "w") as f:
    print(json.dumps(members, ensure_ascii=False, indent=4), file=f)
