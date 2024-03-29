from itertools import count
from queue import PriorityQueue


def astar(graph, start, target, metric="0", weight="length", **kwargs):
    """
    void aStar (Graph g, Vertex s , Vertex t) {
        PriorityQueue openList ; // Open List wird als Prioritätsliste realisiert und
        // enthält eine Menge von Knoten v mit Prioritätswert d[v] + h(v).
        s.dist = 0;
        s.prev = null;
        openList.insert(s , h(s)); // Fügt Startknoten s mit Prioritätswert h(s) ein .
        while (! openList .empty() ) {
            u = openList.delMin(); // Knoten v wird besucht;
            // kürzester Weg ist jetzt bekannt.
            if (u == t) // Ziel erreicht .
            //breche Suche erfolgreich ab;
            for (jeden Nachbarn v von u ) {
                if (v. dist ist noch undefiniert ) { // Knoten v ist noch unbekannt.
                    v.dist = u.dist + w(u,v);
                    v.prev = u;
                    openList.insert (v, v. dist + h(v,t ));
                } else if (v. dist + w(u,v) < v.dist ) { // v. dist kann verbessert werden mit Knoten u als Vorgänger.
                    v. dist = u.dist + w(u,v);
                    v. prev = u;
                    openList.changePriority(v, v.dist + h(v,t ));
                }
            }
        }
    """
    match metric:
        case "0":
            heuristik = null
        case "euklid":
            heuristik = euklid
        case "euklid_quadrat":
            heuristik = euklid_quadrat
        case "manhattan":
            heuristik = manhattan
        case _:
            heuristik = euklid

    openList = PriorityQueue()
    dist = {start: 0}
    prev = {start: None}
    counter = count()
    openList.put((heuristik(graph, start, target), next(counter), start))
    matrix = []
    parent = {start: None}
    visited = set()

    # Haben schon die Kosten anhand des aktuellen Gewichts,
    # wollen aber immer die Länge und Dauer:
    length = {start: 0}
    travel_time = {start: 0}

    while not openList.empty():
        inner_array = []

        _, _, vertex = openList.get()

        visited.add(vertex)

        if vertex == target:
            return (
                matrix,
                make_path(parent, target),
                dist.get(target, 0),
                length.get(target, 0),
                travel_time.get(target, 0),
            )

        for adjacent, _ in graph._adj[vertex].items():
            inner_array.append([vertex, adjacent])

            new_dist = dist[vertex] + graph.edges[vertex, adjacent, 0][weight]

            if dist.get(adjacent, None) is None:
                parent[adjacent] = vertex
                dist[adjacent] = new_dist
                prev[adjacent] = vertex
                h = heuristik(graph, adjacent, target)
                openList.put((dist[adjacent] + h, next(counter), adjacent))

                # Immer Länge und Dauer sammeln
                length[adjacent] = (
                    length[vertex] + graph.edges[vertex, adjacent, 0]["length"]
                )
                travel_time[adjacent] = (
                    travel_time[vertex]
                    + graph.edges[vertex, adjacent, 0]["travel_time"]
                )

            elif (new_dist) < dist[adjacent]:
                parent[adjacent] = vertex
                dist[adjacent] = new_dist
                prev[adjacent] = vertex
                # changePriority in Python nicht möglich? Einfach hinzufügen
                h = heuristik(graph, adjacent, target)
                openList.put((dist[adjacent] + h, next(counter), adjacent))

                # Immer Länge und Dauer sammeln
                length[adjacent] = (
                    length[vertex] + graph.edges[vertex, adjacent, 0]["length"]
                )
                travel_time[adjacent] = (
                    travel_time[vertex]
                    + graph.edges[vertex, adjacent, 0]["travel_time"]
                )

        if len(inner_array) > 0:
            matrix.append(inner_array)

    return (
        matrix,
        make_path(parent, target),
        dist.get(target, 0),
        length.get(target, 0),
        travel_time.get(target, 0),
    )


def null(G, v, t):
    return 0


def manhattan(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return abs(v["x"] - t["x"]) + abs(v["y"] - t["y"])


def euklid(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return ((v["x"] - t["x"]) ** 2 + (v["y"] - t["y"]) ** 2) ** 0.5


def euklid_quadrat(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return (v["x"] - t["x"]) ** 2 + (v["y"] - t["y"]) ** 2


def make_path(parent, target):
    if target not in parent:
        return []
    v = target
    path = []
    while v is not None:  # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]


if __name__ == "__main__":
    import osmnx as ox

    ## Bbox vom Start
    north, south, east, west = (
        50.32942276889266,
        50.32049083973944,
        11.944606304168701,
        11.929510831832886,
    )

    ## create network from that bounding box
    G = ox.graph_from_bbox(north, south, east, west, network_type="drive")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # 295704008
    # 295704255
    print("astar")
    matrix, path, cost, length, time = astar(
        G, 379493008, 295704255, weight="travel_time"
    )
    print(matrix)
    print(path)
    print(len(matrix))
    print(cost)
    print(length)
    print(time)
