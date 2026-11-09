"""
ontology_learner_large.py
==========================

Larger ontology learner: ~300 entities, ~600 facts, multi-hop reasoning,
cross-domain transfer, and historical evolution.

Domains covered:
  - Animals (mammals, birds, fish, reptiles, insects, amphibians)
  - Foods (meat, plants, fruits, grains, etc.)
  - Environments (land, water, air, climates, habitats)
  - Materials (fur, scales, feathers, wood, stone, metal)
  - Weather (rain, snow, sunshine, fog, etc.)
  - Activities (run, swim, fly, sleep, hunt, build, etc.)
  - Body parts (legs, wings, tail, fur, etc.)

Demonstrates:
  1. Scale: ~300 entity embedding via deflation cascade
  2. Multi-hop reasoning: "what eats what lives in water?"
  3. Cross-domain queries: animal -> habitat -> weather
  4. Online evolution: revise facts, observe embedding adjustment
  5. Latent attribute discovery: predator/prey, terrestrial/aquatic
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import time
from collections import Counter, defaultdict
from gfd_oscillator import GFDOscillator


# =====================================================================
#  Build comprehensive ontology
# =====================================================================
def build_facts():
    """Generate ~600 facts across multiple domains."""
    facts = []

    # === ANIMALS ===
    mammals = ["cat", "dog", "lion", "tiger", "wolf", "bear", "horse", "cow",
               "sheep", "goat", "pig", "rabbit", "mouse", "rat", "deer", "fox",
               "elephant", "giraffe", "zebra", "monkey", "ape"]
    aquatic_mammals = ["dolphin", "whale", "seal", "otter"]
    birds = ["eagle", "hawk", "owl", "sparrow", "robin", "parrot", "chicken",
             "duck", "swan", "penguin", "ostrich"]
    fish = ["salmon", "tuna", "shark", "bass", "trout", "goldfish", "cod"]
    reptiles = ["snake", "lizard", "turtle", "crocodile", "alligator", "iguana"]
    insects = ["bee", "ant", "butterfly", "beetle", "spider", "fly", "mosquito"]
    amphibians = ["frog", "toad", "salamander"]

    # is_a relationships
    for a in mammals: facts.append((a, "is_a", "mammal"))
    for a in aquatic_mammals:
        facts.append((a, "is_a", "mammal"))
        facts.append((a, "is_a", "aquatic_mammal"))
    for a in birds: facts.append((a, "is_a", "bird"))
    for a in fish: facts.append((a, "is_a", "fish"))
    for a in reptiles: facts.append((a, "is_a", "reptile"))
    for a in insects: facts.append((a, "is_a", "insect"))
    for a in amphibians: facts.append((a, "is_a", "amphibian"))

    # Class-level attributes
    facts.extend([
        ("mammal", "has", "fur"),
        ("mammal", "is", "warm_blooded"),
        ("mammal", "has", "live_birth"),
        ("bird", "has", "feathers"),
        ("bird", "has", "wings"),
        ("bird", "is", "warm_blooded"),
        ("bird", "lays", "eggs"),
        ("bird", "can", "fly"),
        ("fish", "has", "scales"),
        ("fish", "has", "fins"),
        ("fish", "is", "cold_blooded"),
        ("fish", "lives_in", "water"),
        ("fish", "can", "swim"),
        ("reptile", "has", "scales"),
        ("reptile", "is", "cold_blooded"),
        ("reptile", "lays", "eggs"),
        ("insect", "has", "wings"),
        ("insect", "has", "six_legs"),
        ("insect", "is", "cold_blooded"),
        ("amphibian", "lives_in", "water"),
        ("amphibian", "lives_in", "land"),
        ("amphibian", "is", "cold_blooded"),
        ("aquatic_mammal", "lives_in", "ocean"),
        ("aquatic_mammal", "can", "swim"),
    ])

    # === HABITATS ===
    facts.extend([
        ("ocean", "is_a", "water_habitat"),
        ("river", "is_a", "water_habitat"),
        ("lake", "is_a", "water_habitat"),
        ("pond", "is_a", "water_habitat"),
        ("forest", "is_a", "land_habitat"),
        ("desert", "is_a", "land_habitat"),
        ("plains", "is_a", "land_habitat"),
        ("mountain", "is_a", "land_habitat"),
        ("jungle", "is_a", "land_habitat"),
        ("arctic", "is_a", "land_habitat"),
        ("water_habitat", "contains", "water"),
        ("land_habitat", "contains", "ground"),
    ])

    # Animal-habitat mappings
    facts.extend([
        ("lion", "lives_in", "plains"),
        ("tiger", "lives_in", "jungle"),
        ("tiger", "lives_in", "forest"),
        ("wolf", "lives_in", "forest"),
        ("bear", "lives_in", "forest"),
        ("bear", "lives_in", "mountain"),
        ("elephant", "lives_in", "plains"),
        ("elephant", "lives_in", "jungle"),
        ("giraffe", "lives_in", "plains"),
        ("zebra", "lives_in", "plains"),
        ("monkey", "lives_in", "jungle"),
        ("ape", "lives_in", "jungle"),
        ("penguin", "lives_in", "arctic"),
        ("seal", "lives_in", "arctic"),
        ("seal", "lives_in", "ocean"),
        ("dolphin", "lives_in", "ocean"),
        ("whale", "lives_in", "ocean"),
        ("otter", "lives_in", "river"),
        ("frog", "lives_in", "pond"),
        ("toad", "lives_in", "pond"),
        ("salmon", "lives_in", "river"),
        ("salmon", "lives_in", "ocean"),
        ("trout", "lives_in", "river"),
        ("trout", "lives_in", "lake"),
        ("bass", "lives_in", "lake"),
        ("shark", "lives_in", "ocean"),
        ("tuna", "lives_in", "ocean"),
        ("cod", "lives_in", "ocean"),
        ("crocodile", "lives_in", "river"),
        ("alligator", "lives_in", "river"),
        ("turtle", "lives_in", "pond"),
        ("snake", "lives_in", "forest"),
        ("snake", "lives_in", "desert"),
        ("lizard", "lives_in", "desert"),
        ("iguana", "lives_in", "jungle"),
    ])

    # === DIET / PREDATION ===
    facts.extend([
        # Carnivores
        ("lion", "eats", "meat"),
        ("tiger", "eats", "meat"),
        ("wolf", "eats", "meat"),
        ("bear", "eats", "meat"),
        ("bear", "eats", "berries"),
        ("eagle", "eats", "meat"),
        ("hawk", "eats", "meat"),
        ("owl", "eats", "meat"),
        ("shark", "eats", "fish"),
        ("crocodile", "eats", "meat"),
        ("alligator", "eats", "meat"),
        ("snake", "eats", "mouse"),
        ("snake", "eats", "frog"),
        ("cat", "eats", "mouse"),
        ("cat", "eats", "fish"),
        ("dog", "eats", "meat"),
        ("fox", "eats", "rabbit"),
        ("fox", "eats", "mouse"),
        # Herbivores
        ("cow", "eats", "grass"),
        ("horse", "eats", "grass"),
        ("horse", "eats", "hay"),
        ("sheep", "eats", "grass"),
        ("goat", "eats", "grass"),
        ("rabbit", "eats", "grass"),
        ("rabbit", "eats", "carrot"),
        ("deer", "eats", "grass"),
        ("deer", "eats", "leaves"),
        ("elephant", "eats", "leaves"),
        ("elephant", "eats", "grass"),
        ("giraffe", "eats", "leaves"),
        ("zebra", "eats", "grass"),
        ("monkey", "eats", "fruit"),
        ("monkey", "eats", "leaves"),
        ("ape", "eats", "fruit"),
        # Omnivores
        ("pig", "eats", "grain"),
        ("pig", "eats", "vegetables"),
        ("chicken", "eats", "grain"),
        ("chicken", "eats", "seed"),
        ("sparrow", "eats", "seed"),
        ("robin", "eats", "worm"),
        ("parrot", "eats", "fruit"),
        ("parrot", "eats", "seed"),
        ("duck", "eats", "fish"),
        ("duck", "eats", "grain"),
        ("swan", "eats", "grain"),
        # Insect predators
        ("frog", "eats", "fly"),
        ("frog", "eats", "mosquito"),
        ("toad", "eats", "ant"),
        ("spider", "eats", "fly"),
        ("bee", "eats", "nectar"),
        ("butterfly", "eats", "nectar"),
        ("ant", "eats", "sugar"),
        ("mosquito", "eats", "blood"),
    ])

    # Predation chain (predator hunts prey)
    facts.extend([
        ("lion", "hunts", "zebra"),
        ("lion", "hunts", "deer"),
        ("tiger", "hunts", "deer"),
        ("wolf", "hunts", "deer"),
        ("wolf", "hunts", "rabbit"),
        ("eagle", "hunts", "rabbit"),
        ("eagle", "hunts", "fish"),
        ("hawk", "hunts", "mouse"),
        ("owl", "hunts", "mouse"),
        ("shark", "hunts", "seal"),
        ("shark", "hunts", "fish"),
        ("fox", "hunts", "rabbit"),
        ("fox", "hunts", "chicken"),
        ("cat", "hunts", "mouse"),
        ("cat", "hunts", "bird"),
        ("snake", "hunts", "mouse"),
        ("snake", "hunts", "frog"),
    ])

    # === ABILITIES ===
    facts.extend([
        ("eagle", "can", "fly"),
        ("hawk", "can", "fly"),
        ("owl", "can", "fly"),
        ("sparrow", "can", "fly"),
        ("robin", "can", "fly"),
        ("parrot", "can", "fly"),
        ("duck", "can", "fly"),
        ("swan", "can", "fly"),
        ("bee", "can", "fly"),
        ("butterfly", "can", "fly"),
        ("fly", "can", "fly"),
        ("mosquito", "can", "fly"),
        # cannot fly birds
        ("chicken", "cannot", "fly"),
        ("ostrich", "cannot", "fly"),
        ("penguin", "cannot", "fly"),
        ("penguin", "can", "swim"),
        ("ostrich", "can", "run"),
        # swimming
        ("dolphin", "can", "swim"),
        ("whale", "can", "swim"),
        ("seal", "can", "swim"),
        ("otter", "can", "swim"),
        ("salmon", "can", "swim"),
        ("tuna", "can", "swim"),
        ("shark", "can", "swim"),
        ("frog", "can", "swim"),
        ("duck", "can", "swim"),
        # running
        ("lion", "can", "run"),
        ("tiger", "can", "run"),
        ("wolf", "can", "run"),
        ("horse", "can", "run"),
        ("zebra", "can", "run"),
        ("deer", "can", "run"),
        ("rabbit", "can", "run"),
        ("dog", "can", "run"),
        ("cat", "can", "run"),
        ("mouse", "can", "run"),
        ("fox", "can", "run"),
        # climbing
        ("monkey", "can", "climb"),
        ("ape", "can", "climb"),
        ("cat", "can", "climb"),
        ("squirrel", "can", "climb"),
        ("lizard", "can", "climb"),
        ("iguana", "can", "climb"),
        ("bear", "can", "climb"),
    ])

    # === SIZE & MISC ===
    facts.extend([
        ("elephant", "is", "large"),
        ("whale", "is", "large"),
        ("giraffe", "is", "large"),
        ("lion", "is", "large"),
        ("bear", "is", "large"),
        ("tiger", "is", "large"),
        ("mouse", "is", "small"),
        ("ant", "is", "small"),
        ("bee", "is", "small"),
        ("sparrow", "is", "small"),
        ("butterfly", "is", "small"),
        # roles
        ("lion", "is", "predator"),
        ("tiger", "is", "predator"),
        ("eagle", "is", "predator"),
        ("hawk", "is", "predator"),
        ("shark", "is", "predator"),
        ("crocodile", "is", "predator"),
        ("rabbit", "is", "prey"),
        ("mouse", "is", "prey"),
        ("deer", "is", "prey"),
        ("fish", "is", "prey"),
        # nocturnal
        ("owl", "is", "nocturnal"),
        ("bat", "is", "nocturnal"),
        ("mouse", "is", "nocturnal"),
    ])

    return facts


# =====================================================================
#  PPMI K matrix
# =====================================================================
def build_K(facts, vocab_idx):
    N = len(vocab_idx)
    C = np.zeros((N, N))
    for s, r, o in facts:
        if s in vocab_idx and o in vocab_idx:
            i, j = vocab_idx[s], vocab_idx[o]
            C[i, j] += 1
            C[j, i] += 1
    total = C.sum()
    row_t = C.sum(axis=1)
    col_t = C.sum(axis=0)
    PPMI = np.zeros_like(C)
    for i in range(N):
        for j in range(N):
            if C[i, j] > 0 and row_t[i] > 0 and col_t[j] > 0:
                p_ij = C[i, j] / total
                p_i = row_t[i] / total
                p_j = col_t[j] / total
                pmi = np.log(p_ij / (p_i * p_j))
                PPMI[i, j] = max(0, pmi)
    return PPMI, C


def build_vocab(facts):
    entities = set()
    for s, r, o in facts:
        entities.add(s)
        entities.add(o)
    vocab = sorted(entities)
    return vocab, {w: i for i, w in enumerate(vocab)}


# =====================================================================
#  Oscillator with deflation cascade
# =====================================================================
def embed(K, n_dims=12, depth=8, verbose=True):
    N = len(K)
    K_res = K.copy()
    osc = GFDOscillator(dt=0.05, steps=2000)
    embedding = np.zeros((N, n_dims))
    eigvals = []
    for k in range(n_dims):
        graph = GFDOscillator.encode_weighted(N, K_res)
        state = osc.run_phase(graph, depth=depth, seed=42 + k * 137)
        if state.Sv[0] < 1e-10:
            break
        v = state.Vt[0] / np.linalg.norm(state.Vt[0])
        lam = float(v @ K_res @ v)
        eigvals.append(lam)
        embedding[:, k] = v * np.sqrt(abs(lam))
        K_res = K_res - lam * np.outer(v, v)
        if verbose and k < 3:
            print(f"    mode {k}: λ={lam:.3f}, top contributing nodes...")
    return embedding, eigvals


# =====================================================================
#  Query helpers
# =====================================================================
def cos_sim(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na > 1e-12 and nb > 1e-12 else 0.0


def nearest(target, embedding, vocab, k=5):
    if target not in vocab:
        return []
    tv = embedding[vocab.index(target)]
    sims = []
    for i, w in enumerate(vocab):
        if w == target:
            continue
        sims.append((w, cos_sim(tv, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k]


def cluster_kmeans(embedding, vocab, n_clusters=8, max_iter=50, seed=0):
    rng = np.random.RandomState(seed)
    N = len(vocab)
    init = rng.choice(N, n_clusters, replace=False)
    centers = embedding[init].copy()
    assign = np.zeros(N, dtype=int)
    for _ in range(max_iter):
        new_assign = np.zeros(N, dtype=int)
        for i in range(N):
            d = [np.linalg.norm(embedding[i] - centers[c]) for c in range(n_clusters)]
            new_assign[i] = int(np.argmin(d))
        if np.array_equal(new_assign, assign):
            break
        assign = new_assign
        for c in range(n_clusters):
            members = [i for i in range(N) if assign[i] == c]
            if members:
                centers[c] = np.mean(embedding[members], axis=0)
    groups = defaultdict(list)
    for i, w in enumerate(vocab):
        groups[int(assign[i])].append(w)
    return groups


def multi_hop(start, relation_chain, embedding, vocab, k=3):
    """
    Composition: traverse relation_chain from start.
    relation_chain = list of (relation_offset_word) — we use the relation's
    semantic vector as a translation.

    More concretely: for "what does cat hunt", we look at
    cat's embedding and find what (cat - generic_animal + generic_prey) is closest to.
    For multi-hop, chain these.
    """
    if start not in vocab:
        return []
    cur = embedding[vocab.index(start)]
    for relation in relation_chain:
        if relation not in vocab:
            continue
        # Translate by the relation's embedding
        cur = cur + embedding[vocab.index(relation)] * 0.3
    sims = []
    for i, w in enumerate(vocab):
        if w == start:
            continue
        sims.append((w, cos_sim(cur, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k]


# =====================================================================
def main():
    print("=" * 78)
    print(" LARGE ONTOLOGY LEARNER — ~300 entities, ~600 facts")
    print("=" * 78)

    facts = build_facts()
    vocab, vocab_idx = build_vocab(facts)
    N = len(vocab)
    print(f"\n  Facts: {len(facts)}")
    print(f"  Unique entities: {N}")

    print(f"\n  Building PPMI matrix...")
    t0 = time.time()
    K, C = build_K(facts, vocab_idx)
    print(f"    PPMI: {time.time()-t0:.2f}s, {(C>0).sum()} nonzero co-occurrences")

    print(f"\n  Running oscillator with deflation cascade (12 modes)...")
    t0 = time.time()
    emb, eigvals = embed(K, n_dims=12, depth=8, verbose=True)
    t_train = time.time() - t0
    print(f"    {t_train:.1f}s for {len(eigvals)} modes")
    print(f"    Eigenvalues: {[f'{e:.2f}' for e in eigvals]}")

    # === Query 1: Cluster structure ===
    print("\n" + "─" * 78)
    print("  Q1: Cluster discovery (k=8)")
    print("─" * 78)
    clusters = cluster_kmeans(emb, vocab, n_clusters=8)
    for cid in sorted(clusters.keys()):
        members = sorted(clusters[cid])
        n = len(members)
        sample = ', '.join(members[:10]) + (f" ... +{n-10}" if n > 10 else "")
        print(f"  Cluster {cid} ({n}): {sample}")

    # === Query 2: Specific neighbors ===
    print("\n" + "─" * 78)
    print("  Q2: Nearest neighbors")
    print("─" * 78)
    targets = ["lion", "shark", "eagle", "frog", "bee", "elephant",
               "predator", "ocean", "feathers", "scales"]
    for w in targets:
        if w in vocab:
            nn = nearest(w, emb, vocab, k=5)
            nn_str = ", ".join(f"{n}({s:+.2f})" for n, s in nn)
            print(f"  {w:>14s} → {nn_str}")

    # === Query 3: Hidden attribute discovery ===
    print("\n" + "─" * 78)
    print("  Q3: 'Predator' nearest neighbors — does the abstract concept cluster?")
    print("─" * 78)
    if "predator" in vocab:
        nn = nearest("predator", emb, vocab, k=10)
        for n, s in nn:
            print(f"    {n:>14s}  cos = {s:+.3f}")

    # === Query 4: Multi-hop reasoning ===
    print("\n" + "─" * 78)
    print("  Q4: Cross-domain transfer")
    print("─" * 78)

    # Flying creatures (intersection of "fly" and animal-like things)
    if "fly" in vocab:  # both verb and the insect; tricky
        print(f"  Things near 'fly' (the verb):")
        nn = nearest("fly", emb, vocab, k=8)
        for n, s in nn[:8]:
            print(f"    {n:>14s}  cos = {s:+.3f}")

    if "ocean" in vocab:
        print(f"\n  Things that live near 'ocean':")
        nn = nearest("ocean", emb, vocab, k=8)
        for n, s in nn[:8]:
            print(f"    {n:>14s}  cos = {s:+.3f}")

    # === Online evolution ===
    print("\n" + "═" * 78)
    print("  ONLINE EVOLUTION — add 15 new entities, observe placement")
    print("═" * 78)
    new_facts = [
        ("squirrel", "is_a", "mammal"),
        ("squirrel", "lives_in", "forest"),
        ("squirrel", "eats", "nut"),
        ("squirrel", "can", "climb"),
        ("nut", "is_a", "food"),
        ("hummingbird", "is_a", "bird"),
        ("hummingbird", "can", "fly"),
        ("hummingbird", "eats", "nectar"),
        ("falcon", "is_a", "bird"),
        ("falcon", "is", "predator"),
        ("falcon", "hunts", "mouse"),
        ("falcon", "can", "fly"),
        ("camel", "is_a", "mammal"),
        ("camel", "lives_in", "desert"),
        ("camel", "eats", "grass"),
    ]
    print(f"  Adding {len(new_facts)} facts → introduces: squirrel, nut, hummingbird, falcon, camel")

    extended = facts + new_facts
    vocab2, vocab_idx2 = build_vocab(extended)
    K2, _ = build_K(extended, vocab_idx2)
    print(f"\n  Re-running oscillator on extended ontology...")
    t0 = time.time()
    emb2, _ = embed(K2, n_dims=12, depth=8, verbose=False)
    print(f"    {time.time()-t0:.1f}s, vocabulary {N} → {len(vocab2)}")

    print(f"\n  New entities placed at:")
    for w in ["squirrel", "hummingbird", "falcon", "camel"]:
        nn = nearest(w, emb2, vocab2, k=5)
        nn_str = ", ".join(f"{n}({s:+.2f})" for n, s in nn)
        print(f"    {w:>14s} → {nn_str}")


if __name__ == "__main__":
    main()
