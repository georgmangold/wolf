def null(G,v,t):
    return 0

def euklid(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return ((v['x'] - t['x'] )**2 + (v['y'] - t['y'] )**2)**0.5

def euklid_quadrat(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return (v['x'] - t['x'] )**2 + (v['y'] - t['y'] )**2

def manhattan(G, v, t):
    v = G.nodes[v]
    t = G.nodes[t]
    return abs(v['x']-t['x'])+abs(v['y']-t['y'])
