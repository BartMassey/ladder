import igraph

g = igraph.Graph()
g.add_vertices(6)
edges = [
    (0, 1),
    (0, 3),
    (1, 2),
    (1, 4),
    (1, 5),
    (2, 5),
    (3, 4),
]
g.add_edges(edges)
