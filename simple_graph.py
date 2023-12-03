import osmnx as ox
from collections import defaultdict

def simple_graph(graph):
    simple_graph = defaultdict(list)
    seen_edges = defaultdict(int)
    for src, dst, raw_data in graph.edges(data=True):
        weight = raw_data['length']
        seen_edges[(src, dst, weight)] += 1
        if seen_edges[(src, dst, weight)] > 1:  # checking for duplicated edge entries
            continue
        simple_graph[src].append((dst, weight))
    return simple_graph

def print_true(graph):
    i = 0
    for edge in graph.edges(data=True):
        i+=1
        print(i, "->", edge)

def print_nodes(graph):
    i = 0
    for node in graph.nodes():
        i+=1
        for adjacent, data in graph._adj[node].items():
            print(i, node, "->", adjacent, ":", data[0]#['length']
            )

def print_node_xy(graph):
    i = 0
    for node, data in graph.nodes(data=True):
        i+=1
        print(i, node, "x =", data['x'], "y =", data['y'])

def print_edges(graph):
    i = 0
    for node, adj, weight in graph.edges(data='length', default=1):
        i+=1
        print(i, node, "->", adj, ":", weight)