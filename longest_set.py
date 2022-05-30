# Find a longest simple path in an undirected unweighted graph.
# Bart Massey 2022

import igraph

def longest_path(g):
    nlongest = 0
    longest = None
    for v in range(len(g.vs)):
        class Rep(object):
            def __init__(self, w, prototype = None):
                self.w = w
                if prototype:
                    self.used = prototype.used | {w}
                    self.path = prototype.path + (w,)
                else:
                    self.used = frozenset({v, w})
                    self.path = (v, w)
            
            def __eq__(self, r):
                return r.w == self.w and r.used == self.used

            def __hash__(self):
                return hash((self.w, self.used))

            def extend(self):
                for x in g.neighbors(self.w):
                    if x not in self.used:
                        yield Rep(x, prototype=self)

        rs = set(map(Rep, g.neighbors(v)))
        depth = 1
        while True:
            print(f"longest: {v}@{depth}")
            nrs = set(nr for r in rs for nr in r.extend())
            if not nrs:
                break
            rs = nrs
            depth += 1

        rp = list(rs)[0].path
        nrp = len(rp)
        if nrp > nlongest:
            nlongest = nrp
            longest = rp

    return longest

if __name__ == "__main__":
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

    print(longest_path(g))
