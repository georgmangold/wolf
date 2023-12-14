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
    
    # Haben schon die Kosten anhand des aktuellen Gewichts,
    # wollen aber immer die Länge und Dauer:
    length = {start: 0}
    travel_time = {start: 0}
    
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
                
                # Immer Länge und Dauer sammeln
                length[adjacent] = length[vertex] + graph.edges[vertex, adjacent, 0]["length"]
                travel_time[adjacent] = travel_time[vertex] + graph.edges[vertex, adjacent, 0]["travel_time"]

            
            # if (vertex, adjacent) not in inner_array:
            inner_array.append([vertex, adjacent])
            # print(i, vertex, "->", adjacent)

            #if adjacent == target:
            #    matrix.append(inner_array)
            #    return matrix, make_path(parent, target)
            
        if(len(inner_array) > 0) and inner_array not in matrix:
            matrix.append(inner_array)

    return matrix, make_path(parent, target), cost.get(target, 0), length.get(target, 0), travel_time.get(target, 0)

def make_path(parent, target):
    path = []

    if target not in parent:
        return path
    
    v = target
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]

if __name__ == "__main__":
        ## Bbox vom Start
        north, south, east, west = 50.32942276889266, 50.32049083973944, 11.944606304168701, 11.929510831832886
        
        ## create network from that bounding box
        G = ox.graph_from_bbox(north, south, east, west, network_type="drive")
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        #295704008
        #295704255
        print("greedy")
        matrix, path, cost, length, time = dijkstra(G,379493008, 295704255, abort=False, weight='length')
        print(len(matrix))
        print(path)
        print(cost)
        print(length)
        print(time)