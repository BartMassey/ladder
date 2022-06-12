import igraph

g = igraph.Graph()
g.add_vertices(12)
edges = [
    (0, 2),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 4),
    (3, 9),
    (4, 5),
    (4, 8),
    (5, 7),
    (6, 7),
    (6, 8),
    (7, 9),
    (8, 10),
    (9, 10),
    (10, 11),
]
g.add_edges(edges)
