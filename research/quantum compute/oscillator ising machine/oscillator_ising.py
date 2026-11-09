"""
Oscillator Ising Sampler
========================

A D-Wave-compatible sampler built on the GFD oscillator's phase dynamics.

It accepts any binary quadratic model in D-Wave's own format (dimod BQM:
Ising with fields, or QUBO) and returns a dimod SampleSet, so it can be used
anywhere a D-Wave sampler is used, including D-Wave's problem libraries
(for example dwave_networkx.maximum_cut or min_vertex_color).

The dynamics
------------
Each spin s_i is an oscillator with phase phi_i. The sampler runs gradient
flow on the continuous energy

    H(phi) = sum_i h_i cos(phi_i)
           + sum_{i<j} J_ij cos(phi_i - phi_j)
           - (k_s / 2) sum_i cos(2 phi_i),

so that

    dphi_i/dt =  h_i sin(phi_i)
               + sum_j J_ij sin(phi_i - phi_j)        (Kuramoto coupling, K = -J)
               - k_s sin(2 phi_i)                     (second-harmonic locking)
               + noise.

When every phase is 0 or pi, cos(phi_i) = s_i and cos(phi_i - phi_j) = s_i s_j,
so H equals the Ising energy E(s) = sum h_i s_i + sum J_ij s_i s_j exactly
(up to the constant locking term). The locking strength k_s ramps from 0 to
k_s_max and the noise ramps down to 0 over the run, an annealing schedule.
The spin read out is s_i = sign(cos phi_i). Phases are taken in the frame
rotating with the common natural frequency, so the field term has a fixed
reference.

Relation to the original GFD oscillator (../graph solver/gfd_oscillator.py)
--------------------------------------------------------------------------
The coupling term is the same Kuramoto coupling. This sampler adds the three
things an Ising machine needs: a field input h_i, second-harmonic locking so
each oscillator settles to a spin, and an annealing schedule. It reads spins
directly instead of through an SVD of the phase state.

Stephen Nelson, Field Dynamics Research
"""

import numpy as np
import scipy.sparse as sp
import dimod


class OscillatorIsingSampler(dimod.Sampler):
    """Sample low-energy states of a BQM with annealed oscillator dynamics.

    Parameters of ``sample``
    ------------------------
    num_reads : int        independent runs (all integrated together)
    steps : int            integration steps per run
    dt : float             time step (coefficients are normalised to max |h|, |J| = 1)
    ks_max : float         final second-harmonic locking strength
    noise : float          initial noise amplitude, ramped linearly to zero
    seed : int or None     random seed
    """

    parameters = {"num_reads": [], "steps": [], "dt": [], "ks_max": [],
                  "noise": [], "seed": []}
    properties = {"description": "annealed oscillator Ising machine (GFD phase dynamics)"}

    def sample(self, bqm, num_reads=10, steps=8000, dt=0.02, ks_max=1.5,
               noise=1.0, seed=None, **kwargs):
        original_vartype = bqm.vartype
        spin = bqm.change_vartype(dimod.SPIN, inplace=False)
        labels = list(spin.variables)
        n = len(labels)
        if n == 0:
            return dimod.SampleSet.from_samples([], original_vartype, energy=[])
        index = {v: k for k, v in enumerate(labels)}

        h = np.array([spin.linear[v] for v in labels], dtype=float)
        rows, cols, vals = [], [], []
        for (u, v), bias in spin.quadratic.items():
            i, j = index[u], index[v]
            rows += [i, j]; cols += [j, i]; vals += [bias, bias]
        J = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))

        scale = max(np.abs(h).max(initial=0.0), np.abs(J.data).max(initial=0.0), 1e-12)
        h, J = h / scale, J / scale

        rng = np.random.default_rng(seed)
        phi = rng.uniform(0.0, 2.0 * np.pi, (n, num_reads))
        sqrt_dt = np.sqrt(dt)
        for t in range(steps):
            frac = t / steps
            c, s = np.cos(phi), np.sin(phi)
            # sum_j J_ij sin(phi_i - phi_j) = sin(phi_i) (J cos)_i - cos(phi_i) (J sin)_i
            coupling = s * (J @ c) - c * (J @ s)
            drift = h[:, None] * s + coupling - ks_max * frac * np.sin(2.0 * phi)
            phi += dt * drift
            if noise > 0.0:
                phi += noise * (1.0 - frac) * sqrt_dt * rng.standard_normal(phi.shape)

        spins = np.where(np.cos(phi) >= 0.0, 1, -1).T.astype(np.int8)
        sampleset = dimod.SampleSet.from_samples_bqm((spins, labels), spin)
        sampleset.info["phases"] = phi.T % (2.0 * np.pi)      # final phases, one row per read,
        sampleset.info["phase_variables"] = labels            # columns in this variable order
        return sampleset.change_vartype(original_vartype, inplace=False)


def continuous_energy(bqm, phases, ks=0.0):
    """H(phi) for a BQM, with phases given as a mapping {variable: phase} (used by the tests)."""
    spin = bqm.change_vartype(dimod.SPIN, inplace=False)
    E = spin.offset + sum(h * np.cos(phases[v]) for v, h in spin.linear.items())
    E += sum(J * np.cos(phases[u] - phases[v]) for (u, v), J in spin.quadratic.items())
    return float(E - 0.5 * ks * sum(np.cos(2 * phases[v]) for v in spin.variables))


def phases_of(sampleset, read=0):
    """The final phases of one read as a mapping {variable: phase}."""
    return dict(zip(sampleset.info["phase_variables"], sampleset.info["phases"][read]))
