# Find longest word ladder in a dictionary.
# Bart Massey 2022

# Strategy: Build an undirected graph of words from the
# dictionary, with edges for connected words. Separate the
# graph into its connected components. For each component c
# from largest to smallest, find the longest path in c by
# simple enumeration of all paths. When c has fewer vertices
# than the longest path so far, stop the search.

import igraph, sys

# Load up the dictionary.
words = [w.strip() for w in open(sys.argv[1], "r")]
nwords = len(words)
nchars = len(words[0])

# Make a graph with given vertices. Label each vertex with
# its word.
graph = igraph.Graph()
graph.add_vertices(nwords)
for i, w in enumerate(words):
    graph.vs[i]["label"] = w

# Build a list of dicts giving the "contractions" of each
# word in the dictionary. The contraction of a word at
# position i is the string obtained by deleting the
# character at position i from the word. The i-th element of
# the resulting list will have the contraction of each word
# at position i.
contractions = []
for i in range(nchars):
    d = dict()
    for j, w in enumerate(words):
        dw = w[:i] + w[i + 1:]
        ws = d.setdefault(dw, set())
        ws.add(j)
    contractions.append(d)

# Add the edges to the graph. Be careful to add edges in an
# ordered fashion, so that there are no loops and each edge
# is added only once.
for cs in contractions:
    for js in cs.values():
        clique = list(js)
        nclique = len(clique)
        for i in range(nclique):
            for j in range(i + 1, nclique):
                graph.add_edge(clique[i], clique[j])

# Find the longest path through the graph.
#
# Start by finding the forest of connected components and
# sorting this list from largest to smallest vertex count.
components = sorted(graph.decompose(), key=lambda g: len(g.vs), reverse=True)
nlongest = 0
glongest = None
longest = None
for g in components:
    # Find the longest path in this component. This is done
    # by brute force enumeration of all paths. There are
    # faster algorithms, but apparently they are not needed
    # here, as the component sizes in real dictionaries tend
    # to be reasonably small. The problem is NP-hard in general,
    # so no truly efficient algorithm is known.
    ng = len(g.vs)
    # print(nlongest, ng)
    if ng < nlongest:
        # If the current g has too few vertices to have a
        # new longest path, then later g will also. We're
        # done.
        break
    p = max((max(g.get_all_simple_paths(v), key=len) for v in g.vs), key=len)
    np = len(p)
    if np > nlongest:
        # We have found a new longest path. Save the length,
        # the path, and for grins the component.
        nlongest = np
        glongest = g
        longest = p
        
# Display the answer.
print(len(glongest.vs), nlongest)
for v in longest:
    print(glongest.vs[v]["label"])
