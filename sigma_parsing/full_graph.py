import json
import sys
import functools
from sklearn import tree
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import export_text
from igraph import *    # pip install python-igraph
from scipy.optimize import minimize
from scipy.special import factorial
from scipy import stats
from sigma_parsing.utils import *

suffix = ".final_graph.png"
members, filename = get_json_by_pattern("output/*processed*txt")
members_oname = get_file_name(filename,suffix)

counter = set()
for member in members:
    for account in member["vk_pages"]:
        counter.add(account["id"])

graph = Graph(n=len(counter))
graph.vs["vkid"] = list(counter)

edges = set()

for member in members:
    for account in member["vk_pages"]:
        index = graph.vs.select(vkid=account["id"])[0].index
        for friend in account["friends"]:
            if(not friend in counter):
                print(friend)
            idx2 = graph.vs.select(vkid=friend)[0].index
            if(not (index,idx2) in edges and not (idx2,index) in edges):
                edges.add((index,idx2))

graph.add_edges(edges)

nfriends = graph.degree()

print(graph.vs.select(_degree=graph.maxdegree())["vkid"])
#fig, ax = plt.subplots()
#layout = graph.layout("kk")
#plot(graph, layout=layout, target=ax)
#plt.show()

KEEP_COMPONENTS_WITH_GREATER_SIZE = 50

subgraphs_to_del = [x for x in graph.components().subgraphs() if len(x.vs) <= KEEP_COMPONENTS_WITH_GREATER_SIZE]
vert_to_del = set()
for g in subgraphs_to_del:
    for vkid in g.vs["vkid"]:
        vert_to_del.add(vkid) 

to_delete_ids = [v.index for v in graph.vs if v["vkid"] in vert_to_del]
graph.delete_vertices(to_delete_ids)

print(graph.components().sizes())

#graph.vs["hc"] = graph.harmonic_centrality(normalized=True)
graph.vs["hc"] = graph.personalized_pagerank()

hcmin = min(graph.vs["hc"])
print("min hc: ",hcmin)
hcmax = max(graph.vs["hc"])
print("max hc: ",hcmax)

graph.vs["hc"] = [x/hcmax for x in graph.vs["hc"]]

for member in members:
    accounts = []
    for account in member["vk_pages"]:
        v = graph.vs.select(vkid=account["id"])
        if len(v) > 0:
            accounts.append((account,v[0]))
        else:
            account["colored"] = False
    if len(accounts) == 1:
        accounts[0][0]["colored"] = True
        accounts[0][1]["colored"] = True
        member["colored"] = True
        member["colored_id"] = accounts[0][0]["id"]
    else:
        member["colored"] = False
        for x,v in accounts:
            accounts[0][0]["colored"] = False
            accounts[0][1]["colored"] = False

n = []
m1 = []
m2 = []
m1hc = []
m2hc = []
m1colored = []
m2colored = []



for member in members:
    accounts = []
    for account in member["vk_pages"]:
        v = graph.vs.select(vkid=account["id"])
        if len(v) > 0:
            accounts.append((account,v[0]))
#            nfriends.append(v[0].degree())
    accounts.sort(reverse=True,key=lambda x: x[1].degree())
    n.append(len(accounts))
    if len(accounts) > 0:
        m1.append(accounts[0][1].degree()/30. if len(accounts) > 0 else 0)
        m1hc.append(accounts[0][1]["hc"] if len(accounts) > 0 else 0)
        m1colored.append(len([x for x in accounts[0][1].neighbors() if x["colored"]]) if len(accounts) > 0 else 0)
        m2.append(accounts[1][1].degree()/30. if len(accounts) > 1 else 0)
        m2hc.append(accounts[1][1]["hc"] if len(accounts) > 1 else 0)
        m2colored.append(len([x for x in accounts[1][1].neighbors() if x["colored"]]) if len(accounts) > 1 else 0)

fig, axs = plt.subplots(3,3)
filler_internal = [0,0]
def filler():
    global filler_internal
    nfi = filler_internal
    ofi = tuple(filler_internal)
    nfi[0] += 1
    if nfi[0] == 3:
        nfi[1] += 1
        nfi[0] = 0
    if nfi[1] == 3:
        nfi = [0,0]
    filler_internal = nfi
    return ofi

hist, xbins, im = axs[filler()].hist(n, bins=10, range=(0,10))
#plt.show()

s = sum(hist)
for i in range(len(hist)):
    print(i,": ",hist[i]/s)

def plot_2d(m1,m2,ax,lx="",ly=""):
    hist, xbins, ybins, im = ax.hist2d(m1, m2, bins=(30,30), range=[(0,1),(0,1)], cmin=1)
    for i in range(len(ybins)-1):
        for j in range(len(xbins)-1):
            ax.text((xbins[j]+xbins[j+1])/2.,(ybins[i]+ybins[i+1])/2., int(hist.T[i,j]) if not np.isnan(hist.T[i,j]) else "", 
                    color="w", ha="center", va="center", fontweight="bold", fontsize=5)
    ax.set_xlabel(lx)
    ax.set_ylabel(ly)

def plot_1d(m1,ax,lx=""):
    hist, xbins, im = ax.hist(m1, bins=50, range=(0,1))
    ax.set_xlabel(lx)

plot_2d(m1,m2,axs[filler()],"m1","m2")
plot_2d(m1hc,m2hc,axs[filler()],"m1hc","m2hc")
plot_2d(m1,m1hc,axs[filler()],"m1","m1hc")
plot_2d(m2,m2hc,axs[filler()],"m2","m2hc")
plot_1d(m1hc,axs[filler()],"m1hc")
plot_1d(m2hc,axs[filler()],"m2hc")

nfriends = [x for x in nfriends if x < 30]

#plot_1d(nfriends)

def poisson(k, lamb):
    """poisson pdf, parameter lamb is the fit parameter"""
    return (lamb**k/factorial(k)) * np.exp(-lamb)

def pdf(x, params):
    res = poisson(x, abs(params[0]))
    res += abs(params[1])*poisson(x, abs(params[2]))
    res += abs(params[3])*poisson(x, abs(params[4]))
    #res += params[5]*params[5]*poisson(x, params[6]*params[6])
    return res / (1+abs(params[1])+abs(params[3]))#+params[5]*params[5])

def negative_log_likelihood(params, data):
    """
    The negative log-Likelihood-Function
    """

    lnl = - np.sum(np.log(pdf(data,params)))
    return lnl

# minimize the negative log-Likelihood

result = minimize(negative_log_likelihood,  # function to minimize
                  x0=np.ones(5),            # start value
                  args=(nfriends,),             # additional arguments for function
                  method='Powell',          # minimization method, see docs
                  )
# result is a scipy optimize result object, the fit parameters 
# are stored in result.x
print(result)

# plot poisson-distribution with fitted parameter
x_plot = np.arange(0.5, 29.5)

ax = axs[filler()]
ax.hist(nfriends, bins=30, range=(0,30), density=True, label='Data')
ax.plot(
    x_plot,
    list(map(lambda x: pdf(int(x-0.5),result.x), x_plot)),
    marker='o', linestyle='',
    label='Fit result',
)
ax.legend()

#m1hc_minus_m2hc = list(map(lambda x,y: x-y, m1hc ,m2hc))
m1hc_minus_m2hc = []
for i in range(len(m1hc)):
    if(m2hc[i] != 0):
        m1hc_minus_m2hc.append(m1hc[i]-m2hc[i])
hist, xbins, im = axs[filler()].hist(m1hc_minus_m2hc, bins=75, range=(-1,2))


for member in members:
    accounts = []
    for account in member["vk_pages"]:
        v = graph.vs.select(vkid=account["id"])
        if len(v) > 0:
            accounts.append((account,v[0]))
    accounts.sort(reverse=True,key=lambda x: x[1]["hc"])
    if len(accounts) >= 1:
        accounts[0][0]["colored"] = True
        accounts[0][1]["colored"] = True
        member["colored"] = True
        member["colored_id"] = accounts[0][0]["id"]

#for member in members:
    #graph_guess = member["official_page"]["id"] if member["processed"] else -1
    #our_guess = member["colored_id"] if member["colored"] else -1
    #accounts = []
    #for account in member["vk_pages"]:
        #v = graph.vs.select(vkid=account["id"])
        #if len(v) > 0:
            #accounts.append((account,v[0]))
    #accounts.sort(reverse=True,key=lambda x: x[1]["hc"])
    #if(graph_guess != our_guess):
        #print(our_guess," |",member["vk_id"] if "vk_id" in member else "","| ",str(accounts[0][0]["id"])+"<"+str(len(accounts[0][0]["friends"])) if len(accounts) > 0 else ""," ",str(accounts[1][0]["id"])+"<"+str(len(accounts[1][0]["friends"])) if len(accounts) > 1 else ""," processed:",member["official_page"]["id"] if member["processed"] else "NO")

plt.show()
