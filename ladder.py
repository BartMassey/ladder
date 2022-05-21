# Find a longest word ladder in a dictionary.
# Bart Massey 2022

# Strategy: Build an undirected graph of words from the
# dictionary, with edges for connected words. Separate the
# graph into its connected components. For each component c
# from largest to smallest, find the longest path in c by
# simple enumeration of all paths. When c has fewer vertices
# than the longest path so far, stop the search.

import igraph, sys
from longest import longest_path

# Load up the dictionary. Ignore one-letter words.
all_words = [w.strip() for w in open(sys.argv[1], "r") if len(w.strip()) >= 2]
nshortest_word = min(map(len, all_words))
nlongest_word = max(map(len, all_words))

# Iterate over words of increasing length.
sep = False
for nchars in range(nshortest_word, nlongest_word + 1):
    # Get the words of the current length.
    words = [w for w in all_words if len(w) == nchars]
    nwords = len(words)
    if nwords == 0:
        continue

    # Formatting kludge to get blank lines between iterations.
    if sep:
        print()
    sep = True

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
        with open(f"clusters/{nchars}-{ng}.txt", "w") as f:
            for v in g.vs:
                print(f'{v["label"]}', file=f)
        if ng < nlongest:
            # If the current g has too few vertices to have a
            # new longest path, then later g will also. We're
            # done.
            break
        print(f"starting search {nchars}/{ng}")
        p = longest_path(g)
        np = len(p)
        if np > nlongest:
            # We have found a new longest path. Save the length,
            # the path, and for grins the component.
            nlongest = np
            glongest = g
            longest = p

    # Display the answer.
    print(f"word length {nchars}")
    print(f"vertices of max length component {len(glongest.vs)}")
    print(f"max path length {nlongest}")
    for v in longest:
        print(glongest.vs[v]["label"])
