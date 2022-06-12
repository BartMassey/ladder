# Find a longest simple path in an undirected unweighted graph.
# Bart Massey 2022

from collections import deque

import igraph

def bfs_order(g, v):
    stoplist = set()
    v["level"] = 0
    stoplist.add(v.index)
    q = deque()
    q.append(v)
    while q:
        v0 = q.popleft()
        for v1 in v0.neighbors():
            if v1.index in stoplist:
                continue
            stoplist.add(v1.index)
            v1["level"] = v0["level"] + 1
            q.append(v1)

def longest_path(g, path = None, stoplist = None):
    longest = None
    nlongest = 0

    if not path:
        for v in g.vs:
            bfs_order(g, v)
            p = longest_path(g, [v], {v.index})
            np = len(p)
            if np > nlongest:
                nlongest = np
                longest = p
        return longest
    
    npath = len(path)
    if npath > nlongest:
        nlongest = npath
        longest = path

    v0 = path[-1]
    vs = [v for v in v0.neighbors() if v.index not in stoplist]
    vs.sort(key = lambda v: v["level"])
    # XXX Replace complete search with heuristic.
    #vs = [v for v in vs if v["level"] == vs[0]["level"]]
    for v1 in vs:
        p = longest_path(
            g,
            path = path + [v1],
            stoplist = stoplist | {v1.index}
        )
        np = len(p)
        if np > nlongest:
            nlongest = np
            longest = p

    return longest

if __name__ == "__main__":
    from gallaigraph import g
    #bfs_order(g, 0)
    #for v in g.vs:
    #    print(v.index, v["level"])
    p = longest_path(g)
    pi = [v.index for v in p]
    print(len(pi), pi)
