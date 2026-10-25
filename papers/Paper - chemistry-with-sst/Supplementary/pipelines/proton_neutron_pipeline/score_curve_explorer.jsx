import { useState, useMemo } from "react";

const muSST = (x) => {
  if (x <= 0) return 0;
  return ((2 * x + 1) - Math.sqrt(4 * x + 1)) / (2 * x);
};

const alpha = 1 / (137 + 1 / 28);

// Precompute sigma
const MAX_A = 210;
const sigma = [0];
for (let i = 1; i <= MAX_A; i++) {
  sigma.push(sigma[i - 1] + muSST(i * i));
}

const scoreFn = (Z, A) => {
  const N = A - Z;
  if (Z < 1 || N < 1) return -9999;
  const lam = alpha * (2 - muSST(A));
  const coupling = Math.sqrt(sigma[Z] * sigma[N]);
  const coulomb = lam * Z * (Z - 1) / Math.pow(A, 1 / 3);
  return coupling - coulomb;
};

const couplingFn = (Z, A) => {
  const N = A - Z;
  if (Z < 1 || N < 1) return 0;
  return Math.sqrt(sigma[Z] * sigma[N]);
};

const coulombFn = (Z, A) => {
  if (Z < 1 || A - Z < 1) return 0;
  const lam = alpha * (2 - muSST(A));
  return lam * Z * (Z - 1) / Math.pow(A, 1 / 3);
};

const elements = [
  { Z: 2, sym: "He", A: 4 }, { Z: 3, sym: "Li", A: 7 },
  { Z: 4, sym: "Be", A: 9 }, { Z: 6, sym: "C", A: 12 },
  { Z: 7, sym: "N", A: 14 }, { Z: 8, sym: "O", A: 16 },
  { Z: 10, sym: "Ne", A: 20 }, { Z: 12, sym: "Mg", A: 24 },
  { Z: 14, sym: "Si", A: 28 }, { Z: 16, sym: "S", A: 32 },
  { Z: 20, sym: "Ca", A: 40 }, { Z: 22, sym: "Ti", A: 48 },
  { Z: 26, sym: "Fe", A: 56 }, { Z: 28, sym: "Ni", A: 58 },
  { Z: 30, sym: "Zn", A: 64 }, { Z: 36, sym: "Kr", A: 84 },
  { Z: 40, sym: "Zr", A: 90 }, { Z: 50, sym: "Sn", A: 120 },
  { Z: 56, sym: "Ba", A: 138 }, { Z: 62, sym: "Sm", A: 152 },
  { Z: 76, sym: "Os", A: 192 }, { Z: 82, sym: "Pb", A: 208 },
];

export default function App() {
  const [selectedIdx, setSelectedIdx] = useState(12); // Fe-56
  const [showComponents, setShowComponents] = useState(false);
  const [showDerivative, setShowDerivative] = useState(false);

  const el = elements[selectedIdx];

  const data = useMemo(() => {
    const points = [];
    let bestZ = 1, bestS = -Infinity;
    for (let z = 1; z < el.A; z++) {
      const s = scoreFn(z, el.A);
      const c = couplingFn(z, el.A);
      const cb = coulombFn(z, el.A);
      points.push({ z, score: s, coupling: c, coulomb: cb });
      if (s > bestS) { bestS = s; bestZ = z; }
    }
    // Compute derivative (dS/dZ)
    for (let i = 0; i < points.length; i++) {
      if (i === 0) points[i].deriv = points[1].score - points[0].score;
      else if (i === points.length - 1) points[i].deriv = points[i].score - points[i-1].score;
      else points[i].deriv = (points[i+1].score - points[i-1].score) / 2;
    }
    // Second derivative
    for (let i = 0; i < points.length; i++) {
      if (i === 0 || i === points.length - 1) points[i].deriv2 = 0;
      else points[i].deriv2 = points[i+1].score - 2*points[i].score + points[i-1].score;
    }
    return { points, bestZ, bestS };
  }, [el]);

  const diff = data.bestZ - el.Z;
  const hit = diff === 0;

  // SVG dimensions
  const W = 800, H = 400, pad = { t: 30, r: 30, b: 50, l: 70 };
  const plotW = W - pad.l - pad.r;
  const plotH = H - pad.t - pad.b;

  // Scales
  const zMin = 1, zMax = el.A - 1;
  const scores = data.points.map(p => p.score).filter(s => s > -9000);
  const sMin = Math.min(...scores);
  const sMax = Math.max(...scores);
  const sRange = sMax - sMin || 1;

  const xScale = (z) => pad.l + ((z - zMin) / (zMax - zMin)) * plotW;
  const yScale = (s) => pad.t + plotH - ((s - sMin) / sRange) * plotH;

  // Derivative scales
  const derivs = data.points.map(p => p.deriv);
  const dMin = Math.min(...derivs);
  const dMax = Math.max(...derivs);
  const dRange = Math.max(Math.abs(dMin), Math.abs(dMax)) || 1;
  const yScaleDeriv = (d) => pad.t + plotH/2 - (d / dRange) * (plotH/2) * 0.9;

  // Build SVG path for score
  const scorePath = data.points
    .filter(p => p.score > -9000)
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${xScale(p.z).toFixed(1)},${yScale(p.score).toFixed(1)}`)
    .join(' ');

  const couplingPath = data.points
    .filter(p => p.coupling > 0)
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${xScale(p.z).toFixed(1)},${yScale(p.coupling).toFixed(1)}`)
    .join(' ');

  const coulombPath = data.points
    .filter(p => p.z > 1)
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${xScale(p.z).toFixed(1)},${yScale(p.coulomb).toFixed(1)}`)
    .join(' ');

  const derivPath = data.points
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${xScale(p.z).toFixed(1)},${yScaleDeriv(p.deriv).toFixed(1)}`)
    .join(' ');

  // Score at actual Z
  const scoreAtActual = scoreFn(el.Z, el.A);
  const gap = data.bestS - scoreAtActual;

  return (
    <div style={{ fontFamily: "system-ui", padding: 16, background: "#0a0a0a", color: "#e0e0e0", minHeight: "100vh" }}>
      <div style={{ marginBottom: 16, display: "flex", flexWrap: "wrap", gap: 6 }}>
        {elements.map((e, i) => {
          const d = (() => {
            let bz = 1, bs = -Infinity;
            for (let z = 1; z < e.A; z++) {
              const s = scoreFn(z, e.A);
              if (s > bs) { bs = s; bz = z; }
            }
            return bz - e.Z;
          })();
          const isHit = d === 0;
          return (
            <button key={i} onClick={() => setSelectedIdx(i)}
              style={{
                padding: "4px 8px", fontSize: 12, cursor: "pointer",
                border: i === selectedIdx ? "2px solid #60a0ff" : "1px solid #444",
                borderRadius: 4,
                background: isHit ? "#1a2a1a" : "#2a1a1a",
                color: isHit ? "#80ff80" : "#ff8080",
                fontWeight: i === selectedIdx ? "bold" : "normal",
              }}>
              {e.sym}-{e.A} {isHit ? "✓" : `${d > 0 ? "+" : ""}${d}`}
            </button>
          );
        })}
      </div>

      <div style={{ marginBottom: 12, fontSize: 18, fontWeight: "bold" }}>
        {el.sym}-{el.A}: Z_actual = {el.Z}, Z_pred = {data.bestZ}
        <span style={{ color: hit ? "#80ff80" : "#ff8080", marginLeft: 12 }}>
          {hit ? "✓ EXACT" : `${diff > 0 ? "+" : ""}${diff} MISS`}
        </span>
        <span style={{ color: "#888", marginLeft: 12, fontSize: 14 }}>
          gap = {gap.toFixed(6)} ({(gap/data.bestS*100).toFixed(4)}%)
        </span>
      </div>

      <div style={{ marginBottom: 12, display: "flex", gap: 16 }}>
        <label style={{ cursor: "pointer" }}>
          <input type="checkbox" checked={showComponents} onChange={() => setShowComponents(!showComponents)} />
          {" "}Show coupling & coulomb
        </label>
        <label style={{ cursor: "pointer" }}>
          <input type="checkbox" checked={showDerivative} onChange={() => setShowDerivative(!showDerivative)} />
          {" "}Show dS/dZ (derivative)
        </label>
      </div>

      <svg width={W} height={H} style={{ background: "#111", borderRadius: 8 }}>
        {/* Grid */}
        {[0.25, 0.5, 0.75].map(f => (
          <line key={f} x1={pad.l} x2={W-pad.r}
            y1={pad.t + plotH * (1-f)} y2={pad.t + plotH * (1-f)}
            stroke="#222" strokeWidth={1} />
        ))}

        {/* Components */}
        {showComponents && (
          <>
            <path d={couplingPath} fill="none" stroke="#4488ff44" strokeWidth={1.5} />
            <path d={coulombPath} fill="none" stroke="#ff444444" strokeWidth={1.5} />
          </>
        )}

        {/* Score curve */}
        <path d={scorePath} fill="none" stroke="#60d060" strokeWidth={2.5} />

        {/* Derivative */}
        {showDerivative && (
          <>
            <line x1={pad.l} x2={W-pad.r} y1={yScaleDeriv(0)} y2={yScaleDeriv(0)}
              stroke="#666" strokeWidth={1} strokeDasharray="4,4" />
            <path d={derivPath} fill="none" stroke="#ffaa00" strokeWidth={1.5} />
          </>
        )}

        {/* Actual Z line */}
        <line x1={xScale(el.Z)} x2={xScale(el.Z)} y1={pad.t} y2={pad.t + plotH}
          stroke="#ff6666" strokeWidth={2} strokeDasharray="6,4" />
        <circle cx={xScale(el.Z)} cy={yScale(scoreAtActual)} r={5} fill="#ff6666" />
        <text x={xScale(el.Z) + 6} y={pad.t + 15} fill="#ff6666" fontSize={12} fontWeight="bold">
          Z={el.Z}
        </text>

        {/* Predicted Z line */}
        <line x1={xScale(data.bestZ)} x2={xScale(data.bestZ)} y1={pad.t} y2={pad.t + plotH}
          stroke="#6666ff" strokeWidth={2} strokeDasharray="6,4" />
        <circle cx={xScale(data.bestZ)} cy={yScale(data.bestS)} r={5} fill="#6666ff" />
        <text x={xScale(data.bestZ) - 40} y={pad.t + 15} fill="#6666ff" fontSize={12} fontWeight="bold">
          pred={data.bestZ}
        </text>

        {/* Coupling peak (A/2) */}
        <line x1={xScale(Math.floor(el.A/2))} x2={xScale(Math.floor(el.A/2))}
          y1={pad.t + plotH - 5} y2={pad.t + plotH + 5}
          stroke="#888" strokeWidth={1} />
        <text x={xScale(Math.floor(el.A/2))} y={pad.t + plotH + 18}
          fill="#888" fontSize={10} textAnchor="middle">A/2</text>

        {/* Axes */}
        <line x1={pad.l} x2={W-pad.r} y1={pad.t+plotH} y2={pad.t+plotH} stroke="#666" />
        <line x1={pad.l} x2={pad.l} y1={pad.t} y2={pad.t+plotH} stroke="#666" />

        {/* X axis labels */}
        {Array.from({ length: 5 }, (_, i) => {
          const z = Math.round(zMin + (zMax - zMin) * i / 4);
          return (
            <text key={i} x={xScale(z)} y={pad.t + plotH + 30} fill="#aaa" fontSize={11} textAnchor="middle">
              {z}
            </text>
          );
        })}
        <text x={W/2} y={H - 5} fill="#aaa" fontSize={12} textAnchor="middle">Z (candidate proton count)</text>

        {/* Y axis labels */}
        {[0, 0.25, 0.5, 0.75, 1].map(f => {
          const val = sMin + sRange * f;
          return (
            <text key={f} x={pad.l - 8} y={pad.t + plotH * (1-f) + 4} fill="#aaa" fontSize={10} textAnchor="end">
              {val.toFixed(1)}
            </text>
          );
        })}
        <text x={15} y={H/2} fill="#aaa" fontSize={12} textAnchor="middle"
          transform={`rotate(-90, 15, ${H/2})`}>Score S(Z)</text>

        {/* Legend */}
        <rect x={W-pad.r-150} y={pad.t+5} width={140} height={showComponents ? 80 : 50} fill="#0008" rx={4} />
        <line x1={W-pad.r-140} x2={W-pad.r-120} y1={pad.t+20} y2={pad.t+20} stroke="#60d060" strokeWidth={2.5} />
        <text x={W-pad.r-115} y={pad.t+24} fill="#60d060" fontSize={11}>Score S(Z)</text>
        <line x1={W-pad.r-140} x2={W-pad.r-120} y1={pad.t+38} y2={pad.t+38} stroke="#ff6666" strokeWidth={2} strokeDasharray="4,3" />
        <text x={W-pad.r-115} y={pad.t+42} fill="#ff6666" fontSize={11}>Z actual</text>
        {showComponents && (
          <>
            <line x1={W-pad.r-140} x2={W-pad.r-120} y1={pad.t+56} y2={pad.t+56} stroke="#4488ff66" strokeWidth={1.5} />
            <text x={W-pad.r-115} y={pad.t+60} fill="#4488ff" fontSize={11}>Coupling</text>
            <line x1={W-pad.r-140} x2={W-pad.r-120} y1={pad.t+74} y2={pad.t+74} stroke="#ff444466" strokeWidth={1.5} />
            <text x={W-pad.r-115} y={pad.t+78} fill="#ff4444" fontSize={11}>Coulomb</text>
          </>
        )}
      </svg>

      <div style={{ marginTop: 16, fontSize: 13, color: "#aaa", maxWidth: 800 }}>
        <strong style={{ color: "#ddd" }}>What to look for:</strong> The green curve is the full series of scores S(Z) across every possible split.
        The blue dashed line marks the argmax (predicted Z). The red dashed line marks the actual Z.
        For misses, they're always adjacent — the curve is nearly flat at the peak and the actual Z sits on the shoulder.
        The question: does the <em>shape</em> of the full curve — its asymmetry, its width, its tails — contain information
        that could resolve which shoulder is correct?
      </div>
    </div>
  );
}
