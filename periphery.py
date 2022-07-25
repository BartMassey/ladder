import igraph

def periphery(g, i):
    return sum(*g.shortest_paths(source=i))

def pvis(g):
    ps = [periphery(g, i) for i in range(len(g.vs))]
    print(ps)
    least_p = min(ps)
    greatest_p = max(ps)
    range_p = greatest_p - least_p
    rs = [int(0xff * ((p - least_p) / range_p)) for p in ps]
    print(rs)
    colors = [f"#{r:02x}{0xff - r:02x}00" for r in rs]

    layout = g.layout(layout='fruchterman_reingold')
    igraph.plot(g, vertex_color=colors)

g = igraph.Graph.K_Regular(50, 3)
pvis(g)
