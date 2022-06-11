# Find a longest simple path in an undirected unweighted graph.
# Bart Massey 2022

from collections import deque

import igraph

def longest_path_tree(tree):
    # Dijkstra's algorithm for longest path in an undirected
    # tree.
    vids, _, _ = tree.bfs(0)
    start = vids[-1]
    vids, _, parents = tree.bfs(start)
    end = vids[-1]
    cur = end
    path = []
    while True:
        path = [tree.vs[cur]] + path
        if cur == start:
            break
        cur = parents[cur]
    assert path[0] == tree.vs[start]
    return path

def longest_path(g):
    tree = g.spanning_tree(weights = [-1] * len(g.es))
    return longest_path_tree(tree)

if __name__ == "__main__":
    from gallaigraph import g
    #bfs_order(g, 0)
    #for v in g.vs:
    #    print(v.index, v["level"])
    p = longest_path(g)
    pi = [v.index for v in p]
    print(len(pi) - 1, pi)
