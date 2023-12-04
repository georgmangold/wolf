import simple_graph as sg
from queue import PriorityQueue
import osmnx as ox

def dijkstra(G, start, target, abort=True):

    G = sg.simple_graph(G)

    visited = set()
    cost = {start: 0}
    parent = {start: None}
    todo = PriorityQueue()
    matrix = []

    todo.put((0, start))
    i = 0
    while not todo.empty():

        inner_array = []

        while not todo.empty():
            _, vertex = todo.get() # finds lowest cost vertex
            # loop until fresh vertex
            if vertex not in visited: break
            else: # if todo ran out
                break # quit main loop
        visited.add(vertex)
        
        if vertex == target and abort:
            break
        
        for adjacent, weight in G[vertex]:
            
            if adjacent in visited: continue # skip these to save time
            old_cost = cost.get(adjacent, float('inf')) # default to infinity
            new_cost = cost[vertex] + weight

            if new_cost < old_cost:
                todo.put((new_cost, adjacent))
                cost[adjacent] = new_cost
                parent[adjacent] = vertex
            
            # if (vertex, adjacent) not in inner_array:
            inner_array.append([vertex, adjacent])
            # print(i, vertex, "->", adjacent)
            i+=1

        if(len(inner_array) > 0) and inner_array not in matrix:
            matrix.append(inner_array)

    return parent, matrix

def make_path(parent, target):
    if target not in parent:
        return None
    v = target
    path = []
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]