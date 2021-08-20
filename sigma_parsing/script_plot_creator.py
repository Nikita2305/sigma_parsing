'''
active = {}
for i in range(-1,80):
    active[i] = 0

lst = []
for member in members:
    if (len(member["vk_pages"]) == 0):
        active[-1] = active[-1] + 1
        continue
    l = [len(account["friends"]) for account in member["vk_pages"]]
    l.sort()
    l = l[::-1]
    lst += [(l, getstr(member["surname"]) + " " + getstr(member["name"]))]

lst.sort()

plt.bar(active.keys(), active.values())
plt.savefig("output/plot.png")

for l in lst:
    print(l)
'''
