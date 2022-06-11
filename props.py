import igraph, sys

# Load up the dictionary. Ignore one-letter words.
all_words = [w.strip() for w in open(sys.argv[1], "r") if len(w.strip()) >= 2]
nshortest_word = min(map(len, all_words))
nlongest_word = max(map(len, all_words))

def decompose(g):
    for v in g.vs:
        cs = (g - v.index).decompose()
        if len(cs) > 1:
            ds = []
            for c in cs:
                ds += decompose(c)
            return ds
    return [g]

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

    # Start by finding the forest of connected components and
    # sorting this list from largest to smallest vertex count.
    components = sorted(graph.decompose(), key=lambda g: len(g.vs), reverse=True)

    for c in components:
        print('component', len(c.vs))
        d = c.biconnected_components()
        print(
            'decomposition',
            len(c.vs),
            len(d),
            [len(g0) for g0 in d],
        )
        break
