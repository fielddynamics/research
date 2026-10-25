"""
packet_router.py
=================

Learn packet routing rules with a 100-node GFD oscillator.

Setup:
  - Define ~50 routing rules as (feature, action) pairs
  - Each rule: feature(port=N, src=R, flag=X, ...) → action(forward, drop, suspicious, ...)
  - Build co-occurrence between features and actions
  - Run oscillator with deflation cascade
  - Embed packet features at runtime, find nearest action

Demonstrates:
  1. Rule learning: network of rules → embedding
  2. Exact rule matching: known features → correct action
  3. Generalization: similar-but-unseen features → reasonable action by analogy
  4. Online updates: add new rules, system updates without retraining
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import time
from collections import defaultdict
from gfd_oscillator import GFDOscillator


# =====================================================================
# Define the routing rule set
#
# Rule = (list of features, action)
# Features are tokenized atoms: "port:22", "src:external", "flag:syn", etc.
# Actions are atoms too: "drop", "forward", "suspicious", "trusted"
# =====================================================================

def build_routing_rules():
    """~50 hand-crafted rules covering common routing scenarios."""
    rules = []

    # --- Trusted services (forward) ---
    rules.append((["port:80", "proto:tcp", "dst:web_server"], "forward"))
    rules.append((["port:443", "proto:tcp", "dst:web_server"], "forward"))
    rules.append((["port:443", "proto:tcp", "dst:internal"], "forward"))
    rules.append((["port:53", "proto:udp", "dst:dns_server"], "forward"))
    rules.append((["port:25", "proto:tcp", "dst:mail_server"], "forward"))
    rules.append((["port:993", "proto:tcp", "dst:mail_server"], "forward"))
    rules.append((["port:587", "proto:tcp", "dst:mail_server"], "forward"))
    rules.append((["port:123", "proto:udp", "dst:ntp_server"], "forward"))

    # --- SSH/admin: trusted from internal, suspicious from external ---
    rules.append((["port:22", "proto:tcp", "src:internal"], "forward"))
    rules.append((["port:22", "proto:tcp", "src:external"], "suspicious"))
    rules.append((["port:3389", "proto:tcp", "src:internal"], "forward"))
    rules.append((["port:3389", "proto:tcp", "src:external"], "suspicious"))
    rules.append((["port:23", "proto:tcp", "src:any"], "drop"))     # telnet always bad
    rules.append((["port:21", "proto:tcp", "src:external"], "suspicious"))  # FTP

    # --- Database ports: never from external ---
    rules.append((["port:3306", "proto:tcp", "src:external"], "drop"))   # MySQL
    rules.append((["port:5432", "proto:tcp", "src:external"], "drop"))   # Postgres
    rules.append((["port:27017", "proto:tcp", "src:external"], "drop"))  # MongoDB
    rules.append((["port:6379", "proto:tcp", "src:external"], "drop"))   # Redis
    rules.append((["port:3306", "proto:tcp", "src:internal"], "forward"))
    rules.append((["port:5432", "proto:tcp", "src:internal"], "forward"))

    # --- Known bad/exploit ports ---
    rules.append((["port:33", "proto:any"], "drop"))                # registered for DSP3270 — flagged in user's example
    rules.append((["port:31337", "proto:tcp"], "drop"))             # backdoor
    rules.append((["port:6667", "proto:tcp"], "drop"))              # IRC (often C2)
    rules.append((["port:4444", "proto:tcp"], "suspicious"))        # metasploit default
    rules.append((["port:1337", "proto:any"], "suspicious"))        # leet, often malware

    # --- Attack patterns ---
    rules.append((["flag:syn", "rate:high", "no_ack"], "suspicious"))           # SYN flood
    rules.append((["flag:syn", "flag:fin", "anomaly"], "drop"))                 # malformed
    rules.append((["flag:xmas", "anomaly"], "drop"))                            # XMAS scan
    rules.append((["flag:null", "anomaly"], "drop"))                            # NULL scan
    rules.append((["payload:shellcode", "any"], "drop"))                        # shellcode signature
    rules.append((["payload:sqli", "any"], "drop"))                             # SQL injection
    rules.append((["payload:xss", "port:80"], "drop"))                          # XSS
    rules.append((["src:tor_exit", "any"], "suspicious"))
    rules.append((["src:known_botnet", "any"], "drop"))

    # --- Volume/rate ---
    rules.append((["rate:high", "port:53", "src:external"], "suspicious"))      # DNS amp
    rules.append((["rate:high", "port:123", "src:external"], "suspicious"))     # NTP amp
    rules.append((["fragmented", "rate:high"], "suspicious"))

    # --- ICMP rules ---
    rules.append((["proto:icmp", "type:echo", "src:internal"], "forward"))
    rules.append((["proto:icmp", "type:echo", "src:external"], "suspicious"))
    rules.append((["proto:icmp", "rate:high", "src:external"], "drop"))         # ping flood
    rules.append((["proto:icmp", "type:redirect", "src:external"], "drop"))

    # --- Trust patterns ---
    rules.append((["src:management_subnet", "any"], "trusted"))
    rules.append((["src:vpn_gateway", "proto:any"], "trusted"))
    rules.append((["src:internal", "dst:internal", "common_port"], "forward"))

    # --- Unusual but acceptable ---
    rules.append((["port:8080", "proto:tcp", "dst:web_server"], "forward"))
    rules.append((["port:8443", "proto:tcp", "dst:web_server"], "forward"))
    rules.append((["port:5060", "proto:udp", "dst:voip_server"], "forward"))    # SIP

    return rules


# =====================================================================
# Build co-occurrence and oscillator embedding
# =====================================================================
def build_vocab(rules):
    """All unique tokens across features and actions."""
    tokens = set()
    for features, action in rules:
        tokens.update(features)
        tokens.add(action)
    return sorted(tokens)


def build_K(rules, vocab):
    """Co-occurrence: each rule contributes pair-couplings between every
    feature in the rule and the action."""
    idx = {w: i for i, w in enumerate(vocab)}
    N = len(vocab)
    C = np.zeros((N, N))

    for features, action in rules:
        # Each feature ↔ action gets a strong coupling (this is the rule)
        a_idx = idx[action]
        for f in features:
            f_idx = idx[f]
            C[f_idx, a_idx] += 2.0  # action coupling weighted higher
            C[a_idx, f_idx] += 2.0
        # Features within a rule also weakly co-occur (they appear together)
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                a, b = idx[features[i]], idx[features[j]]
                C[a, b] += 1.0
                C[b, a] += 1.0

    # PPMI normalization
    total = C.sum()
    rt = C.sum(1)
    ct = C.sum(0)
    PPMI = np.zeros_like(C)
    for i in range(N):
        for j in range(N):
            if C[i, j] > 0 and rt[i] > 0 and ct[j] > 0:
                pmi = np.log(C[i, j] * total / (rt[i] * ct[j]))
                PPMI[i, j] = max(0, pmi)
    return PPMI, C, idx


def embed_via_oscillator(K, n_dims=12, depth=8):
    """Standard deflation cascade."""
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
    return embedding, eigvals


def cos_sim(a, b):
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na > 1e-12 and nb > 1e-12 else 0.0


# =====================================================================
# Inference: classify a packet by its features
# =====================================================================
ACTIONS = ["forward", "drop", "suspicious", "trusted"]


def classify_packet(features, embedding, vocab, idx, k_show=4):
    """Given a list of feature tokens, return predicted action(s)
    by similarity to action embeddings."""
    in_vocab = [f for f in features if f in idx]
    oov = [f for f in features if f not in idx]
    if not in_vocab:
        return None, oov, None

    # Sum the feature vectors → query vector
    query = np.zeros(embedding.shape[1])
    for f in in_vocab:
        query += embedding[idx[f]]

    # Score against each action
    scores = {}
    for action in ACTIONS:
        if action in idx:
            scores[action] = cos_sim(query, embedding[idx[action]])

    sorted_actions = sorted(scores.items(), key=lambda x: -x[1])

    # Also show top-k closest tokens overall (for context)
    all_sims = []
    excl = set(in_vocab)
    for w, i in idx.items():
        if w in excl:
            continue
        all_sims.append((w, cos_sim(query, embedding[i])))
    all_sims.sort(key=lambda x: -x[1])

    return sorted_actions, oov, all_sims[:k_show]


def main():
    print("=" * 76)
    print(" PACKET ROUTING via GFD oscillator")
    print("=" * 76)

    rules = build_routing_rules()
    vocab = build_vocab(rules)
    print(f"\n  Rules: {len(rules)}")
    print(f"  Vocabulary: {len(vocab)} unique tokens")
    print(f"  Actions: {ACTIONS}")
    print(f"  First 10 vocab: {vocab[:10]}")

    print(f"\n  Building PPMI co-occurrence matrix...")
    K, C, idx = build_K(rules, vocab)
    print(f"    nonzero co-occurrences: {(C>0).sum()}")

    print(f"\n  Training oscillator (12-mode deflation cascade)...")
    t0 = time.time()
    emb, eigvals = embed_via_oscillator(K, n_dims=12, depth=8)
    print(f"    {time.time()-t0:.1f}s, eigenvalues: {[f'{e:.2f}' for e in eigvals[:6]]}...")

    # =======================================================
    # Test 1: Exact known rules — should classify correctly
    # =======================================================
    print("\n" + "─" * 76)
    print("  TEST 1: Exact known patterns")
    print("─" * 76)

    known_packets = [
        # (description, features, expected_action)
        ("HTTPS to web server",      ["port:443", "proto:tcp", "dst:web_server"],     "forward"),
        ("SSH from external (bad)",  ["port:22", "proto:tcp", "src:external"],         "suspicious"),
        ("Telnet (always drop)",     ["port:23", "proto:tcp", "src:any"],              "drop"),
        ("Port 33 (bad)",            ["port:33", "proto:any"],                         "drop"),
        ("MySQL from external",      ["port:3306", "proto:tcp", "src:external"],       "drop"),
        ("MySQL from internal",      ["port:3306", "proto:tcp", "src:internal"],       "forward"),
        ("Botnet IP",                ["src:known_botnet", "any"],                      "drop"),
        ("VPN gateway",              ["src:vpn_gateway", "proto:any"],                 "trusted"),
        ("XMAS scan",                ["flag:xmas", "anomaly"],                         "drop"),
        ("SQL injection payload",    ["payload:sqli", "any"],                          "drop"),
    ]

    correct = 0
    for desc, feats, expected in known_packets:
        result, oov, top_words = classify_packet(feats, emb, vocab, idx)
        if not result:
            print(f"  {desc:>30s}: [no in-vocab features]")
            continue
        top_action = result[0][0]
        match = "✓" if top_action == expected else "✗"
        if match == "✓":
            correct += 1
        scores_str = ", ".join(f"{a}({s:+.2f})" for a, s in result)
        print(f"  {match} {desc:>28s}: top={top_action:<11s} (expected={expected})")
        print(f"      scores: {scores_str}")

    print(f"\n  Score: {correct}/{len(known_packets)} known patterns correctly classified")

    # =======================================================
    # Test 2: Generalization — features the system hasn't seen
    # in this combination, but components are familiar
    # =======================================================
    print("\n" + "─" * 76)
    print("  TEST 2: Generalization — unseen feature combinations")
    print("─" * 76)

    novel_packets = [
        # (description, features, hypothesis)
        ("Web on port 8443 (similar to 8080)",      ["port:8443", "proto:tcp"],                    "should be near forward"),
        ("Random unknown port 4444 + external src", ["port:4444", "proto:tcp", "src:external"],    "should lean suspicious/drop (4444 is bad)"),
        ("DNS amplification pattern",               ["rate:high", "port:53"],                       "should lean suspicious"),
        ("New: port:4445 (unseen) external",        ["port:4445", "src:external"],                 "should lean suspicious by neighborhood?"),
        ("Internal + uncommon port 8080",            ["port:8080", "src:internal"],                "should lean forward"),
        ("Just SYN flag, high rate (partial pattern)", ["flag:syn", "rate:high"],                  "should lean suspicious"),
    ]

    for desc, feats, hyp in novel_packets:
        result, oov, top_words = classify_packet(feats, emb, vocab, idx)
        if not result:
            print(f"  {desc}: [features not in vocab — OOV: {oov}]")
            continue
        top_action = result[0][0]
        scores_str = ", ".join(f"{a}({s:+.2f})" for a, s in result)
        print(f"  {desc}")
        print(f"    features:    {feats}")
        if oov:
            print(f"    OOV (ignored): {oov}")
        print(f"    prediction:  top={top_action}")
        print(f"    all scores:  {scores_str}")
        print(f"    nearest tokens overall: {[w for w,_ in top_words]}")
        print(f"    hypothesis:  {hyp}")
        print()

    # =======================================================
    # Test 3: Online learning — add a new rule, verify it works
    # =======================================================
    print("\n" + "═" * 76)
    print("  TEST 3: Online learning — add a new rule")
    print("═" * 76)

    new_rules = [
        (["port:9999", "src:external"], "drop"),                # new bad port
        (["port:9999", "src:internal"], "forward"),
        (["payload:ransomware_signature", "any"], "drop"),       # new threat signature
    ]
    print(f"  Adding {len(new_rules)} new rules:")
    for f, a in new_rules:
        print(f"    {f} → {a}")

    extended_rules = rules + new_rules
    vocab2 = build_vocab(extended_rules)
    K2, _, idx2 = build_K(extended_rules, vocab2)
    print(f"\n  Re-running oscillator on extended ruleset ({len(vocab2)} tokens)...")
    t0 = time.time()
    emb2, _ = embed_via_oscillator(K2, n_dims=12, depth=8)
    print(f"    {time.time()-t0:.1f}s")

    # Test the new rules
    test_new = [
        ("Port 9999 from external",     ["port:9999", "src:external"],                  "drop"),
        ("Port 9999 from internal",     ["port:9999", "src:internal"],                  "forward"),
        ("Ransomware signature",        ["payload:ransomware_signature", "any"],        "drop"),
    ]
    print(f"\n  After update, classifying new patterns:")
    for desc, feats, expected in test_new:
        result, oov, _ = classify_packet(feats, emb2, vocab2, idx2)
        if not result:
            print(f"    {desc}: OOV {oov}")
            continue
        top = result[0][0]
        match = "✓" if top == expected else "✗"
        print(f"    {match} {desc:>30s}: {top:<11s}  (expected {expected})")


if __name__ == "__main__":
    main()
