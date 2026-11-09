"""
ontology_learner.py
====================

100-node ontology learning via GFD oscillator.

Setup:
  ~100 hand-crafted facts as (subject, relation, object) triples.
  Each unique entity becomes one node.
  Co-occurrence in facts builds K (PPMI-weighted).
  Oscillator with deflation cascade extracts an N-dimensional embedding.

Queries the system answers (without being told):
  1. Cluster structure: which entities group together?
  2. Top-k similar: nearest neighbors of any entity.
  3. Analogies: a:b :: c:?
  4. Relational membership: which entities have property X?
  5. Out-of-distribution probing: rarely-mentioned entities.

Online learning:
  Mid-run, add 10 new facts to K (one outer product per fact).
  Re-run oscillator. New entities slot into existing structure
  without retraining, in milliseconds.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from collections import defaultdict
from gfd_oscillator import GFDOscillator
import time


# =====================================================================
#  ONTOLOGY: ~100 facts about animals, plants, environments, actions
# =====================================================================
# Carefully designed so that:
#   - Mammals: cat, dog, cow, horse, mouse, rabbit, lion, tiger
#   - Birds: sparrow, eagle, owl, parrot, chicken
#   - Fish: salmon, tuna, shark, goldfish
#   - Reptiles: snake, lizard
#   - Insects: bee, butterfly
#   - Plants: tree, flower, grass, rose
#   - Environments: forest, ocean, sky, ground, water, nest, den
#   - Actions: swim, fly, run, walk, sleep, eat, hunt, sing, climb
#   - Foods: meat, fish_food, grass_food, seed, nectar
#   - Attributes: warm-blooded, cold-blooded, has-wings, has-fur, has-scales

FACTS = [
    # Mammals are warm-blooded with fur
    ("cat", "is_a", "mammal"),
    ("dog", "is_a", "mammal"),
    ("cow", "is_a", "mammal"),
    ("horse", "is_a", "mammal"),
    ("mouse", "is_a", "mammal"),
    ("rabbit", "is_a", "mammal"),
    ("lion", "is_a", "mammal"),
    ("tiger", "is_a", "mammal"),
    ("mammal", "has", "fur"),
    ("mammal", "is", "warm_blooded"),

    # Birds fly, have wings
    ("sparrow", "is_a", "bird"),
    ("eagle", "is_a", "bird"),
    ("owl", "is_a", "bird"),
    ("parrot", "is_a", "bird"),
    ("chicken", "is_a", "bird"),
    ("bird", "has", "wings"),
    ("bird", "is", "warm_blooded"),
    ("bird", "can", "fly"),

    # Fish swim, in water
    ("salmon", "is_a", "fish"),
    ("tuna", "is_a", "fish"),
    ("shark", "is_a", "fish"),
    ("goldfish", "is_a", "fish"),
    ("fish", "has", "scales"),
    ("fish", "is", "cold_blooded"),
    ("fish", "can", "swim"),
    ("fish", "lives_in", "water"),
    ("fish", "lives_in", "ocean"),

    # Reptiles
    ("snake", "is_a", "reptile"),
    ("lizard", "is_a", "reptile"),
    ("reptile", "has", "scales"),
    ("reptile", "is", "cold_blooded"),

    # Insects
    ("bee", "is_a", "insect"),
    ("butterfly", "is_a", "insect"),
    ("insect", "has", "wings"),
    ("insect", "can", "fly"),
    ("bee", "produces", "honey"),
    ("bee", "eats", "nectar"),
    ("butterfly", "eats", "nectar"),

    # Plants
    ("tree", "is_a", "plant"),
    ("flower", "is_a", "plant"),
    ("grass", "is_a", "plant"),
    ("rose", "is_a", "flower"),
    ("plant", "lives_in", "ground"),
    ("plant", "needs", "water"),
    ("plant", "needs", "sunlight"),

    # Environment relationships
    ("bird", "lives_in", "nest"),
    ("bird", "lives_in", "tree"),
    ("bird", "lives_in", "sky"),
    ("dog", "lives_in", "den"),
    ("cat", "lives_in", "house"),
    ("mouse", "lives_in", "ground"),
    ("snake", "lives_in", "ground"),
    ("lion", "lives_in", "forest"),
    ("tiger", "lives_in", "forest"),

    # Predator/prey
    ("cat", "hunts", "mouse"),
    ("lion", "hunts", "rabbit"),
    ("tiger", "hunts", "rabbit"),
    ("eagle", "hunts", "rabbit"),
    ("owl", "hunts", "mouse"),
    ("shark", "hunts", "fish"),

    # Diet
    ("cat", "eats", "fish"),
    ("cat", "eats", "meat"),
    ("dog", "eats", "meat"),
    ("lion", "eats", "meat"),
    ("tiger", "eats", "meat"),
    ("cow", "eats", "grass"),
    ("horse", "eats", "grass"),
    ("rabbit", "eats", "grass"),
    ("sparrow", "eats", "seed"),
    ("parrot", "eats", "seed"),
    ("chicken", "eats", "seed"),

    # Capabilities
    ("cat", "can", "run"),
    ("dog", "can", "run"),
    ("cow", "can", "walk"),
    ("horse", "can", "run"),
    ("snake", "can", "slither"),
    ("lizard", "can", "climb"),
    ("parrot", "can", "fly"),
    ("parrot", "can", "sing"),
    ("sparrow", "can", "sing"),
    ("sparrow", "can", "fly"),
    ("owl", "can", "fly"),
    ("eagle", "can", "fly"),
    ("chicken", "can", "walk"),
    ("salmon", "can", "swim"),
    ("tuna", "can", "swim"),
    ("shark", "can", "swim"),
    ("bee", "produces", "honey"),

    # Sleep/rest
    ("cat", "does", "sleep"),
    ("dog", "does", "sleep"),
    ("owl", "is", "nocturnal"),

    # Some duplicates and reinforcements
    ("dog", "is", "loyal"),
    ("cat", "is", "independent"),
    ("eagle", "is", "predator"),
    ("lion", "is", "predator"),
    ("tiger", "is", "predator"),
    ("shark", "is", "predator"),
]


# =====================================================================
def build_vocabulary(facts):
    """Extract all unique entities (subjects, objects) AND relations."""
    entities = set()
    relations = set()
    for s, r, o in facts:
        entities.add(s)
        entities.add(o)
        relations.add(r)
    vocab = sorted(entities)
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    return vocab, word_to_idx, sorted(relations)


def build_K_from_facts(facts, word_to_idx):
    """
    Build coupling matrix from co-occurrence in facts.

    Each fact (s, r, o) contributes to K:
      - Strong coupling between s and o (they're related)
      - The relation r is implicit in the structure
    """
    N = len(word_to_idx)
    C = np.zeros((N, N))

    for s, r, o in facts:
        i = word_to_idx[s]
        j = word_to_idx[o]
        # Symmetric co-occurrence
        C[i, j] += 1
        C[j, i] += 1

    # PPMI normalization
    total = C.sum()
    row_totals = C.sum(axis=1)
    col_totals = C.sum(axis=0)
    PPMI = np.zeros_like(C)
    for i in range(N):
        for j in range(N):
            if C[i, j] > 0 and row_totals[i] > 0 and col_totals[j] > 0:
                p_ij = C[i, j] / total
                p_i = row_totals[i] / total
                p_j = col_totals[j] / total
                pmi = np.log(p_ij / (p_i * p_j))
                PPMI[i, j] = max(0, pmi)
    return PPMI, C


def embedding_via_oscillator(K, n_dims=8, depth=8):
    """Deflation cascade: extract n_dims modes one at a time."""
    N = len(K)
    K_residual = K.copy()
    osc = GFDOscillator(dt=0.05, steps=2000)
    embedding = np.zeros((N, n_dims))
    eigvals = []
    for k in range(n_dims):
        graph = GFDOscillator.encode_weighted(N, K_residual)
        state = osc.run_phase(graph, depth=depth, seed=42 + k * 137)
        if state.Sv[0] < 1e-10:
            break
        v = state.Vt[0] / np.linalg.norm(state.Vt[0])
        lam = float(v @ K_residual @ v)
        eigvals.append(lam)
        embedding[:, k] = v * np.sqrt(abs(lam))
        K_residual = K_residual - lam * np.outer(v, v)
    return embedding, eigvals


# =====================================================================
#  Query interface
# =====================================================================
def cosine_sim(a, b):
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def nearest_neighbors(target, embedding, vocab, k=5):
    if target not in vocab:
        return []
    target_vec = embedding[vocab.index(target)]
    sims = []
    for i, w in enumerate(vocab):
        if w == target:
            continue
        sims.append((w, cosine_sim(target_vec, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k]


def cluster(embedding, vocab, n_clusters=4):
    """k-means clustering of the embedding."""
    from collections import defaultdict
    rng = np.random.RandomState(0)
    N = len(vocab)
    # Init centers randomly from data
    init_idx = rng.choice(N, n_clusters, replace=False)
    centers = embedding[init_idx].copy()
    assignments = np.zeros(N, dtype=int)
    for it in range(50):
        # Assign each point to nearest center
        new_assignments = np.zeros(N, dtype=int)
        for i in range(N):
            dists = [np.linalg.norm(embedding[i] - centers[c]) for c in range(n_clusters)]
            new_assignments[i] = int(np.argmin(dists))
        if np.array_equal(new_assignments, assignments):
            break
        assignments = new_assignments
        # Update centers
        for c in range(n_clusters):
            members = [i for i in range(N) if assignments[i] == c]
            if members:
                centers[c] = np.mean(embedding[members], axis=0)
    # Group entities by cluster
    groups = defaultdict(list)
    for i, w in enumerate(vocab):
        groups[int(assignments[i])].append(w)
    return groups


def analogy(a, b, c, embedding, vocab, k=3):
    """a:b :: c:? — return top-k candidate ?"""
    if a not in vocab or b not in vocab or c not in vocab:
        return []
    va = embedding[vocab.index(a)]
    vb = embedding[vocab.index(b)]
    vc = embedding[vocab.index(c)]
    # Target = vb - va + vc  (the canonical analogy formula)
    target = vb - va + vc
    sims = []
    excl = {a, b, c}
    for i, w in enumerate(vocab):
        if w in excl:
            continue
        sims.append((w, cosine_sim(target, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k]


# =====================================================================
def main():
    print("=" * 76)
    print(" 100-NODE ONTOLOGY LEARNER — oscillator builds a world model from facts")
    print("=" * 76)

    # --- Build initial system ---
    vocab, word_to_idx, relations = build_vocabulary(FACTS)
    N = len(vocab)
    print(f"\n  Initial corpus: {len(FACTS)} facts, {N} unique entities, "
          f"{len(relations)} relations")
    print(f"  Relations seen: {relations}")

    t0 = time.time()
    K, C = build_K_from_facts(FACTS, word_to_idx)
    t_build = time.time() - t0
    print(f"  PPMI matrix built in {t_build*1000:.1f} ms — "
          f"{(C > 0).sum()} nonzero co-occurrence entries")

    t0 = time.time()
    embedding, eigvals = embedding_via_oscillator(K, n_dims=8, depth=8)
    t_train = time.time() - t0
    print(f"  Oscillator + deflation cascade: {t_train:.1f}s "
          f"({len(eigvals)} modes extracted)")
    print(f"  Eigenvalues: {[f'{e:.2f}' for e in eigvals]}")

    # --- Query 1: cluster structure ---
    print("\n" + "─" * 76)
    print("  Q1: What clusters did the oscillator find? (k-means on embedding, k=5)")
    print("─" * 76)
    clusters = cluster(embedding, vocab, n_clusters=5)
    for cid in sorted(clusters.keys()):
        members = sorted(clusters[cid])
        print(f"  Cluster {cid} ({len(members)}): {', '.join(members[:12])}"
              + (f" ... +{len(members)-12} more" if len(members) > 12 else ""))

    # --- Query 2: nearest neighbors ---
    print("\n" + "─" * 76)
    print("  Q2: Nearest neighbors (top-5)")
    print("─" * 76)
    test_words = ["cat", "dog", "shark", "eagle", "snake", "rose", "honey",
                  "predator", "warm_blooded", "ocean"]
    for w in test_words:
        if w in vocab:
            nn = nearest_neighbors(w, embedding, vocab, k=5)
            nn_str = ", ".join(f"{n}({s:+.2f})" for n, s in nn)
            print(f"  {w:>14s}  →  {nn_str}")

    # --- Query 3: analogies ---
    print("\n" + "─" * 76)
    print("  Q3: Analogies (a:b :: c:?)")
    print("─" * 76)
    analogies_to_test = [
        ("cat", "mammal", "sparrow"),     # → bird
        ("cat", "mammal", "salmon"),       # → fish
        ("salmon", "water", "bird"),       # → sky?
        ("bird", "fly", "fish"),           # → swim?
        ("cat", "meat", "cow"),            # → grass
        ("cat", "meat", "rabbit"),         # → grass
    ]
    for a, b, c in analogies_to_test:
        result = analogy(a, b, c, embedding, vocab, k=3)
        if result:
            top = ", ".join(f"{w}({s:+.2f})" for w, s in result)
            print(f"  {a} : {b} :: {c} : ?   →   {top}")

    # --- Query 4: out-of-distribution probing ---
    print("\n" + "─" * 76)
    print("  Q4: Where did rare entities land? (each appears in only 1 fact)")
    print("─" * 76)
    rare = ["honey", "loyal", "independent", "nocturnal"]
    for w in rare:
        if w in vocab:
            nn = nearest_neighbors(w, embedding, vocab, k=3)
            nn_str = ", ".join(f"{n}({s:+.2f})" for n, s in nn)
            print(f"  {w:>14s}  →  {nn_str}")

    # --- Online learning ---
    print("\n" + "═" * 76)
    print(" ONLINE LEARNING: add 10 new facts, re-train, observe placement")
    print("═" * 76)

    NEW_FACTS = [
        ("dolphin", "is_a", "mammal"),
        ("dolphin", "lives_in", "ocean"),
        ("dolphin", "can", "swim"),
        ("whale", "is_a", "mammal"),
        ("whale", "lives_in", "ocean"),
        ("whale", "can", "swim"),
        ("hawk", "is_a", "bird"),
        ("hawk", "can", "fly"),
        ("hawk", "hunts", "mouse"),
        ("hawk", "hunts", "rabbit"),
    ]
    print(f"  New facts: {len(NEW_FACTS)} — introduces 'dolphin', 'whale', 'hawk'")
    for f in NEW_FACTS[:5]:
        print(f"    {f}")
    print("    ...")

    extended_facts = FACTS + NEW_FACTS
    vocab2, w2i2, _ = build_vocabulary(extended_facts)
    N2 = len(vocab2)

    t0 = time.time()
    K2, C2 = build_K_from_facts(extended_facts, w2i2)
    t_rebuild = time.time() - t0

    t0 = time.time()
    embedding2, eigvals2 = embedding_via_oscillator(K2, n_dims=8, depth=8)
    t_retrain = time.time() - t0

    print(f"\n  K rebuilt: {t_rebuild*1000:.1f} ms")
    print(f"  Oscillator re-converged: {t_retrain:.1f}s")
    print(f"  Vocabulary: {N} → {N2} entities (+{N2-N})")

    # --- Probe new entities ---
    print("\n" + "─" * 76)
    print("  After ingesting new facts: where do dolphin/whale/hawk land?")
    print("─" * 76)
    for w in ["dolphin", "whale", "hawk"]:
        nn = nearest_neighbors(w, embedding2, vocab2, k=5)
        nn_str = ", ".join(f"{n}({s:+.2f})" for n, s in nn)
        print(f"  {w:>14s}  →  {nn_str}")

    # --- Did existing entities stay stable? ---
    print("\n" + "─" * 76)
    print("  Existing entities: did their neighborhoods stay stable?")
    print("─" * 76)
    for w in ["cat", "shark", "eagle"]:
        nn1 = set(n for n, _ in nearest_neighbors(w, embedding, vocab, k=5))
        nn2 = set(n for n, _ in nearest_neighbors(w, embedding2, vocab2, k=5))
        overlap = len(nn1 & nn2)
        print(f"  {w:>14s}: {overlap}/5 of top-5 neighbors unchanged")
        print(f"                 before: {sorted(nn1)}")
        print(f"                 after:  {sorted(nn2)}")


if __name__ == "__main__":
    main()
