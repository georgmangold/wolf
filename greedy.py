from queue import PriorityQueue
import osmnx as ox

from itertools import count

def greedy(graph, start, target, metric='0', weight='length'):
    '''
    GBFS(Graph G, Vertex s, Vertex t) { 
        PriorityQueue Q;
        Q. insert (s , h(s , t )) // Füge Startknoten hinzu 
        while (! Q.empty()) { // Solange noch Knoten unbesucht 
            u = Q.getMin(); // Nächster + bester Knoten 
            if (u == t) // Ziel erreicht
                return;
            for (jeden Nachbarn v von u) { // Alle ausgehenden Kanten
                v. dist = u. dist + w(u,v) //Tatsächliche Kosten bis v
                h = h(v,t ); // Berechne Schätzung zum Ziel
                if (v. dist ist noch undefiniert )
                    Q.add(v, h) // Füge Knoten mit Schätzung zur Schlange hinzu } } }
    '''
    match metric:
        case '0': heuristik = null
        case 'euklid': heuristik = euklid
        case 'euklid_quadrat': heuristik = euklid_quadrat
        case 'manhattan': heuristik = manhattan
        case _: heuristik = euklid
    
    todo = PriorityQueue()
    cost = {start: 0}
    counter = count()
    todo.put((0, next(counter), start))
    matrix = []
    parent = {start: None}
    visited = set()

    while not todo.empty():
        
        inner_array = []

        _, _,  vertex = todo.get()
        
        visited.add(vertex)

        if vertex == target:
            return matrix, make_path(parent, target)
        
        for adjacent,_ in graph._adj[vertex].items():

            if adjacent in visited: continue # skip these to save time

            inner_array.append([vertex, adjacent])
            
            new_cost = cost[vertex] + graph.edges[vertex, adjacent, 0][weight]
            
            #if cost.get(adjacent, None) is None:
            if cost.get(adjacent, float('inf')) > new_cost:
                parent[adjacent] = vertex
                
                cost[adjacent] = new_cost

                if adjacent == target:
                    matrix.append(inner_array)
                    return matrix, make_path(parent, target)
                
                h = heuristik(graph,adjacent,target)
                todo.put((h, next(counter), adjacent))
        
        if len(inner_array)>0:
            matrix.append(inner_array)

    return matrix, make_path(parent, target)

def null(G,v,t):
    return 0

def manhattan(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return abs(v['x']-t['x'])+abs(v['y']-t['y'])

def euklid(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return ((v['x'] - t['x'] )**2 + (v['y'] - t['y'] )**2)**0.5

def euklid_quadrat(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return (v['x'] - t['x'] )**2 + (v['y'] - t['y'] )**2
    
def make_path(parent, target):
    if target not in parent:
        return []
    v = target
    path = []
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
        matrix, path = greedy(G,379493008, 295704255, weight='travel_time')
        print(matrix)
        print(path)