"""
mini_word_embedding.py
=======================

Miniature unsupervised word embedding via GFD oscillator dynamics on a
PPMI co-occurrence matrix.

Corpus: ~10 hand-crafted sentences with obvious semantic structure.
Goal: show that the oscillator clusters semantically related words
      WITHOUT any training, gradient descent, or backprop.

Method:
  1. Tokenize sentences.
  2. Build co-occurrence matrix C[i,j] = #(word_i within window of word_j).
  3. Convert to PPMI: log(P(i,j) / (P(i) * P(j))) clipped at 0.
  4. Use PPMI as the coupling matrix K for the GFD oscillator.
  5. Run oscillator dynamics; SVD readout gives word embeddings.
  6. Compute cosine similarities between word pairs.
  7. Verify expected clusters by eye.

If "cat" and "dog" come out close, and "mat" and "rug" come out close,
and "fish" and "meat" come out close — we've demonstrated that
unsupervised dynamics finds semantic structure.

Compare to: SVD of PPMI directly (the closed-form answer that
oscillator dynamics is supposed to converge to).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from collections import Counter, defaultdict
from gfd_oscillator import GFDOscillator


# ---------------------------------------------------------------
#  Hand-crafted corpus with deliberate semantic structure
# ---------------------------------------------------------------
CORPUS = [
    # Cats and dogs as animal subjects, mat/rug as resting surfaces
    "the cat sits on the mat",
    "the dog sits on the rug",
    "the cat sleeps on the mat",
    "the dog sleeps on the rug",
    # Eating verbs distinguish food
    "the cat eats fish",
    "the dog eats meat",
    "the cat likes fish",
    "the dog likes meat",
    # Reinforce subject/object pairings
    "a cat is on a mat",
    "a dog is on a rug",
    "cats eat fish daily",
    "dogs eat meat daily",
    # Singular vs plural same-cluster
    "the cats sit on mats",
    "the dogs sit on rugs",
    # A few cross-statements to test discrimination
    "fish swim in water",
    "meat comes from animals",
    "mats are soft and warm",
    "rugs are soft and warm",
]

WINDOW = 2  # words on each side count as context


# ---------------------------------------------------------------
#  Tokenize and build vocabulary
# ---------------------------------------------------------------
def tokenize(corpus):
    tokens = []
    for sentence in corpus:
        tokens.append(sentence.lower().split())
    return tokens


def build_vocab(tokenized):
    flat = [w for s in tokenized for w in s]
    vocab = sorted(set(flat))
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    return vocab, word_to_idx, Counter(flat)


# ---------------------------------------------------------------
#  Co-occurrence matrix and PPMI
# ---------------------------------------------------------------
def build_cooccurrence(tokenized, word_to_idx, window=2):
    N = len(word_to_idx)
    C = np.zeros((N, N))
    for sentence in tokenized:
        for i, w in enumerate(sentence):
            wi = word_to_idx[w]
            lo = max(0, i - window)
            hi = min(len(sentence), i + window + 1)
            for j in range(lo, hi):
                if j != i:
                    wj = word_to_idx[sentence[j]]
                    C[wi, wj] += 1
    return C


def cooccurrence_to_ppmi(C):
    """Positive Pointwise Mutual Information.
       PPMI[i,j] = max(0, log(P(i,j) / (P(i) P(j))))
    """
    total = C.sum()
    if total == 0:
        return C
    row_totals = C.sum(axis=1)
    col_totals = C.sum(axis=0)

    PPMI = np.zeros_like(C)
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            if C[i, j] > 0 and row_totals[i] > 0 and col_totals[j] > 0:
                p_ij = C[i, j] / total
                p_i = row_totals[i] / total
                p_j = col_totals[j] / total
                pmi = np.log(p_ij / (p_i * p_j))
                PPMI[i, j] = max(0, pmi)
    return PPMI


# ---------------------------------------------------------------
#  Two embedding methods to compare
# ---------------------------------------------------------------
def embedding_via_svd(K, n_dims=4):
    """Direct SVD of K. The closed-form answer the oscillator should match."""
    # PPMI matrices aren't symmetric in general for finite samples, but
    # ours will be by construction.  Use eigendecomposition of K = K^T.
    K_sym = (K + K.T) / 2
    eigvals, eigvecs = np.linalg.eigh(K_sym)
    # Keep the top n_dims by absolute eigenvalue
    idx = np.argsort(-np.abs(eigvals))[:n_dims]
    embedding = eigvecs[:, idx] * np.sqrt(np.abs(eigvals[idx]))
    return embedding


def embedding_via_oscillator(K, n_dims=4, depth=8):
    """Run the GFD oscillator with deflation cascade to extract n_dims modes.

    Single-shot oscillator finds only the dominant eigenmode of K. To get
    multiple semantic dimensions, we extract one mode, deflate K by it,
    extract the next, etc. — building a rank-n_dims embedding from
    rank-1 oscillator pieces.
    """
    N = len(K)
    K_residual = K.copy()
    osc = GFDOscillator(dt=0.05, steps=2000)

    embedding = np.zeros((N, n_dims))
    eigvals_recovered = []
    sv_history = []

    for k in range(n_dims):
        graph = GFDOscillator.encode_weighted(N, K_residual)
        state = osc.run_phase(graph, depth=depth, seed=42 + k * 137)
        sv_history.append(state.Sv[:4].tolist())

        if state.Sv[0] < 1e-10:
            break  # nothing left to extract

        # Mode 0 is the current dominant eigenvector
        v = state.Vt[0].copy()
        v = v / np.linalg.norm(v)

        # Eigenvalue: λ = v^T K v (Rayleigh quotient)
        lam = float(v @ K_residual @ v)
        eigvals_recovered.append(lam)

        # This mode is the k-th column of the embedding, scaled by sqrt(|λ|)
        embedding[:, k] = v * np.sqrt(abs(lam))

        # Deflate K_residual by this rank-1 piece
        K_residual = K_residual - lam * np.outer(v, v)

    return embedding, eigvals_recovered, sv_history


# ---------------------------------------------------------------
#  Similarity and analysis
# ---------------------------------------------------------------
def cosine_similarity(a, b):
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def nearest_neighbors(target, embedding, vocab, k=5, exclude_self=True):
    target_vec = embedding[vocab.index(target)]
    sims = []
    for i, w in enumerate(vocab):
        if exclude_self and w == target:
            continue
        sims.append((w, cosine_similarity(target_vec, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k]


def report_pairs(embedding, vocab, name):
    """Specific pairs we expect to be close (semantic) or far (unrelated)."""
    print(f"\n  {name}:")
    expected_close = [
        ("cat", "dog"),
        ("mat", "rug"),
        ("fish", "meat"),
        ("sits", "sleeps"),
        ("eats", "likes"),
        ("cats", "dogs"),
    ]
    expected_far = [
        ("cat", "fish"),
        ("dog", "rug"),
        ("eats", "soft"),
    ]
    for a, b in expected_close:
        if a in vocab and b in vocab:
            sim = cosine_similarity(
                embedding[vocab.index(a)], embedding[vocab.index(b)])
            mark = "✓" if sim > 0.3 else "?"
            print(f"    {a:>8s} ↔ {b:<8s}  cos = {sim:>+.3f}  (expect close) {mark}")

    for a, b in expected_far:
        if a in vocab and b in vocab:
            sim = cosine_similarity(
                embedding[vocab.index(a)], embedding[vocab.index(b)])
            mark = "✓" if sim < 0.5 else "?"
            print(f"    {a:>8s} ↔ {b:<8s}  cos = {sim:>+.3f}  (expect far)   {mark}")


def main():
    print("=" * 76)
    print(" Miniature unsupervised word embedding via GFD oscillator")
    print("=" * 76)

    # 1. Build vocabulary
    tokenized = tokenize(CORPUS)
    vocab, word_to_idx, freq = build_vocab(tokenized)
    print(f"\n  Corpus: {len(CORPUS)} sentences, {sum(len(t) for t in tokenized)} tokens, {len(vocab)} unique words")
    print(f"  Vocabulary: {vocab}")

    # 2. Co-occurrence and PPMI
    C = build_cooccurrence(tokenized, word_to_idx, window=WINDOW)
    PPMI = cooccurrence_to_ppmi(C)

    print(f"\n  Co-occurrence stats: total = {int(C.sum())}, nonzero entries = {(C > 0).sum()}")
    print(f"  PPMI nonzero: {(PPMI > 0).sum()} entries")
    print(f"  PPMI max = {PPMI.max():.3f}, mean (nonzero) = {PPMI[PPMI > 0].mean():.3f}")

    # 3a. SVD baseline (closed-form answer)
    n_dims = 4
    emb_svd = embedding_via_svd(PPMI, n_dims=n_dims)
    print(f"\n  SVD baseline: {emb_svd.shape}")

    # 3b. Oscillator dynamics with deflation cascade
    emb_osc, eigvals, sv_hist = embedding_via_oscillator(PPMI, n_dims=n_dims, depth=8)
    print(f"  Oscillator (cascade) embedding: {emb_osc.shape}")
    print(f"  Eigenvalues recovered: {[f'{e:.3f}' for e in eigvals]}")
    print(f"  Per-stage Sv[0..3]:")
    for k, sv in enumerate(sv_hist):
        print(f"    stage {k}: {[f'{s:.3f}' for s in sv]}")

    # 4. Test expected pairs
    print("\n" + "─" * 76)
    print("  EXPECTED-PAIR CHECKS")
    print("─" * 76)
    report_pairs(emb_svd, vocab, "SVD baseline (closed form)")
    report_pairs(emb_osc, vocab, "Oscillator dynamics")

    # 5. Nearest neighbors for key words
    print("\n" + "─" * 76)
    print("  NEAREST NEIGHBORS (oscillator embedding)")
    print("─" * 76)
    for w in ["cat", "dog", "mat", "fish", "eats", "sits"]:
        if w in vocab:
            nn = nearest_neighbors(w, emb_osc, vocab, k=4)
            nn_str = ", ".join(f"{n}({s:+.2f})" for n, s in nn)
            print(f"  {w:>6s}  →  {nn_str}")

    # 6. Comparison metric
    print("\n" + "─" * 76)
    print("  AGREEMENT BETWEEN SVD AND OSCILLATOR")
    print("─" * 76)
    # For each word, compare its SVD-similarity-rank vs oscillator-similarity-rank
    target_words = ["cat", "dog", "fish", "mat", "rug", "eats"]
    for tw in target_words:
        if tw not in vocab:
            continue
        # Top-3 NN in each
        nn_svd = [n for n, _ in nearest_neighbors(tw, emb_svd, vocab, k=3)]
        nn_osc = [n for n, _ in nearest_neighbors(tw, emb_osc, vocab, k=3)]
        agreement = len(set(nn_svd) & set(nn_osc)) / 3
        print(f"  {tw:>6s}  SVD top-3: {nn_svd}")
        print(f"  {tw:>6s}  OSC top-3: {nn_osc}      agreement: {agreement:.0%}")
        print()


if __name__ == "__main__":
    main()
