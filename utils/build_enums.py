import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

g = nx.Graph()
g.add_node('1000', x=10,y=11,size=10)
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
nx.draw_networkx(g, ax=ax)

nodes = [{'name': str(i), 'club': g.node[i]['club']}
         for i in g.nodes()]
links = [{'source': u[0], 'target': u[1]}
         for u in g.edges()]
with open('graph.json', 'w') as f:
    json.dump({'nodes': nodes, 'links': links}, f, indent=4,)