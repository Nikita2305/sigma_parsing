import json
from sigma_parsing.vk import *
import networkx as nx

vk = vk_collection()
group_ids = ["sigma_omsk", "happydevlite"]

def append_group_members(response, array):
    if (len(response["items"]) == 0):
        return False
    for member in response["items"]:
        array.append(member)
    return True

def add_edges(response, members, member, G, results):
    results[str(member)] = []
    for friend in response["items"]:
        if friend in members:
            results[str(member)].append(str(friend))
            G.add_edge(str(member), str(friend))

for group_id in group_ids: 
    print("LOG: " + group_id)
    try:
        with open("output/" + group_id + ".txt", "r") as f:
            results = json.load(f)
    except:
        results = {}
    G = nx.Graph()
    if (len(results) == 0):
        members = []
        i = 0
        while (True):
            print(i * 1000)
            ok = vk.direct_call(
                            "groups.getMembers",
                            {"group_id": group_id,
                            "count": 1000,
                            "offset": i * 1000},
                            append_group_members,
                            array=members
            )
            i += 1
            if not ok:
                break
        print("done downloading " + group_id)
        for member in members:
            vk.add_task(
                        "friends.get",
                        {"user_id": member},
                        add_edges,
                        members=members,
                        member=member,
                        G=G,
                        results=results
            )
        vk.execute_tasks()
        with open("output/" + group_id + ".txt", "w") as f:
            print(json.dumps(results, ensure_ascii=False, indent=4), file=f)           
    else:
        for member in results:
            for friend in results[member]:
                G.add_edge(str(member), str(friend))
    
    # -- Graph statistics -- 
    print(G.number_of_nodes())
    print(nx.average_clustering(G)) 
    # print(json.dumps(nx.algorithms.cluster.clustering(G), ensure_ascii=False, indent=4))
    
    # -- Community searching algorithms --
    # lst = nx.algorithms.community.centrality.girvan_newman(G) 
    # print(json.dumps([sorted(c) for c in next(lst)], ensure_ascii=False, indent=4)) 

    # lst = nx.algorithms.community.modularity_max.greedy_modularity_communities(G)
    # print(json.dumps([str(x) for x in lst], ensure_ascii=False, indent=4))
    
    # lst = nx.algorithms.community.label_propagation.label_propagation_communities(G)   
    # print(json.dumps([str(x) for x in lst], ensure_ascii=False, indent=4))
