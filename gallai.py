import igraph

from gallaigraph import g

paths = []
for v in range(12):
    paths.append(g.get_all_simple_paths(v))
nmax = max(len(p) for p in paths[v] for v in range(12))
print(nmax)
max_paths = [p for v in range(12) for p in paths[v] if len(p) == nmax]
print(len(max_paths[0]))
print(len(max_paths))

for v in range(12):
    if all(v in p for p in max_paths):
        print(v)
