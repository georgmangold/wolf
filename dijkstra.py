from queue import PriorityQueue
import osmnx as ox
from itertools import count

def dijkstra(graph, start, target, abort=True, weight='length', **kwargs):

    visited = set()
    cost = {start: 0}
    parent = {start: None}
    todo = PriorityQueue()
    matrix = []
    counter = count() 
    todo.put((0, next(counter),start))
    
    while not todo.empty():

        inner_array = []

        while not todo.empty():
            _, _, vertex = todo.get() # finds lowest cost vertex
            # loop until fresh vertex
            if vertex not in visited: break

        visited.add(vertex)
        
        if vertex == target and abort:
            break
        
        for adjacent, _ in graph._adj[vertex].items():
            
            if adjacent in visited: continue # skip these to save time
            old_cost = cost.get(adjacent, float('inf')) # default to infinity
            new_cost = cost[vertex] + graph.edges[vertex, adjacent, 0][weight]

            if new_cost < old_cost:
                todo.put((new_cost, next(counter), adjacent))
                cost[adjacent] = new_cost
                parent[adjacent] = vertex
            
            # if (vertex, adjacent) not in inner_array:
            inner_array.append([vertex, adjacent])
            # print(i, vertex, "->", adjacent)

            #if adjacent == target:
            #    matrix.append(inner_array)
            #    return matrix, make_path(parent, target)
            
        if(len(inner_array) > 0) and inner_array not in matrix:
            matrix.append(inner_array)

    return matrix, make_path(parent, target)

def make_path(parent, target):
    path = []

    if target not in parent:
        return path
    
    v = target
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]