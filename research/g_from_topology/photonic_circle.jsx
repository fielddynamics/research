import { useState, useEffect, useRef, useCallback } from "react";

const K = 4;
const D = 3;
const N_SECTORS = K ** D; // 64
const ALPHA = 1 / 137.035999177;
const TAU = 2 * Math.PI;

// BBP weights and offsets
const BBP_WEIGHTS = [4, -2, -3, -3];
const BBP_OFFSETS = [1, 4, 5, 6];
const BBP_BASE = 2 ** D; // 8

// Coupling polynomial
const fPoly = (s) => 1 + s * K + K * K;

// Compute BBP sum for π up to n terms
function bbpPartial(nTerms) {
  let sum = 0;
  for (let k = 0; k < nTerms; k++) {
    const base_pow = Math.pow(1 / 16, k);
    sum += base_pow * (
      4 / (8 * k + 1) -
      2 / (8 * k + 4) -
      1 / (8 * k + 5) -
      1 / (8 * k + 6)
    );
  }
  return sum;
}

// Map a sector index (0-63) to its hierarchical position
function sectorHierarchy(n) {
  const face = Math.floor(n / 16);       // 0-3 (which face)
  const channel = Math.floor((n % 16) / 4); // 0-3 (which channel)
  const subchannel = n % 4;              // 0-3 (which sub-channel)
  return { face, channel, subchannel };
}

// Determine which band a sector's COUPLING LEVEL belongs to
function sectorBand(n) {
  const { face, channel, subchannel } = sectorHierarchy(n);
  // Band 2: sub-channel level (16 harmonics)
  // Band 1: channel level (4 harmonics)  
  // Band 0: face level (1 harmonic)
  // The coupling level: face gives 1, channel gives K, subchannel gives K²
  return 2; // All 64 sectors are at the sub-channel level of the full tiling
}

// Color palette
const COLORS = {
  bg: "#0a0b0f",
  bgCard: "#12141a",
  bgCardHover: "#1a1d26",
  face0: "#ff6b6b",
  face1: "#4ecdc4",
  face2: "#45b7d1",
  face3: "#f9ca24",
  band0: "#ff6b6b",
  band1: "#4ecdc4",
  band2: "#45b7d1",
  accent: "#f9ca24",
  text: "#e8e6e3",
  textDim: "#6b7280",
  textMuted: "#3d4250",
  gold: "#f9ca24",
  gridLine: "#1e2030",
  active: "#22c55e",
  silent: "#374151",
  inverted: "#ef4444",
};

const FACE_COLORS = [COLORS.face0, COLORS.face1, COLORS.face2, COLORS.face3];

function CircleSVG({ step, signature, showBBP, showBands, hoveredSector, setHoveredSector }) {
  const cx = 300, cy = 300, outerR = 260, innerR = 100;
  const bandR = [outerR, 210, 160, innerR];

  const sectors = [];
  for (let i = 0; i < N_SECTORS; i++) {
    const { face, channel, subchannel } = sectorHierarchy(i);
    const a0 = (i / N_SECTORS) * TAU - TAU / 4;
    const a1 = ((i + 1) / N_SECTORS) * TAU - TAU / 4;
    const cos0 = Math.cos(a0), sin0 = Math.sin(a0);
    const cos1 = Math.cos(a1), sin1 = Math.sin(a1);

    // Determine color based on signature
    let opacity = 0.8;
    let baseColor = FACE_COLORS[face];
    
    if (signature === 0) {
      // At origin: kinematic (channel) band goes silent
      // The 4 channel-level harmonics go to zero
      // Visually: dim the channel structure
      opacity = 0.7;
    } else if (signature === -1) {
      // In TetB: kinematic band inverts
      opacity = 0.6;
    }

    // Highlight if BBP walk is at this sector
    const isActive = showBBP && (i === step % N_SECTORS);
    const isRead = showBBP && (i < step);
    const isHovered = hoveredSector === i;

    const r1 = outerR;
    const r2 = showBands ? bandR[1] : innerR;

    const x1o = cx + r1 * cos0, y1o = cy + r1 * sin0;
    const x2o = cx + r1 * cos1, y2o = cy + r1 * sin1;
    const x1i = cx + r2 * cos0, y1i = cy + r2 * sin0;
    const x2i = cx + r2 * cos1, y2i = cy + r2 * sin1;

    const path = `M ${x1o} ${y1o} A ${r1} ${r1} 0 0 1 ${x2o} ${y2o} L ${x2i} ${y2i} A ${r2} ${r2} 0 0 0 ${x1i} ${y1i} Z`;

    sectors.push(
      <path
        key={`sector-${i}`}
        d={path}
        fill={baseColor}
        opacity={isActive ? 1 : isRead ? 0.3 : isHovered ? 0.95 : opacity}
        stroke={isActive ? COLORS.gold : isHovered ? "#fff" : COLORS.bg}
        strokeWidth={isActive ? 2 : isHovered ? 1.5 : 0.5}
        style={{ cursor: "pointer", transition: "opacity 0.15s" }}
        onMouseEnter={() => setHoveredSector(i)}
        onMouseLeave={() => setHoveredSector(null)}
      />
    );
  }

  // Band rings (if showing bands)
  const bandElements = [];
  if (showBands) {
    // Band 0: fundamental (1 harmonic) - innermost ring
    const b0R1 = bandR[3], b0R2 = bandR[2];
    bandElements.push(
      <circle key="band0" cx={cx} cy={cy} r={(b0R1 + b0R2) / 2}
        fill="none" stroke={COLORS.band0} strokeWidth={b0R2 - b0R1 - 4}
        opacity={0.3} strokeDasharray="none" />
    );
    // Band 1: first overtone (K harmonics) - middle ring
    for (let i = 0; i < K; i++) {
      const a0 = (i / K) * TAU - TAU / 4;
      const a1 = ((i + 1) / K) * TAU - TAU / 4;
      const r1 = bandR[2], r2 = bandR[1];
      const cos0 = Math.cos(a0), sin0 = Math.sin(a0);
      const cos1 = Math.cos(a1), sin1 = Math.sin(a1);
      const sWeight = signature;
      let col = COLORS.band1;
      let op = 0.4;
      if (sWeight === 0) { col = COLORS.silent; op = 0.15; }
      if (sWeight === -1) { col = COLORS.inverted; op = 0.35; }

      bandElements.push(
        <path key={`band1-${i}`}
          d={`M ${cx + r1 * cos0} ${cy + r1 * sin0} A ${r1} ${r1} 0 0 1 ${cx + r1 * cos1} ${cy + r1 * sin1} L ${cx + r2 * cos1} ${cy + r2 * sin1} A ${r2} ${r2} 0 0 0 ${cx + r2 * cos0} ${cy + r2 * sin0} Z`}
          fill={col} opacity={op} stroke={COLORS.bg} strokeWidth={0.5} />
      );
    }
    // Labels
    bandElements.push(
      <text key="b0-label" x={cx} y={cy - (b0R1 + b0R2) / 2 + 5} textAnchor="middle"
        fill={COLORS.text} fontSize="10" fontFamily="'JetBrains Mono', monospace" opacity={0.7}>
        Band 0: 1
      </text>
    );
    bandElements.push(
      <text key="b1-label" x={cx} y={cy - (bandR[2] + bandR[1]) / 2 + 5} textAnchor="middle"
        fill={COLORS.text} fontSize="10" fontFamily="'JetBrains Mono', monospace" opacity={0.7}>
        Band 1: {signature === 0 ? "s·4 = 0" : signature === -1 ? "s·4 = −4" : "s·4 = 4"}
      </text>
    );
    bandElements.push(
      <text key="b2-label" x={cx} y={cy - (bandR[1] + outerR) / 2 + 5} textAnchor="middle"
        fill={COLORS.text} fontSize="9" fontFamily="'JetBrains Mono', monospace" opacity={0.6}>
        Band 2: 16
      </text>
    );
  }

  // BBP walk trail
  const trailElements = [];
  if (showBBP && step > 0) {
    const trailLen = Math.min(step, N_SECTORS);
    for (let i = Math.max(0, step - trailLen); i < step; i++) {
      const idx = i % N_SECTORS;
      const angle = ((idx + 0.5) / N_SECTORS) * TAU - TAU / 4;
      const r = (outerR + (showBands ? bandR[1] : innerR)) / 2;
      const opacity = 0.2 + 0.6 * ((i - (step - trailLen)) / trailLen);
      trailElements.push(
        <circle key={`trail-${i}`}
          cx={cx + r * Math.cos(angle)} cy={cy + r * Math.sin(angle)}
          r={2.5} fill={COLORS.gold} opacity={opacity} />
      );
    }
    // Current position
    const curIdx = step % N_SECTORS;
    const curAngle = ((curIdx + 0.5) / N_SECTORS) * TAU - TAU / 4;
    const curR = (outerR + (showBands ? bandR[1] : innerR)) / 2;
    trailElements.push(
      <circle key="cursor"
        cx={cx + curR * Math.cos(curAngle)} cy={cy + curR * Math.sin(curAngle)}
        r={5} fill={COLORS.gold} stroke="#fff" strokeWidth={1.5}>
        <animate attributeName="r" values="5;7;5" dur="0.8s" repeatCount="indefinite" />
      </circle>
    );
  }

  // Center text
  const traceVal = fPoly(signature);

  return (
    <svg viewBox="0 0 600 600" style={{ width: "100%", maxWidth: 600 }}>
      <defs>
        <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#1a1d26" />
          <stop offset="100%" stopColor={COLORS.bg} />
        </radialGradient>
      </defs>
      <circle cx={cx} cy={cy} r={outerR + 20} fill="url(#bgGrad)" />
      {bandElements}
      {sectors}
      {trailElements}
      
      {/* Center display */}
      <circle cx={cx} cy={cy} r={showBands ? innerR - 5 : innerR - 5} fill={COLORS.bg} opacity={0.9} />
      <text x={cx} y={cy - 25} textAnchor="middle" fill={COLORS.gold}
        fontSize="14" fontFamily="'JetBrains Mono', monospace" fontWeight="bold">
        Tr(I_s) = {traceVal}
      </text>
      <text x={cx} y={cy} textAnchor="middle" fill={COLORS.text}
        fontSize="11" fontFamily="'JetBrains Mono', monospace">
        1 + ({signature})·{K} + {K * K} = {traceVal}
      </text>
      <text x={cx} y={cy + 22} textAnchor="middle" fill={COLORS.textDim}
        fontSize="10" fontFamily="'JetBrains Mono', monospace">
        det(α^I) = α^{traceVal}
      </text>
      {showBBP && (
        <text x={cx} y={cy + 45} textAnchor="middle" fill={COLORS.gold}
          fontSize="11" fontFamily="'JetBrains Mono', monospace">
          π ≈ {bbpPartial(Math.floor(step / 4) + 1).toFixed(10)}
        </text>
      )}
    </svg>
  );
}

function GEquation({ signature }) {
  const f21 = fPoly(1), f17 = fPoly(0), f13 = fPoly(-1);
  const Gtree = (f17 / f13) * Math.pow(ALPHA, f21) * 3.809946e34;
  const schwinger = ALPHA / (2 * Math.PI);
  const G1loop = Gtree * (1 + schwinger);
  const Gmeas = 6.67430e-11;

  const s = signature;
  const traceVal = fPoly(s);
  const labels = { 1: "TetA (s=+1)", 0: "Origin (s=0)", "-1": "TetB (s=−1)" };

  return (
    <div style={{
      background: COLORS.bgCard, borderRadius: 12, padding: "20px 24px",
      border: `1px solid ${COLORS.textMuted}`,
    }}>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.textDim, marginBottom: 12, textTransform: "uppercase", letterSpacing: 2 }}>
        Newton's Constant from the Matrix
      </div>
      
      <div style={{ fontFamily: "'Crimson Pro', Georgia, serif", fontSize: 20, color: COLORS.text, marginBottom: 16, lineHeight: 1.6 }}>
        <span style={{ color: COLORS.gold }}>G</span> = [Tr<sub>s=0</sub> / Tr<sub>s=−1</sub>] × det(α<sup>I<sub>s=+1</sub></sup>) × ℏc/m<sub>e</sub>²
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginBottom: 16 }}>
        {[1, 0, -1].map(sv => {
          const tv = fPoly(sv);
          const label = sv === 1 ? "TetA" : sv === 0 ? "Origin" : "TetB";
          const role = sv === 1 ? "Exponent" : sv === 0 ? "Numerator" : "Denominator";
          const isActive = sv === signature;
          return (
            <div key={sv} style={{
              background: isActive ? COLORS.bgCardHover : "transparent",
              border: `1px solid ${isActive ? COLORS.gold : COLORS.textMuted}`,
              borderRadius: 8, padding: "10px 12px", textAlign: "center",
              transition: "all 0.2s",
            }}>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim, marginBottom: 4 }}>{label} (s={sv >= 0 ? "+" : ""}{sv})</div>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 24, color: isActive ? COLORS.gold : COLORS.text, fontWeight: "bold" }}>{tv}</div>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim, marginTop: 4 }}>
                det(α^I) = α<sup>{tv}</sup>
              </div>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim, marginTop: 2 }}>{role}</div>
            </div>
          );
        })}
      </div>

      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: COLORS.text, lineHeight: 1.8 }}>
        <div>G<sub>tree</sub> = ({f17}/{f13}) × α<sup>{f21}</sup> × ℏc/m<sub>e</sub>² = <span style={{ color: COLORS.gold }}>{Gtree.toExponential(4)}</span></div>
        <div>G<sub>1-loop</sub> = G<sub>tree</sub> × (1 + α/2π) = <span style={{ color: COLORS.active }}>{G1loop.toExponential(4)}</span></div>
        <div>G<sub>measured</sub> = <span style={{ color: COLORS.text }}>{Gmeas.toExponential(4)}</span></div>
        <div style={{ color: COLORS.active, marginTop: 4 }}>
          Residual: {((G1loop - Gmeas) / Gmeas * 100).toFixed(4)}%
        </div>
      </div>
    </div>
  );
}

function BBPPanel({ step, running }) {
  const rotation = Math.floor(step / N_SECTORS);
  const position = step % N_SECTORS;
  const piValue = bbpPartial(Math.floor(step / 4) + 1);
  const piError = Math.abs(piValue - Math.PI);
  const { face, channel, subchannel } = sectorHierarchy(position);
  const weightIdx = step % 4;
  const weight = BBP_WEIGHTS[weightIdx];
  const offset = BBP_OFFSETS[weightIdx];

  return (
    <div style={{
      background: COLORS.bgCard, borderRadius: 12, padding: "20px 24px",
      border: `1px solid ${COLORS.textMuted}`,
    }}>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.textDim, marginBottom: 12, textTransform: "uppercase", letterSpacing: 2 }}>
        BBP Walk — Base {BBP_BASE} Closure
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 16 }}>
        <div style={{ background: COLORS.bg, borderRadius: 8, padding: 12 }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim }}>Step</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 22, color: COLORS.gold }}>{step}</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim }}>
            Rotation {rotation + 1}, sector {position}
          </div>
        </div>
        <div style={{ background: COLORS.bg, borderRadius: 8, padding: 12 }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim }}>π accumulation</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, color: COLORS.active }}>{piValue.toFixed(12)}</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim }}>
            error: {piError.toExponential(3)}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 8, marginBottom: 12 }}>
        <div style={{ background: COLORS.bg, borderRadius: 6, padding: 8, textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Face</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, color: FACE_COLORS[face] }}>{face}</div>
        </div>
        <div style={{ background: COLORS.bg, borderRadius: 6, padding: 8, textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Channel</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, color: COLORS.text }}>{channel}</div>
        </div>
        <div style={{ background: COLORS.bg, borderRadius: 6, padding: 8, textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Sub-ch</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, color: COLORS.text }}>{subchannel}</div>
        </div>
        <div style={{ background: COLORS.bg, borderRadius: 6, padding: 8, textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Weight</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, color: weight > 0 ? COLORS.active : COLORS.inverted }}>
            {weight > 0 ? "+" : ""}{weight}
          </div>
        </div>
      </div>

      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim, lineHeight: 1.6 }}>
        Weights: [{BBP_WEIGHTS.map((w, i) => (
          <span key={i} style={{ color: i === weightIdx ? COLORS.gold : COLORS.textDim, fontWeight: i === weightIdx ? "bold" : "normal" }}>
            {w > 0 ? "+" : ""}{w}{i < 3 ? ", " : ""}
          </span>
        ))}] = [+K, −2, −D, −D]<br/>
        Offsets: [{BBP_OFFSETS.map((o, i) => (
          <span key={i} style={{ color: i === weightIdx ? COLORS.gold : COLORS.textDim }}>
            {o}{i < 3 ? ", " : ""}
          </span>
        ))}] = [1, K, K+1, K+2]<br/>
        Σ weights = −K = −{K} &nbsp;|&nbsp; Σ offsets = K² = {K * K}
      </div>
    </div>
  );
}

function SectorInfo({ sectorIdx }) {
  if (sectorIdx === null) return (
    <div style={{
      background: COLORS.bgCard, borderRadius: 12, padding: "20px 24px",
      border: `1px solid ${COLORS.textMuted}`, minHeight: 100,
    }}>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.textDim, textTransform: "uppercase", letterSpacing: 2, marginBottom: 8 }}>
        Sector Detail
      </div>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: COLORS.textDim }}>
        Hover over a sector to inspect
      </div>
    </div>
  );

  const { face, channel, subchannel } = sectorHierarchy(sectorIdx);
  const I = face, J = channel, KK = subchannel;
  const nDistinct = new Set([I, J, KK]).size;
  const type = nDistinct === 1 ? "Diagonal (self-coupling)" : nDistinct === 2 ? "Face coupling" : "Permutation (torsion)";

  return (
    <div style={{
      background: COLORS.bgCard, borderRadius: 12, padding: "20px 24px",
      border: `1px solid ${FACE_COLORS[face]}40`,
    }}>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.textDim, textTransform: "uppercase", letterSpacing: 2, marginBottom: 8 }}>
        Sector {sectorIdx} — Γ<sup>{I}</sup><sub>{J}{KK}</sub>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: 12 }}>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Output I</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 20, color: FACE_COLORS[I] }}>{I}</div>
        </div>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Input J</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 20, color: FACE_COLORS[J] }}>{J}</div>
        </div>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>Direction K</div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 20, color: FACE_COLORS[KK] }}>{KK}</div>
        </div>
      </div>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.text }}>
        {type} — {nDistinct === 3 ? "S₄ torsion (GR deletes this)" : nDistinct === 1 ? "Self-interaction" : "Christoffel"}
      </div>
    </div>
  );
}

function HarmonicBreakdown({ signature }) {
  const band0 = 1;
  const band1 = signature * K;
  const band2 = K * K;
  const total = band0 + band1 + band2;

  return (
    <div style={{
      background: COLORS.bgCard, borderRadius: 12, padding: "20px 24px",
      border: `1px solid ${COLORS.textMuted}`,
    }}>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.textDim, marginBottom: 12, textTransform: "uppercase", letterSpacing: 2 }}>
        Three Harmonic Bands — f(K, s={signature >= 0 ? "+" : ""}{signature})
      </div>

      {[
        { label: "Band 0 — Fundamental", dim: 1, val: band0, color: COLORS.band0, desc: "Face identity (1 harmonic)" },
        { label: "Band 1 — First Overtone", dim: K, val: band1, color: signature === 0 ? COLORS.silent : signature === -1 ? COLORS.inverted : COLORS.band1, desc: `Channel structure (${K} harmonics × s)` },
        { label: "Band 2 — Second Overtone", dim: K * K, val: band2, color: COLORS.band2, desc: `Sub-channel boundary (${K * K} harmonics)` },
      ].map((b, i) => (
        <div key={i} style={{
          display: "flex", alignItems: "center", gap: 12, marginBottom: 10,
          padding: "8px 12px", background: COLORS.bg, borderRadius: 8,
          borderLeft: `3px solid ${b.color}`,
        }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: COLORS.text }}>{b.label}</div>
            <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: COLORS.textDim }}>{b.desc}</div>
          </div>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 20, color: b.color, fontWeight: "bold", minWidth: 40, textAlign: "right" }}>
            {b.val > 0 ? "+" : ""}{b.val}
          </div>
        </div>
      ))}

      <div style={{
        display: "flex", justifyContent: "space-between", alignItems: "center",
        marginTop: 12, padding: "10px 16px", background: COLORS.bg, borderRadius: 8,
        border: `1px solid ${COLORS.gold}40`,
      }}>
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: COLORS.textDim }}>
          Tr(I<sub>s</sub>) = {band0} + ({band1}) + {band2}
        </span>
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 24, color: COLORS.gold, fontWeight: "bold" }}>
          = {total}
        </span>
      </div>
    </div>
  );
}

export default function App() {
  const [signature, setSignature] = useState(1);
  const [step, setStep] = useState(0);
  const [running, setRunning] = useState(false);
  const [showBBP, setShowBBP] = useState(false);
  const [showBands, setShowBands] = useState(true);
  const [hoveredSector, setHoveredSector] = useState(null);
  const [speed, setSpeed] = useState(80);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (running && showBBP) {
      intervalRef.current = setInterval(() => {
        setStep(s => s + 1);
      }, speed);
    } else {
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [running, showBBP, speed]);

  const toggleBBP = useCallback(() => {
    if (!showBBP) {
      setShowBBP(true);
      setStep(0);
      setRunning(true);
    } else {
      setRunning(!running);
    }
  }, [showBBP, running]);

  const resetBBP = useCallback(() => {
    setStep(0);
    setRunning(false);
  }, []);

  const btnStyle = (active) => ({
    padding: "8px 16px",
    borderRadius: 6,
    border: `1px solid ${active ? COLORS.gold : COLORS.textMuted}`,
    background: active ? COLORS.gold + "20" : "transparent",
    color: active ? COLORS.gold : COLORS.textDim,
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 11,
    cursor: "pointer",
    transition: "all 0.15s",
  });

  return (
    <div style={{
      minHeight: "100vh",
      background: COLORS.bg,
      color: COLORS.text,
      fontFamily: "'JetBrains Mono', monospace",
    }}>
      {/* Header */}
      <div style={{ padding: "24px 32px", borderBottom: `1px solid ${COLORS.textMuted}` }}>
        <div style={{ fontSize: 9, color: COLORS.textDim, textTransform: "uppercase", letterSpacing: 3, marginBottom: 4 }}>
          Field Dynamics Research
        </div>
        <h1 style={{ fontSize: 22, fontWeight: 600, color: COLORS.text, margin: 0, fontFamily: "'Crimson Pro', Georgia, serif" }}>
          The 64-Sector Photonic Circle
        </h1>
        <div style={{ fontSize: 11, color: COLORS.textDim, marginTop: 4 }}>
          K<sup>D</sup> = 64 photonic states · 3 harmonic bands · BBP closure walk · G = (17/13) × α<sup>21</sup> × ℏc/m<sub>e</sub>²
        </div>
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 24, padding: 24 }}>
        {/* Left: Circle */}
        <div style={{ flex: "1 1 580px", minWidth: 340 }}>
          <CircleSVG
            step={step}
            signature={signature}
            showBBP={showBBP}
            showBands={showBands}
            hoveredSector={hoveredSector}
            setHoveredSector={setHoveredSector}
          />

          {/* Controls */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12, justifyContent: "center" }}>
            <div style={{ display: "flex", gap: 4, background: COLORS.bgCard, borderRadius: 8, padding: 4 }}>
              {[1, 0, -1].map(s => (
                <button key={s} onClick={() => setSignature(s)} style={btnStyle(signature === s)}>
                  s={s >= 0 ? "+" : ""}{s}
                </button>
              ))}
            </div>
            <button onClick={() => setShowBands(!showBands)} style={btnStyle(showBands)}>
              {showBands ? "Hide" : "Show"} Bands
            </button>
            <button onClick={toggleBBP} style={btnStyle(showBBP && running)}>
              {!showBBP ? "Start BBP Walk" : running ? "Pause" : "Resume"}
            </button>
            {showBBP && (
              <button onClick={resetBBP} style={btnStyle(false)}>Reset</button>
            )}
            {showBBP && (
              <select value={speed} onChange={e => setSpeed(Number(e.target.value))}
                style={{ ...btnStyle(false), appearance: "auto" }}>
                <option value={200}>Slow</option>
                <option value={80}>Normal</option>
                <option value={30}>Fast</option>
                <option value={5}>Warp</option>
              </select>
            )}
          </div>
        </div>

        {/* Right: Panels */}
        <div style={{ flex: "1 1 340px", display: "flex", flexDirection: "column", gap: 16, minWidth: 300 }}>
          <HarmonicBreakdown signature={signature} />
          <GEquation signature={signature} />
          {showBBP && <BBPPanel step={step} running={running} />}
          <SectorInfo sectorIdx={hoveredSector} />
        </div>
      </div>

      {/* Footer identity */}
      <div style={{
        padding: "16px 32px",
        borderTop: `1px solid ${COLORS.textMuted}`,
        display: "flex", flexWrap: "wrap", justifyContent: "space-between",
        fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: COLORS.textDim,
      }}>
        <span>64 = 21 × 3 + 1 · One circle · Three bands · G is algebra</span>
        <span>K = 4 · D = 3 · f(K,s) = 1 + sK + K²</span>
      </div>
    </div>
  );
}
