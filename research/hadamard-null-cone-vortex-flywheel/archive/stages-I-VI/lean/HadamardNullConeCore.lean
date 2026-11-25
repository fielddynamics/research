import HadamardCubeFrame
import WalshEigenmodes
import Mathlib.Data.Matrix.Notation

/-!
# Finite integer certificates for the Hadamard null-cone core
DRAFT — not compiled. Explicitly ordered matrices reproduce the Python geometry.
The imported parent proofs provide context; a reindexing lemma linking these finite
matrices to their abstract definitions remains to be written. No physical theorem
is claimed here. No sorry or native_decide is used in this draft.
-/
namespace HadamardNullConeCore
set_option maxRecDepth 10000
set_option maxHeartbeats 0

/-- A finite integer dot product, using a computable list rather than a quotient. -/
def dot {n : Nat} (a b : Fin n → Int) : Int :=
  (List.ofFn (fun i => a i * b i)).sum

def L : Fin 6 → Fin 12 → Int :=
  ![![-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
  ![1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0],
  ![0, 1, 0, 0, 1, 0, 0, -1, -1, 0, 0, 0],
  ![0, 0, 0, 0, 0, 1, 0, 1, 0, -1, -1, 0],
  ![0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, -1],
  ![0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1]]

def D : Fin 12 → Fin 8 → Int :=
  ![![1, 0, 0, 0, 0, 0, 0, -1],
  ![-1, 0, 0, 0, 0, 0, 1, 0],
  ![0, 1, 0, 0, 0, 0, -1, 0],
  ![0, -1, 0, 0, 0, 0, 0, 1],
  ![1, 0, 0, 0, 0, -1, 0, 0],
  ![0, 0, -1, 0, 0, 1, 0, 0],
  ![0, 0, 1, 0, 0, 0, 0, -1],
  ![0, 0, 0, 1, 0, -1, 0, 0],
  ![0, 0, 0, -1, 0, 0, 1, 0],
  ![0, 0, 0, 1, -1, 0, 0, 0],
  ![0, 0, -1, 0, 1, 0, 0, 0],
  ![0, 1, 0, 0, -1, 0, 0, 0]]

def W : Fin 8 → Fin 8 → Int :=
  ![![1, 1, 1, 1, 1, 1, 1, 1],
  ![1, 1, -1, -1, 1, -1, -1, 1],
  ![1, -1, 1, -1, -1, 1, -1, 1],
  ![1, -1, -1, 1, -1, -1, 1, 1],
  ![1, -1, -1, -1, 1, 1, 1, -1],
  ![1, -1, 1, 1, 1, -1, -1, -1],
  ![1, 1, -1, 1, -1, 1, -1, -1],
  ![1, 1, 1, -1, -1, -1, 1, -1]]

def S : Fin 8 → Fin 3 → Int :=
  ![![1, 1, 1],
  ![1, -1, -1],
  ![-1, 1, -1],
  ![-1, -1, 1],
  ![-1, -1, -1],
  ![-1, 1, 1],
  ![1, -1, 1],
  ![1, 1, -1]]

def K : Fin 12 → Fin 3 → Int :=
  ![![0, 0, 1],
  ![0, -1, 0],
  ![0, 0, -1],
  ![0, 1, 0],
  ![1, 0, 0],
  ![0, 0, 1],
  ![-1, 0, 0],
  ![0, -1, 0],
  ![1, 0, 0],
  ![0, 0, 1],
  ![0, -1, 0],
  ![1, 0, 0]]

def adj : Fin 8 → Fin 8 → Int :=
  ![![0, 0, 0, 0, 0, 1, 1, 1],
  ![0, 0, 0, 0, 1, 0, 1, 1],
  ![0, 0, 0, 0, 1, 1, 0, 1],
  ![0, 0, 0, 0, 1, 1, 1, 0],
  ![0, 1, 1, 1, 0, 0, 0, 0],
  ![1, 0, 1, 1, 0, 0, 0, 0],
  ![1, 1, 0, 1, 0, 0, 0, 0],
  ![1, 1, 1, 0, 0, 0, 0, 0]]

def eigenvalue : Fin 8 → Int := ![0, 2, 2, 2, 4, 4, 4, 6]

def delta {n : Nat} (i j : Fin n) : Int := if i = j then 1 else 0

theorem boundary_boundary : ∀ (i : Fin 6) (j : Fin 8),
    dot (L i) (fun k => D k j) = 0 := by decide

theorem closed_surface : ∀ i : Fin 12,
    dot (D i) (fun _ => 1) = 0 := by decide

theorem face_gram : ∀ (i j : Fin 8),
    dot (fun k => D k i) (fun k => D k j) = 3 * delta i j - adj i j := by decide

theorem walsh_orthogonality : ∀ (i j : Fin 8),
    dot (fun k => W k i) (fun k => W k j) = 8 * delta i j := by decide

theorem walsh_laplacian : ∀ (i j : Fin 8),
    dot (fun k => 3 * delta i k - adj i k) (fun k => W k j) = W i j * eigenvalue j := by decide

theorem ring_identity : ∀ (i : Fin 12) (j : Fin 3),
    dot (D i) (fun k => S k j) = 2 * K i j := by decide

theorem ring_orthogonality : ∀ (i j : Fin 3),
    dot (fun k => K k i) (fun k => K k j) = 4 * delta i j := by decide

end HadamardNullConeCore
