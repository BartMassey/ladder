import igraph, gallaigraph

gallaigraph.g.write("graph.gml", format="gml")
g2 = igraph.Graph.Read("graph.gml", format="gml")
print(g2)
