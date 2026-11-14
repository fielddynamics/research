"""Uniform k-grid over the diamond (fcc) reciprocal primitive cell, in the units where the
conventional cell has side 4."""
import numpy as np
LEGS = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
A = np.array([(0, 2, 2), (2, 0, 2), (2, 2, 0)], float)
B = 2 * np.pi * np.linalg.inv(A).T          # rows b_i with a_i . b_j = 2 pi delta_ij


def kgrid(m):
    s = (np.arange(m) + 0.5) / m
    f = np.array(np.meshgrid(s, s, s, indexing="ij")).reshape(3, -1).T
    return f @ B
