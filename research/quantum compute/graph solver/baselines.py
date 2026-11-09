"""Standard classical methods on the exact instances of run_all.py, with timings.
Run: python baselines.py
Each line is a classical method run on the same instances the oscillator benchmark uses, so the two can be compared."""
import sys, time, numpy as np, itertools
import os
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from solve_maze import generate_maze, bfs_shortest, dijkstra_on_coords
from solve_maxcut import random_graph, brute_force_maxcut
from solve_coloring import make_k_colorable
from solve_tsp import make_tsp, brute_force_tsp, tour_length
from solve_community import make_communities, normalized_mutual_info, modularity_matrix

def T(f):
    t = time.time(); r = f(); return r, time.time() - t

# Maze: Dijkstra on a FLAT field (no oscillator at all)
def maze():
    ok = 0
    for s in range(10):
        e = generate_maze(16, 16, s * 7 + 13); n = 256
        ok += dijkstra_on_coords(n, e, np.zeros(n), 0, n - 1) == bfs_shortest(n, e, 0, n - 1)
    return f"Maze, flat field (no oscillator): {ok}/10 optimal"

# Max-Cut: random-restart single-flip local search, 10 restarts (same restart count as the oscillator)
def ls_maxcut(n, edges, restarts=10, seed=0):
    rng = np.random.default_rng(seed); nb = [[] for _ in range(n)]
    for i, j in edges: nb[i].append(j); nb[j].append(i)
    best = 0
    for _ in range(restarts):
        p = rng.integers(0, 2, n); improved = True
        while improved:
            improved = False
            for v in range(n):
                gain = sum(1 if p[u] == p[v] else -1 for u in nb[v])
                if gain > 0: p[v] ^= 1; improved = True
        best = max(best, sum(p[i] != p[j] for i, j in edges))
    return best
def maxcut():
    ok = tot = 0
    for trial in range(15):
        nn = 12 + (trial % 4); e = random_graph(nn, 0.25, trial * 7 + 3)
        if len(e) < 3: continue
        tot += 1; ok += ls_maxcut(nn, e, 10, trial) == brute_force_maxcut(nn, e)
    return f"Max-Cut, 1-flip local search x10: {ok}/{tot} optimal"

# 3-colouring: DSATUR greedy, then min-conflicts repair
def color(n, edges, k=3, seed=0, iters=2000):
    rng = np.random.default_rng(seed); nb = [set() for _ in range(n)]
    for i, j in edges: nb[i].add(j); nb[j].add(i)
    c = [-1] * n
    for _ in range(n):
        v = max((u for u in range(n) if c[u] < 0), key=lambda u: (len({c[w] for w in nb[u] if c[w] >= 0}), len(nb[u])))
        used = {c[w] for w in nb[v]}; c[v] = next((x for x in range(k) if x not in used), int(rng.integers(k)))
    for _ in range(iters):
        bad = [v for v in range(n) if any(c[w] == c[v] for w in nb[v])]
        if not bad: break
        v = bad[rng.integers(len(bad))]
        c[v] = min(range(k), key=lambda x: (sum(c[w] == x for w in nb[v]), rng.random()))
    return sum(c[i] == c[j] for i, j in edges)
def coloring():
    ok = tot = 0
    for trial in range(15):
        e, _ = make_k_colorable(20, k=3, density=0.25, seed=trial * 13)
        if len(e) < 5: continue
        tot += 1; ok += color(20, e, 3, trial) == 0
    return f"3-colouring, DSATUR + min-conflicts: {ok}/{tot} valid"

# TSP: nearest neighbour from every start + 2-opt
def two_opt(t, d):
    t = list(t); n = len(t); improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n if i else n - 1):
                a, b, c_, e_ = t[i], t[i + 1], t[j], t[(j + 1) % n]
                if d[a][c_] + d[b][e_] < d[a][b] + d[c_][e_] - 1e-12:
                    t[i + 1:j + 1] = reversed(t[i + 1:j + 1]); improved = True
    return t
def tsp():
    ok = 0
    for trial in range(8):
        nn = 7 + (trial % 3); _, d = make_tsp(nn, seed=trial * 7); best = 1e9
        for s in range(nn):
            t = [s]; left = set(range(nn)) - {s}
            while left: nxt = min(left, key=lambda j: d[t[-1]][j]); t.append(nxt); left.remove(nxt)
            best = min(best, tour_length(np.array(two_opt(t, d)), d))
        ok += abs(best / brute_force_tsp(d) - 1) < 0.002
    return f"TSP, nearest neighbour + 2-opt: {ok}/8 optimal"

# Community: Newman spectral modularity, leading k-1 eigenvectors of B + k-means
def community():
    ok = 0
    for trial in range(12):
        k = 2 + (trial % 3); n, e, lab = make_communities(10, k, 0.5, 0.02, trial * 7)
        B = modularity_matrix(n, e); w, V = np.linalg.eigh(B); X = V[:, np.argsort(-w)[:max(k - 1, 1)]]
        best, bl = -1e9, None
        for att in range(10):
            rng = np.random.default_rng(att); C = X[rng.choice(n, k, replace=False)]
            for _ in range(50):
                l = np.argmin(((X[:, None] - C[None]) ** 2).sum(2), 1)
                C = np.array([X[l == c].mean(0) if (l == c).any() else C[c] for c in range(k)])
            q = sum(B[i, j] for i in range(n) for j in range(n) if l[i] == l[j])
            if q > best: best, bl = q, l.copy()
        ok += normalized_mutual_info(lab, bl) > 0.95
    return f"Community, spectral modularity + k-means: {ok}/12 perfect"

if __name__ == "__main__":
  for f in (maze, maxcut, coloring, tsp, community):
      r, t = T(f); print(f"{r}   [{t:.2f}s]")
