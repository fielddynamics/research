#!/usr/bin/env python3
"""
Spectral Kernel v2
==================
Universal boolean gate with pre-flight bridge validation.

spectral()           — runs kernel, raises on fatal bridge error, returns result
validate_bridges()   — inspects bridges, reports errors, runs kernel if clean
"""

import torch
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ═══════════════════════════════════════════════
# H — built once
# ═══════════════════════════════════════════════

def build_H(n, dev=None):
    if dev is None:
        dev = device
    c = torch.arange(n, device=dev)
    b = torch.arange(n, device=dev)
    cb = c[:, None] & b[None, :]
    x = cb.long()
    x = x - ((x >> 1) & 0x5555555555555555)
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0F
    x = (x * 0x0101010101010101) >> 56
    return 1.0 - 2.0 * (x % 2).float()

# Default H at N=16
N = 16
H = build_H(N, device)

# ═══════════════════════════════════════════════
# EXCEPTIONS
# ═══════════════════════════════════════════════

class SpectralBridgeError(Exception):
    """Raised when one or more bridges have fatal validation failures."""
    def __init__(self, errors):
        self.errors = errors
        lines = [f"{len(errors)} bridge error(s):"]
        for e in errors:
            lines.append(f"  Tick {e['tick']}: {e['message']}")
        super().__init__("\n".join(lines))

# ═══════════════════════════════════════════════
# PRE-FLIGHT CHECK
# ═══════════════════════════════════════════════

def _preflight(bridges, margin_threshold=0.1):
    """
    Check bridges for fatal errors and weak margins.
    Returns list of error/warning dicts (empty = all clean).
    """
    b = bridges[:, 0, :] if bridges.dim() == 3 else bridges
    n = b.shape[1]
    h = H if n == N else build_H(n, b.device)

    raw = b @ h.T                              # (ticks, N) — one matmul
    abs_raw = raw.abs()
    margins = abs_raw.min(dim=1).values        # (ticks,)

    # Global fast exit: if everything is above threshold, done
    if margins.min().item() >= margin_threshold:
        return []

    # Something is wrong — only now do we inspect per-tick
    errors = []
    nz_counts = (b.abs() > 0.001).sum(dim=1)  # only compute when needed

    for t in range(b.shape[0]):
        margin = margins[t].item()
        if margin >= margin_threshold:
            continue

        nz = int(nz_counts[t].item())

        # Skip uniform bridges (identity/negation) — all values same
        if nz == n:
            std = b[t].std().item()
            if std < 0.01:
                continue

        if nz == 0:
            errors.append({
                "tick": t, "severity": "WARN", "type": "ALL_ZERO",
                "margin": 0.0, "channels_active": 0,
                "message": "bridge is all zeros — output will be constant +1 (all bits 0)"
            })
        elif margin < 1e-6:
            dead = (abs_raw[t] < 1e-6).nonzero(as_tuple=True)[0].tolist()
            errors.append({
                "tick": t, "severity": "FATAL", "type": "DEAD_CHANNEL",
                "margin": 0.0, "channels_active": nz, "dead_inputs": dead,
                "message": f"margin=0.000 — {len(dead)} input(s) produce zero output: {dead[:5]}{'...' if len(dead) > 5 else ''}"
            })
        else:
            weakest = abs_raw[t].argmin().item()
            weak_count = (abs_raw[t] < margin_threshold).sum().item()
            errors.append({
                "tick": t, "severity": "WARN", "type": "WEAK_MARGIN",
                "margin": round(margin, 6), "channels_active": nz,
                "weakest_input": weakest, "weakest_raw": round(raw[t, weakest].item(), 6),
                "vulnerable_count": weak_count,
                "message": f"margin={margin:.4f} — input {weakest} (raw={raw[t, weakest].item():+.4f}), {weak_count}/{n} below threshold"
            })

    return errors

    return errors

# ═══════════════════════════════════════════════
# THE KERNEL
# ═══════════════════════════════════════════════

def spectral(state, bridges, validate=False, margin_threshold=0.1):
    """
    state:    (batch, N) float ±1
    bridges:  (ticks, batch, N) or (ticks, N)

    validate: False → skip checks (default, assume bridges pre-validated)
              True  → preflight, raise SpectralBridgeError on FATAL

    returns:  (batch, N) float ±1
    raises:   SpectralBridgeError on fatal bridge errors
    """
    n = state.shape[1]
    h = build_H(n, state.device) if n != N else H

    if validate:
        errors = _preflight(bridges, margin_threshold)
        fatal = [e for e in errors if e["severity"] == "FATAL"]
        if fatal:
            raise SpectralBridgeError(fatal)

    for t in range(bridges.shape[0]):
        bridge = bridges[t]
        transform = state @ h
        filtered = bridge * transform
        candidate = filtered @ h / n
        state = torch.sign(candidate)
        state[state == 0] = 1.0
    return state

# ═══════════════════════════════════════════════
# VALIDATE BRIDGES
# ═══════════════════════════════════════════════

def validate_bridges(bridges, state=None, margin_threshold=0.1, show_passing=False):
    """
    Full bridge inspection. Runs kernel if no fatal errors and state provided.

    bridges:          (ticks, N) or (ticks, batch, N)
    state:            (batch, N) optional — runs kernel on clean bridges
    margin_threshold: minimum acceptable margin
    show_passing:     False → report only errors/warnings (default)
                      True  → report every tick

    returns: dict {
        "status":   "PASS" | "WARN" | "FAIL",
        "ticks":    total tick count,
        "errors":   [...]  only fatal errors,
        "warnings": [...]  only warnings,
        "result":   tensor or None,
        "details":  [...]  only if show_passing=True
    }
    """
    if bridges.dim() == 3:
        bridge_set = bridges[:, 0, :]
    else:
        bridge_set = bridges

    ticks = bridge_set.shape[0]
    n = bridge_set.shape[1]
    h = build_H(n, bridge_set.device) if n != N else H

    all_issues = _preflight(bridges, margin_threshold)
    fatal = [e for e in all_issues if e["severity"] == "FATAL"]
    warnings = [e for e in all_issues if e["severity"] == "WARN"]

    if fatal:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"

    # Build full details if requested
    details = None
    if show_passing:
        raw = bridge_set @ h.T
        abs_raw = raw.abs()
        margins = abs_raw.min(dim=1).values
        nonzero_counts = (bridge_set.abs() > 0.001).sum(dim=1)

        # Detect filter bridges
        bmin = bridge_set.min(dim=1).values
        bmax = bridge_set.max(dim=1).values
        is_id = (bmin > 0.99) & (bmax < 1.01)
        is_neg = (bmin > -1.01) & (bmax < -0.99)

        issue_ticks = {e["tick"]: e for e in all_issues}
        details = []
        for t in range(ticks):
            if t in issue_ticks:
                details.append(issue_ticks[t])
            elif is_id[t]:
                details.append({
                    "tick": t,
                    "severity": "PASS",
                    "type": "IDENTITY",
                    "margin": None,
                    "channels_active": int(nonzero_counts[t].item()),
                    "message": "identity filter — pass-through"
                })
            elif is_neg[t]:
                details.append({
                    "tick": t,
                    "severity": "PASS",
                    "type": "NEGATION",
                    "margin": None,
                    "channels_active": int(nonzero_counts[t].item()),
                    "message": "negation filter — flip all"
                })
            else:
                details.append({
                    "tick": t,
                    "severity": "PASS",
                    "type": "OK",
                    "margin": round(margins[t].item(), 6),
                    "channels_active": int(nonzero_counts[t].item()),
                    "message": f"margin={margins[t].item():.4f}, {int(nonzero_counts[t].item())} channels"
                })

    # Run kernel if clean and state provided
    result = None
    if state is not None and not fatal:
        result = spectral(state, bridges, validate=False)

    report = {
        "status": status,
        "ticks": ticks,
        "errors": fatal,
        "warnings": warnings,
        "result": result,
    }
    if details is not None:
        report["details"] = details

    return report

# ═══════════════════════════════════════════════
# MAKE A BRIDGE FROM A TRUTH TABLE
# ═══════════════════════════════════════════════

def make_bridge(truth_table):
    tt = torch.tensor(truth_table, dtype=torch.float32, device=device)
    return (H @ (1.0 - 2.0 * tt)) / N

# ═══════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Device: {device}")
    print(f"H: {N}×{N}")
    print()

    bridge_and = make_bridge([(v&1) & ((v>>1)&1) for v in range(N)])
    bridge_xor = make_bridge([(v&1) ^ ((v>>1)&1) for v in range(N)])
    state = torch.ones(1, N, device=device)
    state[0, 1::2] = -1.0

    # ── Test 1: Clean program ──
    print("=" * 60)
    print("  Test 1: Clean bridges")
    print("=" * 60)
    clean = torch.stack([bridge_and, bridge_xor])
    report = validate_bridges(clean, show_passing=True)
    print(f"  Status: {report['status']}")
    for d in report["details"]:
        print(f"    Tick {d['tick']}: [{d['severity']}] {d['message']}")

    # ── Test 2: All-zero bridge (WARN, not fatal) ──
    print()
    print("=" * 60)
    print("  Test 2: All-zero bridge")
    print("=" * 60)
    bad = torch.stack([bridge_and, torch.zeros(N, device=device)])
    report = validate_bridges(bad)
    print(f"  Status: {report['status']}")
    for w in report["warnings"]:
        print(f"    Tick {w['tick']}: [{w['severity']}] {w['message']}")

    # ── Test 3: Identity (all +1) — dead channels ──
    print()
    print("=" * 60)
    print("  Test 3: Identity bridge (all +1)")
    print("=" * 60)
    identity = torch.stack([bridge_and, torch.ones(N, device=device)])
    report = validate_bridges(identity, show_passing=True)
    print(f"  Status: {report['status']}")
    for d in report["details"]:
        print(f"    Tick {d['tick']}: [{d['severity']}] {d['message']}")

    # ── Test 4: Kernel raises on fatal (dead channel) ──
    print()
    print("=" * 60)
    print("  Test 4: Kernel raises SpectralBridgeError")
    print("=" * 60)
    # Bridge with cancelling channels → margin=0 on some inputs
    dead_bridge = torch.zeros(N, device=device)
    dead_bridge[0] = 0.5; dead_bridge[1] = 0.5; dead_bridge[2] = -0.5; dead_bridge[3] = -0.5
    fatal_prog = torch.stack([bridge_and, dead_bridge])
    try:
        spectral(state, fatal_prog.unsqueeze(1), validate=True)
        print("  ERROR: should have raised!")
    except SpectralBridgeError as e:
        print(f"  Caught: {e}")

    # ── Test 5: validate=False skips checks ──
    print()
    print("=" * 60)
    print("  Test 5: validate=False")
    print("=" * 60)
    result = spectral(state, bad.unsqueeze(1), validate=False)
    print(f"  Ran OK. Shape: {result.shape}")

    # ── Test 6: validate_bridges runs kernel when clean ──
    print()
    print("=" * 60)
    print("  Test 6: validate_bridges with state (clean)")
    print("=" * 60)
    report = validate_bridges(clean.unsqueeze(1), state=state)
    print(f"  Status: {report['status']}")
    print(f"  Result: {report['result']}")

    # ── Test 7: validate_bridges blocks kernel on fatal ──
    print()
    print("=" * 60)
    print("  Test 7: validate_bridges with state (fatal)")
    print("=" * 60)
    report = validate_bridges(fatal_prog.unsqueeze(1), state=state)
    print(f"  Status: {report['status']}")
    print(f"  Result: {report['result']}")
    for e in report["errors"]:
        print(f"    Tick {e['tick']}: [{e['severity']}] {e['message']}")

    # ── Test 8: Weak margin ──
    print()
    print("=" * 60)
    print("  Test 8: Weak margin bridge")
    print("=" * 60)
    weak = torch.zeros(N, device=device)
    weak[0] = 0.5; weak[1] = 0.5; weak[2] = -0.5; weak[3] = 0.48
    program = torch.stack([bridge_and, weak])
    report = validate_bridges(program, show_passing=True, margin_threshold=0.1)
    print(f"  Status: {report['status']}")
    for d in report["details"]:
        print(f"    Tick {d['tick']}: [{d['severity']}] {d['message']}")

    # ── Benchmark: overhead ──
    print()
    print("=" * 60)
    print("  Benchmark: default (no validation) vs explicit validation")
    print("=" * 60)
    prog = torch.randn(64, N, device=device) * 0.3
    st = torch.sign(torch.rand(10000, N, device=device) - 0.5)
    st[st == 0] = 1.0
    br = prog.unsqueeze(1).expand(64, 10000, -1)

    # Default: validate=False (zero overhead)
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(100):
        spectral(st.clone(), br)
    torch.cuda.synchronize()
    t_default = time.time() - t0

    # Explicit: validate=True
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(100):
        spectral(st.clone(), br, validate=True)
    torch.cuda.synchronize()
    t_val = time.time() - t0

    overhead = (t_val - t_default) / t_default * 100
    print(f"  Default (validate=False): {t_default*10:.1f} ms/call")
    print(f"  Explicit (validate=True): {t_val*10:.1f} ms/call")
    print(f"  Validation cost:          {overhead:.1f}%")
