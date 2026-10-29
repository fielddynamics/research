using System;
using System.Collections.Generic;
using System.Linq;

namespace OctahedralResonance
{
    /// <summary>
    /// Octahedral Resonance Compute Node
    /// 
    /// Architecture: 24 (TetA) + 16 (Shared Vertex) + 24 (TetB) = 64 parameters
    /// 
    /// Three subcycles per oscillation:
    ///   1. Forward  (TetA + Shared): observer projects through vertex
    ///   2. Backward (TetB + Shared): witness receives through vertex  
    ///   3. Reconciliation (all 64): forward and backward meet, delta updates shared
    /// 
    /// The shared 16 vertex parameters are the MEMORY.
    /// They accumulate what both passes agree on.
    /// </summary>
    public class OctahedralNode
    {
        public int Id;
        public const int N = 8;

        // ============================================================
        // TOPOLOGY (fixed)
        // ============================================================

        public static readonly int[,] Signs = {
            {+1,+1,+1}, {+1,+1,-1}, {+1,-1,+1}, {+1,-1,-1},
            {-1,+1,+1}, {-1,+1,-1}, {-1,-1,+1}, {-1,-1,-1}
        };
        public static readonly int[] Parity = {+1,-1,-1,+1,-1,+1,+1,-1};
        public static readonly int[] TetAIdx = {0,3,5,6};
        public static readonly int[] TetBIdx = {1,2,4,7};

        public static readonly double[,] H = BuildH();
        static double[,] BuildH() {
            var h = new double[8,8];
            for (int k=0; k<8; k++) {
                int sx=Signs[k,0], sy=Signs[k,1], sz=Signs[k,2];
                h[k,0]=1; h[k,1]=sx; h[k,2]=sy; h[k,3]=sz;
                h[k,4]=sx*sy; h[k,5]=sx*sz; h[k,6]=sy*sz; h[k,7]=sx*sy*sz;
            }
            return h;
        }

        // ============================================================
        // LEARNABLE PARAMETERS: 24 + 16 + 24 = 64
        // ============================================================

        // TetA chamber: 8 × 3 = 24
        public double[] AmpA, FreqA, PhaseA;

        // TetB chamber: 8 × 3 = 24
        public double[] AmpB, FreqB, PhaseB;

        // Shared vertex: 8 inward couplings + 8 outward couplings = 16
        // CouplingIn:  how strongly each channel drives INTO the vertex mix
        // CouplingOut: how strongly the vertex mix feeds BACK to each channel
        public double[] CouplingIn;
        public double[] CouplingOut;

        // ============================================================
        // STATE
        // ============================================================

        public double[] WaveA;          // TetA wave evaluation [8]
        public double[] WaveB;          // TetB wave evaluation [8]
        public double[] ForwardMix;     // subcycle 1 output: TetA through vertex [8]
        public double[] BackwardMix;    // subcycle 2 output: TetB through vertex [8]
        public double[] Vertex;         // subcycle 3 output: reconciled state [8]
        public double[] Coeffs;         // Hadamard decomposition of Vertex [8]
        public double[] Input;          // external input buffer [8]
        public double[] Output;         // final output to neighbors [8]

        // Scalar readouts
        public double Omega;            // parity coefficient (grade 3)
        public double Mu;               // Born rule activation
        public double MuPrev;           // previous cycle
        public double Entropy;          // binary entropy
        public double EnergyA, EnergyB; // per-sector energy
        public double Delta;            // forward - backward disagreement

        // Time
        public double Time;
        public int Cycle;

        // ============================================================
        // HYPERPARAMETERS
        // ============================================================

        public double ClosureRate = 0.02;   // how fast shared params update
        public double Dt = 0.1;             // time step per cycle
        public double VertexGain = 0.2;     // nonlinear mixing strength
        public double Damping = 0.9;        // energy retention per cycle (1.0 = no damping)

        // ============================================================
        // CONNECTIONS
        // ============================================================

        public List<Connection> Connections = new List<Connection>();
        public List<PairConnection> PairLinks = new List<PairConnection>();

        // ============================================================
        // CONSTRUCTOR
        // ============================================================

        public OctahedralNode(int id, bool randomInit = false)
        {
            Id = id; Time = 0; Cycle = 0; Mu = 0.5; MuPrev = 0.5;

            AmpA = new double[N]; FreqA = new double[N]; PhaseA = new double[N];
            AmpB = new double[N]; FreqB = new double[N]; PhaseB = new double[N];
            CouplingIn = new double[N];
            CouplingOut = new double[N];

            WaveA = new double[N]; WaveB = new double[N];
            ForwardMix = new double[N]; BackwardMix = new double[N];
            Vertex = new double[N]; Coeffs = new double[N];
            Input = new double[N]; Output = new double[N];

            var rng = new Random(id * 37 + 13);

            for (int k = 0; k < N; k++)
            {
                if (randomInit)
                {
                    AmpA[k] = 0.5 + rng.NextDouble();
                    AmpB[k] = 0.5 + rng.NextDouble();
                    FreqA[k] = 0.8 + 0.4 * rng.NextDouble();
                    FreqB[k] = 0.8 + 0.4 * rng.NextDouble();
                    PhaseA[k] = 2 * Math.PI * rng.NextDouble();
                    PhaseB[k] = 2 * Math.PI * rng.NextDouble();
                    CouplingIn[k] = 0.8 + 0.4 * rng.NextDouble();
                    CouplingOut[k] = 0.8 + 0.4 * rng.NextDouble();
                }
                else
                {
                    AmpA[k] = 0.0;
                    AmpB[k] = 0.0;
                    FreqA[k] = 1.0 + 0.01 * k;
                    FreqB[k] = 1.0 + 0.01 * (N - 1 - k);
                    PhaseA[k] = 2 * Math.PI * k / N;
                    PhaseB[k] = 2 * Math.PI * (k + 4) / N;
                    CouplingIn[k] = 1.0;
                    CouplingOut[k] = 1.0;
                }
            }
        }

        // ============================================================
        // CORE: ONE OSCILLATION = THREE SUBCYCLES
        // ============================================================

        public void Tick()
        {
            MuPrev = Mu;

            // ==========================================================
            // SUBCYCLE 1: FORWARD (TetA + Shared = 24 + 16 = 40)
            // The observer projects through the vertex.
            // This is what GR computes.
            // ==========================================================

            // TetA evaluates its 8 waves
            for (int k = 0; k < N; k++)
                WaveA[k] = AmpA[k] * Math.Sin(FreqA[k] * Time + PhaseA[k]);

            // Add external input
            for (int k = 0; k < N; k++)
                WaveA[k] += Input[k];

            // Forward vertex mixing: CouplingIn modulates what enters the vertex
            // Nonlinear: pairwise products weighted by sign overlap and CouplingIn
            for (int k = 0; k < N; k++)
            {
                double linear = CouplingIn[k] * WaveA[k];
                double cross = 0;
                for (int j = 0; j < N; j++)
                {
                    if (j != k)
                    {
                        int overlap = Signs[k,0]*Signs[j,0]
                                    + Signs[k,1]*Signs[j,1]
                                    + Signs[k,2]*Signs[j,2];
                        cross += overlap * CouplingIn[k] * WaveA[k]
                                         * CouplingIn[j] * WaveA[j];
                    }
                }
                ForwardMix[k] = linear + VertexGain * cross / (N - 1);
                if (Double.IsNaN(ForwardMix[k]) || Double.IsInfinity(ForwardMix[k]))
                    ForwardMix[k] = linear;
                ForwardMix[k] = Clamp(ForwardMix[k], -50, 50);
            }

            // ==========================================================
            // SUBCYCLE 2: BACKWARD (TetB + Shared = 24 + 16 = 40)
            // The witness receives through the vertex.
            // This is what GR discards.
            // ==========================================================

            // TetB evaluates its 8 waves
            for (int k = 0; k < N; k++)
                WaveB[k] = AmpB[k] * Math.Sin(FreqB[k] * Time + PhaseB[k]);

            // TetB receives the forward mix through CouplingOut
            for (int k = 0; k < N; k++)
                WaveB[k] += CouplingOut[k] * ForwardMix[k];

            // Backward vertex mixing: same nonlinearity, opposite direction
            for (int k = 0; k < N; k++)
            {
                double linear = CouplingIn[k] * WaveB[k];
                double cross = 0;
                for (int j = 0; j < N; j++)
                {
                    if (j != k)
                    {
                        int overlap = Signs[k,0]*Signs[j,0]
                                    + Signs[k,1]*Signs[j,1]
                                    + Signs[k,2]*Signs[j,2];
                        cross += overlap * CouplingIn[k] * WaveB[k]
                                         * CouplingIn[j] * WaveB[j];
                    }
                }
                BackwardMix[k] = linear + VertexGain * cross / (N - 1);
                if (Double.IsNaN(BackwardMix[k]) || Double.IsInfinity(BackwardMix[k]))
                    BackwardMix[k] = linear;
                BackwardMix[k] = Clamp(BackwardMix[k], -50, 50);
            }

            // ==========================================================
            // SUBCYCLE 3: RECONCILIATION (all 64)
            // Forward and backward meet. The delta updates the shared.
            // The full 64-component state is resolved.
            // ==========================================================

            // Compute per-sector energies
            EnergyA = 0; EnergyB = 0;
            for (int k = 0; k < N; k++)
            {
                EnergyA += ForwardMix[k] * ForwardMix[k];
                EnergyB += BackwardMix[k] * BackwardMix[k];
            }
            Delta = EnergyA - EnergyB;

            // The reconciled vertex state: superposition of forward and backward
            // weighted by CouplingOut (the shared outward parameters)
            for (int k = 0; k < N; k++)
            {
                Vertex[k] = CouplingOut[k] * (ForwardMix[k] + BackwardMix[k]) / 2.0;
            }

            // Hadamard decomposition of the reconciled state
            for (int c = 0; c < N; c++)
            {
                double s = 0;
                for (int k = 0; k < N; k++)
                    s += H[k, c] * Vertex[k];
                Coeffs[c] = s / N;
            }

            // Activation
            Omega = Coeffs[7];
            double c0 = Coeffs[0];
            Mu = (Math.Abs(c0) > 1e-12)
                ? Clamp((1.0 + Omega / c0) / 2.0, 0, 1)
                : 0.5;
            Entropy = (Mu > 1e-12 && Mu < 1 - 1e-12)
                ? -Mu * Math.Log(Mu) - (1 - Mu) * Math.Log(1 - Mu)
                : 0;

            // --- Self-training: update shared parameters from the delta ---

            // The shared coupling weights learn from the disagreement
            // between forward and backward passes.
            // If forward and backward agree on a channel → strengthen coupling
            // If they disagree → weaken coupling (or adjust)
            for (int k = 0; k < N; k++)
            {
                // Agreement signal: positive if same sign, negative if opposite
                double fwd = ForwardMix[k], bwd = BackwardMix[k];
                if (Double.IsNaN(fwd) || Double.IsNaN(bwd)) continue;
                
                double agreement = fwd * bwd;
                agreement = Clamp(agreement, -10, 10);

                // Inward coupling: adjust toward what produces agreement
                CouplingIn[k] += ClosureRate * Math.Sign(agreement)
                                 * (1.0 - Math.Abs(CouplingIn[k]));
                CouplingIn[k] = Clamp(CouplingIn[k], 0.01, 5.0);

                // Outward coupling: adjust toward balanced output
                double targetOut = Math.Sqrt(Math.Max(
                    (EnergyA + EnergyB) / (2 * N), 1e-12));
                targetOut = Math.Min(targetOut, 5.0);
                CouplingOut[k] += ClosureRate * (targetOut - CouplingOut[k]);
                CouplingOut[k] = Clamp(CouplingOut[k], 0.01, 5.0);
            }

            // Closure relaxation on chamber amplitudes
            double meanE = (EnergyA + EnergyB) / (2 * N);
            double targetAmp = Math.Sqrt(Math.Max(meanE, 1e-12));
            targetAmp = Math.Min(targetAmp, 5.0);
            for (int k = 0; k < N; k++)
            {
                AmpA[k] += ClosureRate * (targetAmp - AmpA[k]);
                AmpB[k] += ClosureRate * (targetAmp - AmpB[k]);
                AmpA[k] = Clamp(AmpA[k], 0.01, 5.0);
                AmpB[k] = Clamp(AmpB[k], 0.01, 5.0);
            }

            // Output = reconciled vertex state (raw, full spectrum)
            Array.Copy(Vertex, Output, N);

            // Clear input
            Array.Clear(Input, 0, N);

            Time += Dt;
            Cycle++;
        }

        // ============================================================
        // DATA INTERFACE
        // ============================================================

        public void Inject(double[] data)
        {
            for (int k = 0; k < N; k++)
            {
                double proj = 0;
                for (int d = 0; d < Math.Min(data.Length, 3); d++)
                    proj += data[d] * Signs[k, d];
                Input[k] += proj;
            }
        }

        public void Gather()
        {
            foreach (var c in Connections)
                for (int k = 0; k < N; k++)
                    Input[k] += c.Strength * c.Target.Output[k];
        }

        public double Stability { get { return Math.Abs(Mu - MuPrev); } }
        public bool Converged(double thr = 0.01) { return Entropy < thr; }

        static double Clamp(double v, double lo, double hi)
        { return Math.Max(lo, Math.Min(hi, v)); }

        public int ParamCount { get { return 24 + 16 + 24; } }

        public override string ToString()
        {
            return string.Format(
                "Node[{0}] mu={1:F4} w={2:F4} H={3:F4} d={4:F4} EA={5:F2} EB={6:F2}",
                Id, Mu, Omega, Entropy, Delta, EnergyA, EnergyB);
        }
    }

    public class Connection
    {
        public OctahedralNode Target;
        public double Strength;
        public Connection(OctahedralNode t, double s = 1.0)
        { Target = t; Strength = s; }
    }

    // ================================================================
    // OCTAHEDRAL LATTICE
    // ================================================================
    //
    // A rectangular lattice of OctahedralNodes wired via the 4 parity
    // pair axes.  No layers — just a wave propagation medium.
    //
    //  Pair 0 (ch 0,7): LEFT  ↔ RIGHT  (width axis)
    //  Pair 1 (ch 1,6): LEFT  ↔ RIGHT  (alternate width axis)
    //  Pair 2 (ch 2,5): UP    ↔ DOWN   (height axis)
    //  Pair 3 (ch 3,4): UP    ↔ DOWN   (alternate height axis)
    //
    //  Left edge  = input face.   Open pairs receive injected data.
    //  Right edge = output face.  Read μ from these nodes.
    //  Top/bottom edges: boundary condition = 1.0 where no neighbor.
    //

    public class OctahedralLattice
    {
        public int Width { get; }
        public int Height { get; }
        public OctahedralNode[,] Grid { get; }
        public int TotalNodes { get { return Width * Height; } }
        public int TotalParams { get { return TotalNodes * 64; } }
        public int TickCount { get; private set; }

        // Parity pair definitions:
        // Each pair = (channelA, channelB) = one axis through the octahedron
        // Pair 0: channels (0,7) — axis 0 — used for RIGHT neighbor
        // Pair 1: channels (1,6) — axis 1 — used for LEFT neighbor
        // Pair 2: channels (2,5) — axis 2 — used for DOWN neighbor
        // Pair 3: channels (3,4) — axis 3 — used for UP neighbor
        //
        // When a neighbor exists: its output feeds through the pair.
        // When no neighbor (edge): pair receives boundary condition.

        static readonly int[,] PairChannels = {
            {0, 7},  // pair 0: right
            {1, 6},  // pair 1: left
            {2, 5},  // pair 2: down
            {3, 4},  // pair 3: up
        };

        // Direction offsets: right, left, down, up
        static readonly int[,] Dirs = {
            {+1,  0},  // pair 0 → right neighbor
            {-1,  0},  // pair 1 → left neighbor
            { 0, +1},  // pair 2 → down neighbor
            { 0, -1},  // pair 3 → up neighbor
        };

        public double BoundaryValue = 0.0;
        public double DefaultGain = 0.8;
        public double DefaultDamping = 0.5;

        // ============================================================
        // CONSTRUCTOR
        // ============================================================

        public OctahedralLattice(int width, int height)
        {
            Width = width;
            Height = height;
            Grid = new OctahedralNode[width, height];
            TickCount = 0;

            // Create all nodes
            for (int x = 0; x < width; x++)
                for (int y = 0; y < height; y++)
                {
                    int id = x * height + y;
                    Grid[x, y] = new OctahedralNode(id);
                    Grid[x, y].VertexGain = DefaultGain;
                    Grid[x, y].Damping = DefaultDamping;
                }

            // Wire the lattice
            WireLattice();
        }

        private void WireLattice()
        {
            for (int x = 0; x < Width; x++)
            {
                for (int y = 0; y < Height; y++)
                {
                    var node = Grid[x, y];

                    // For each of the 4 parity pair axes
                    for (int p = 0; p < 4; p++)
                    {
                        int nx = x + Dirs[p, 0];
                        int ny = y + Dirs[p, 1];

                        // WRAP vertical axis (top ↔ bottom)
                        // This closes the standing wave loop vertically.
                        // Every node gets its up/down neighbors.
                        ny = ((ny % Height) + Height) % Height;

                        // Horizontal axis: left/right stay open
                        // Left edge = input face, right edge = output face
                        if (nx >= 0 && nx < Width)
                        {
                            var neighbor = Grid[nx, ny];
                            var conn = new PairConnection(neighbor, p);
                            node.PairLinks.Add(conn);
                        }
                        // else: left/right boundary — open for input/output
                    }
                }
            }
        }

        // ============================================================
        // TICK: ONE LATTICE-WIDE OSCILLATION
        // ============================================================

        public void Tick()
        {
            // Phase 1: Gather inputs from neighbors — full 8-channel coupling
            // Signal passes through constitutive law μ(x) = x/(x+1) at the boundary.
            // This is the natural impedance of the octahedral lattice.
            for (int x = 0; x < Width; x++)
            {
                for (int y = 0; y < Height; y++)
                {
                    var node = Grid[x, y];

                    foreach (var link in node.PairLinks)
                    {
                        for (int k = 0; k < OctahedralNode.N; k++)
                        {
                            double raw = link.Strength * link.Target.Output[k];
                            // Constitutive law: sign(v) * |v| / (|v| + 1)
                            double absv = Math.Abs(raw);
                            double saturated = Math.Sign(raw) * absv / (absv + 1.0);
                            node.Input[k] += saturated;
                        }
                    }
                }
            }

            // Phase 2: All nodes tick
            for (int x = 0; x < Width; x++)
                for (int y = 0; y < Height; y++)
                    Grid[x, y].Tick();

            TickCount++;
        }

        // Pair 0 ↔ Pair 1  (right ↔ left)
        // Pair 2 ↔ Pair 3  (down ↔ up)
        static int OppositePair(int p)
        {
            switch (p) {
                case 0: return 1;
                case 1: return 0;
                case 2: return 3;
                case 3: return 2;
                default: return p;
            }
        }

        // ============================================================
        // DATA INTERFACE
        // ============================================================

        /// <summary>
        /// Inject data into a left-edge node (column 0).
        /// row = which row (0 to Height-1).
        /// data = up to 3 values mapped to x, y, z.
        /// </summary>
        public void SetInput(int row, double[] data)
        {
            if (row >= 0 && row < Height)
                Grid[0, row].Inject(data);
        }

        /// <summary>
        /// Inject data into all left-edge rows.
        /// features is a flat array; every 3 values go to one row.
        /// </summary>
        public void SetInputs(double[] features)
        {
            int row = 0;
            for (int i = 0; i < features.Length && row < Height; i += 3)
            {
                int len = Math.Min(3, features.Length - i);
                double[] chunk = new double[len];
                Array.Copy(features, i, chunk, 0, len);
                SetInput(row, chunk);
                row++;
            }
        }

        /// <summary>
        /// Read μ activations from right-edge nodes (column Width-1).
        /// </summary>
        public double[] ReadOutputs()
        {
            double[] results = new double[Height];
            for (int y = 0; y < Height; y++)
                results[y] = Grid[Width - 1, y].Mu;
            return results;
        }

        /// <summary>
        /// Read full Hadamard coefficients from right-edge nodes.
        /// </summary>
        public double[,] ReadSpectra()
        {
            var spectra = new double[Height, OctahedralNode.N];
            for (int y = 0; y < Height; y++)
                for (int c = 0; c < OctahedralNode.N; c++)
                    spectra[y, c] = Grid[Width - 1, y].Coeffs[c];
            return spectra;
        }

        /// <summary>
        /// Run for N ticks.
        /// </summary>
        public void Run(int ticks)
        {
            for (int i = 0; i < ticks; i++)
                Tick();
        }

        /// <summary>
        /// Run until converged or max ticks reached.
        /// </summary>
        public int RunUntilConverged(int maxTicks = 1000, double threshold = 0.05)
        {
            for (int i = 0; i < maxTicks; i++)
            {
                Tick();
                if (MeanEntropy() < threshold)
                    return i + 1;
            }
            return maxTicks;
        }

        // ============================================================
        // MONITORING
        // ============================================================

        public double MeanEntropy()
        {
            double sum = 0;
            for (int x = 0; x < Width; x++)
                for (int y = 0; y < Height; y++)
                    sum += Grid[x, y].Entropy;
            return sum / TotalNodes;
        }

        public double MaxStability()
        {
            double max = 0;
            for (int x = 0; x < Width; x++)
                for (int y = 0; y < Height; y++)
                    max = Math.Max(max, Grid[x, y].Stability);
            return max;
        }

        public OctahedralNode InputNode(int row) { return Grid[0, row]; }
        public OctahedralNode OutputNode(int row) { return Grid[Width - 1, row]; }

        public void PrintStatus()
        {
            Console.WriteLine("  Lattice {0}x{1} = {2} nodes, {3} params, tick {4}",
                Width, Height, TotalNodes, TotalParams, TickCount);
            Console.WriteLine("  Mean entropy: {0:F4}  Max stability: {1:F6}",
                MeanEntropy(), MaxStability());
        }
    }

    /// <summary>
    /// A parity-pair connection: links one node to a neighbor
    /// through a specific pair of opposite channels.
    /// </summary>
    public class PairConnection
    {
        public OctahedralNode Target;
        public int PairIndex;   // 0-3: which parity pair axis
        public double Strength;

        public PairConnection(OctahedralNode target, int pairIndex, double strength = 1.0)
        {
            Target = target;
            PairIndex = pairIndex;
            Strength = strength;
        }
    }

    // ================================================================
    // TEST SUITE
    // ================================================================

    class Program
    {
        static string F(double v) { return (v >= 0 ? "+" : "") + v.ToString("F4"); }

        static void Main(string[] args)
        {
            Console.WriteLine("==============================================");
            Console.WriteLine("  OCTAHEDRAL RESONANCE NODE v2 + LATTICE");
            Console.WriteLine("  64 parameters: 24 + 16 + 24");
            Console.WriteLine("  Lattice wiring: 2(D+1) = 2^D topology");
            Console.WriteLine("==============================================");
            Console.WriteLine();

            // Parameter count verification
            var testNode = new OctahedralNode(0);
            Console.WriteLine("  Parameters: {0}", testNode.ParamCount);
            Console.WriteLine("    TetA:   8 amp + 8 freq + 8 phase = 24");
            Console.WriteLine("    Vertex: 8 coupling_in + 8 coupling_out = 16");
            Console.WriteLine("    TetB:   8 amp + 8 freq + 8 phase = 24");
            Console.WriteLine("    Total:  24 + 16 + 24 = 64 = K^3");
            Console.WriteLine();

            string[] cnames = {"const","x","y","z","xy","xz","yz","xyz"};
            int[] grades = {0,1,1,1,2,2,2,3};

            // =========================================================
            // TEST 1: XOR — single tick
            // =========================================================
            Console.WriteLine("TEST 1: XOR (2-input, single tick)");
            Console.WriteLine("===================================");

            double[][] xor_in = {
                new double[]{-1,-1}, new double[]{-1,+1},
                new double[]{+1,-1}, new double[]{+1,+1}
            };
            double[] xor_exp = {-1, +1, +1, -1};

            int correct = 0;
            for (int i = 0; i < 4; i++)
            {
                var node = new OctahedralNode(0);
                node.Inject(xor_in[i]);
                node.Tick();
                double xy = node.Coeffs[4];
                double pred = -Math.Sign(xy);
                bool ok = (pred == xor_exp[i]);
                if (ok) correct++;
                Console.WriteLine("  ({0},{1}) xy={2} pred={3} {4}",
                    xor_in[i][0]>0?"+":"-", xor_in[i][1]>0?"+":"-",
                    F(xy), pred>0?"+1":"-1", ok?"PASS":"FAIL");
            }
            Console.WriteLine("  XOR: {0}/4", correct);
            Console.WriteLine();

            // =========================================================
            // TEST 2: 3-BIT PARITY — single tick
            // =========================================================
            Console.WriteLine("TEST 2: 3-bit parity (torsion readout, single tick)");
            Console.WriteLine("===================================================");

            double[][] p3_in = new double[8][];
            double[] p3_exp = new double[8];
            int idx = 0;
            for (int a=-1; a<=1; a+=2)
            for (int b=-1; b<=1; b+=2)
            for (int c=-1; c<=1; c+=2) {
                p3_in[idx] = new double[]{a,b,c};
                p3_exp[idx] = a*b*c;
                idx++;
            }

            correct = 0;
            for (int i = 0; i < 8; i++)
            {
                var node = new OctahedralNode(0);
                node.Inject(p3_in[i]);
                node.Tick();
                double xyz = node.Coeffs[7];
                double pred = Math.Sign(xyz);
                bool ok = (pred == p3_exp[i]);
                if (ok) correct++;
                Console.WriteLine("  ({0},{1},{2}) xyz={3} pred={4} exp={5} {6}",
                    p3_in[i][0]>0?"+":"-", p3_in[i][1]>0?"+":"-",
                    p3_in[i][2]>0?"+":"-", F(xyz),
                    pred>0?"+1":"-1", p3_exp[i]>0?"+1":"-1",
                    ok?"PASS":"FAIL");
            }
            Console.WriteLine("  3-bit parity: {0}/8", correct);
            Console.WriteLine();

            // =========================================================
            // TEST 3: 3-BIT PARITY — multiple cycles
            // =========================================================
            Console.WriteLine("TEST 3: 3-bit parity with standing wave (multi-cycle)");
            Console.WriteLine("=====================================================");

            int[] cycleCounts = {1, 5, 10, 25, 50, 100};
            foreach (int nc in cycleCounts)
            {
                correct = 0;
                for (int i = 0; i < 8; i++)
                {
                    var node = new OctahedralNode(0);
                    for (int c = 0; c < nc; c++) {
                        node.Inject(p3_in[i]);
                        node.Tick();
                    }
                    double xyz = node.Coeffs[7];
                    double pred = Math.Sign(xyz);
                    if (pred == p3_exp[i]) correct++;
                }
                Console.WriteLine("  {0,3} cycles: {1}/8 parity correct", nc, correct);
            }
            Console.WriteLine();

            // =========================================================
            // TEST 4: ALL 16 BOOLEAN (2-input) — single tick
            // =========================================================
            Console.WriteLine("TEST 4: All 16 boolean functions (2-input, single tick)");
            Console.WriteLine("======================================================");

            string[] fnames = {
                "FALSE","AND","A>B","A","B>A","B","XOR","OR",
                "NOR","XNOR","!B","A>=B","!A","B>=A","NAND","TRUE"
            };
            int[,] tt16 = {
                {-1,-1,-1,-1},{-1,-1,-1,+1},{-1,-1,+1,-1},{-1,-1,+1,+1},
                {-1,+1,-1,-1},{-1,+1,-1,+1},{-1,+1,+1,-1},{-1,+1,+1,+1},
                {+1,-1,-1,-1},{+1,-1,-1,+1},{+1,-1,+1,-1},{+1,-1,+1,+1},
                {+1,+1,-1,-1},{+1,+1,-1,+1},{+1,+1,+1,-1},{+1,+1,+1,+1}
            };

            double[,] H4 = {
                {1,-1,-1,+1},{1,-1,+1,-1},{1,+1,-1,-1},{1,+1,+1,+1}
            };

            int totalOk = 0;
            for (int f = 0; f < 16; f++)
            {
                double[] truth = new double[4];
                for (int j=0; j<4; j++) truth[j] = tt16[f,j];

                double[] hc = new double[4];
                for (int c=0; c<4; c++) {
                    double s=0;
                    for (int j=0; j<4; j++) s += H4[j,c]*truth[j];
                    hc[c] = s/4.0;
                }

                int fCorrect = 0;
                for (int j = 0; j < 4; j++)
                {
                    var node = new OctahedralNode(0);
                    node.Inject(xor_in[j]);
                    node.Tick();
                    double dec = hc[0]*node.Coeffs[0] + hc[1]*node.Coeffs[1]
                               + hc[2]*node.Coeffs[2] + hc[3]*node.Coeffs[4];
                    if (Math.Sign(dec) == truth[j]) fCorrect++;
                }
                totalOk += fCorrect;

                string needs = (hc[3]!=0) ? "nonlin" : (hc[1]!=0||hc[2]!=0) ? "linear" : "const ";
                Console.WriteLine("  {0,-5} [{1}]: {2}/4  h=({3:F1},{4:F1},{5:F1},{6:F1})",
                    fnames[f], needs, fCorrect, hc[0], hc[1], hc[2], hc[3]);
            }
            Console.WriteLine("  Total: {0}/64 ({1:F1}%)", totalOk, 100.0*totalOk/64);
            Console.WriteLine();

            // =========================================================
            // TEST 5: FULL ADDER
            // =========================================================
            Console.WriteLine("TEST 5: Full adder (sum + carry)");
            Console.WriteLine("================================");

            int sumOk = 0, carryOk = 0;
            Console.WriteLine("  A B C | S Co | xyz(sum)  | g1(carry) | S?  Co?");
            Console.WriteLine("  ------|------|-----------|-----------|--------");

            for (int i = 0; i < 8; i++)
            {
                var node = new OctahedralNode(0);
                node.Inject(p3_in[i]);
                node.Tick();

                double a=p3_in[i][0], b=p3_in[i][1], c=p3_in[i][2];
                int ai=(a>0)?1:0, bi=(b>0)?1:0, ci=(c>0)?1:0;
                int sumBit = (ai+bi+ci)%2;
                int carBit = (ai+bi+ci>=2)?1:0;
                double sumExp = sumBit==1?+1:-1;
                double carExp = carBit==1?+1:-1;

                double xyzC = node.Coeffs[7];
                double g1 = node.Coeffs[1]+node.Coeffs[2]+node.Coeffs[3];

                bool sOk = Math.Sign(xyzC)==sumExp;
                bool cOk = Math.Sign(g1)==carExp;
                if (sOk) sumOk++;
                if (cOk) carryOk++;

                Console.WriteLine("  {0} {1} {2} | {3} {4}  | {5,9} | {6,9} | {7}  {8}",
                    ai, bi, ci, sumBit, carBit,
                    F(xyzC), F(g1),
                    sOk?"ok":"XX", cOk?"ok":"XX");
            }
            Console.WriteLine("  Sum: {0}/8  Carry: {1}/8", sumOk, carryOk);
            Console.WriteLine();

            // =========================================================
            // TEST 6: Vertex gain sweep for 3-bit parity
            // =========================================================
            Console.WriteLine("TEST 6: Vertex gain sweep (3-bit parity, single tick)");
            Console.WriteLine("====================================================");
            Console.WriteLine("  gain   | parity | xor(xy)");
            Console.WriteLine("  -------|--------|--------");

            double[] gains = {0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0};
            foreach (double g in gains)
            {
                int parOk = 0, xorOk = 0;

                for (int i = 0; i < 8; i++) {
                    var node = new OctahedralNode(0);
                    node.VertexGain = g;
                    node.Inject(p3_in[i]);
                    node.Tick();
                    if (Math.Sign(node.Coeffs[7]) == p3_exp[i]) parOk++;
                }
                for (int i = 0; i < 4; i++) {
                    var node = new OctahedralNode(0);
                    node.VertexGain = g;
                    node.Inject(xor_in[i]);
                    node.Tick();
                    if (-Math.Sign(node.Coeffs[4]) == xor_exp[i]) xorOk++;
                }
                Console.WriteLine("  {0,6:F2} |  {1}/8  |  {2}/4", g, parOk, xorOk);
            }
            Console.WriteLine();

            // =========================================================
            // TEST 7: Full spectrum display for one input
            // =========================================================
            Console.WriteLine("TEST 7: Full spectrum for input (+1,-1,+1)");
            Console.WriteLine("==========================================");

            {
                var node = new OctahedralNode(0);
                node.Inject(new double[]{+1,-1,+1});
                node.Tick();

                Console.WriteLine("  Forward mix (subcycle 1, 24+16=40 active):");
                Console.Write("    [");
                for (int k=0; k<8; k++) {
                    Console.Write(F(node.ForwardMix[k]));
                    if (k<7) Console.Write(", ");
                }
                Console.WriteLine("]");

                Console.WriteLine("  Backward mix (subcycle 2, 24+16=40 active):");
                Console.Write("    [");
                for (int k=0; k<8; k++) {
                    Console.Write(F(node.BackwardMix[k]));
                    if (k<7) Console.Write(", ");
                }
                Console.WriteLine("]");

                Console.WriteLine("  Reconciled vertex (subcycle 3, all 64):");
                Console.Write("    [");
                for (int k=0; k<8; k++) {
                    Console.Write(F(node.Vertex[k]));
                    if (k<7) Console.Write(", ");
                }
                Console.WriteLine("]");

                Console.WriteLine("  Hadamard coefficients:");
                for (int c=0; c<8; c++) {
                    string vis = (grades[c]%2==0)?"metric":"frame ";
                    Console.WriteLine("    g{0} {1,5}: {2}  [{3}]",
                        grades[c], cnames[c], F(node.Coeffs[c]), vis);
                }
                Console.WriteLine("  {0}", node);

                Console.WriteLine();
                Console.WriteLine("  Shared vertex parameters:");
                Console.Write("    CouplingIn:  [");
                for (int k=0; k<8; k++) {
                    Console.Write(F(node.CouplingIn[k]));
                    if (k<7) Console.Write(", ");
                }
                Console.WriteLine("]");
                Console.Write("    CouplingOut: [");
                for (int k=0; k<8; k++) {
                    Console.Write(F(node.CouplingOut[k]));
                    if (k<7) Console.Write(", ");
                }
                Console.WriteLine("]");
            }

            Console.WriteLine();

            // =========================================================
            // SUMMARY
            // =========================================================
            Console.WriteLine("==============================================");
            Console.WriteLine("  NODE ARCHITECTURE SUMMARY");
            Console.WriteLine("==============================================");
            Console.WriteLine();
            Console.WriteLine("  64 parameters = 24 (TetA) + 16 (Vertex) + 24 (TetB)");
            Console.WriteLine("  64 = K^3 = the full connection");
            Console.WriteLine();
            Console.WriteLine("  Three subcycles per oscillation:");
            Console.WriteLine("    1. Forward  (TetA + Shared = 40): observer projects");
            Console.WriteLine("    2. Backward (TetB + Shared = 40): witness receives");
            Console.WriteLine("    3. Reconcile (all 64): delta updates shared memory");
            Console.WriteLine();
            Console.WriteLine("  GR runs subcycle 1 only (40 components).");
            Console.WriteLine("  The full node runs all three (64 components).");
            Console.WriteLine("  The difference: torsion = the backward pass = learning.");
            Console.WriteLine();
            Console.WriteLine("  Output: 8-value vertex superposition (structure preserved)");
            Console.WriteLine("  Activation: Born rule on grade-3 Hadamard coefficient");
            Console.WriteLine("  Self-training: forward/backward agreement updates shared");
            Console.WriteLine();

            // =========================================================
            // TEST 8: LATTICE INSTANTIATION
            // =========================================================
            Console.WriteLine("==============================================");
            Console.WriteLine("  LATTICE TESTS");
            Console.WriteLine("==============================================");
            Console.WriteLine();

            Console.WriteLine("TEST 8: Lattice creation and wiring");
            Console.WriteLine("====================================");

            var lattice = new OctahedralLattice(6, 4);
            lattice.PrintStatus();
            Console.WriteLine();

            // Verify wiring: interior nodes should have 4 PairLinks
            // Edge nodes should have 3, corners should have 2
            int corners = 0, edges = 0, interior = 0;
            for (int x = 0; x < lattice.Width; x++)
            {
                for (int y = 0; y < lattice.Height; y++)
                {
                    int links = lattice.Grid[x, y].PairLinks.Count;
                    if (links == 4) interior++;
                    else if (links == 3) edges++;
                    else if (links == 2) corners++;
                }
            }
            Console.WriteLine("  Wiring verification:");
            Console.WriteLine("    Interior (4 neighbors): {0}", interior);
            Console.WriteLine("    Edge (3 neighbors):     {0}", edges);
            Console.WriteLine("    Corner (2 neighbors):   {0}", corners);
            Console.WriteLine("    Total: {0}", interior + edges + corners);
            Console.WriteLine("    Expected: {0}x{1} = {2}", 
                lattice.Width, lattice.Height, lattice.TotalNodes);
            Console.WriteLine();

            // =========================================================
            // TEST 9: WAVE PROPAGATION — does data reach the output?
            // =========================================================
            Console.WriteLine("TEST 9: Wave propagation through lattice");
            Console.WriteLine("========================================");

            lattice = new OctahedralLattice(6, 4);
            
            // Inject on left edge: (+1, -1) on row 0
            Console.WriteLine("  Injecting (+1, -1) into input row 0");
            Console.WriteLine("  Lattice: 6 wide x 4 tall");
            Console.WriteLine();
            Console.WriteLine("  tick | out[0] mu | out[1] mu | out[2] mu | out[3] mu | mean H");
            Console.WriteLine("  -----|-----------|-----------|-----------|-----------|-------");

            for (int t = 0; t < 50; t++)
            {
                lattice.SetInput(0, new double[]{+1, -1});
                lattice.Tick();

                if (t < 10 || t % 10 == 0)
                {
                    double[] outs = lattice.ReadOutputs();
                    Console.WriteLine("  {0,4} |   {1,7:F4} |   {2,7:F4} |   {3,7:F4} |   {4,7:F4} | {5:F4}",
                        t, outs[0], outs[1], outs[2], outs[3], lattice.MeanEntropy());
                }
            }
            Console.WriteLine();

            // =========================================================
            // TEST 10: XOR THROUGH THE LATTICE
            // =========================================================
            Console.WriteLine("TEST 10: XOR through a 4x2 lattice");
            Console.WriteLine("===================================");
            Console.WriteLine();

            // 2 input rows: row 0 = input A, row 1 = input B
            // 2 output rows: read from right edge
            // XOR: when inputs differ, output should differ from when they agree

            correct = 0;
            for (int i = 0; i < 4; i++)
            {
                var lat = new OctahedralLattice(4, 2);

                // Both inputs into the SAME node on axes x and y
                // — same as single-node XOR that gets 4/4
                double a = xor_in[i][0];
                double b = xor_in[i][1];

                for (int t = 0; t < 30; t++)
                {
                    // Inject into ALL left-edge rows
                    for (int row = 0; row < 2; row++)
                        lat.SetInput(row, new double[]{a, b, 0});
                    lat.Tick();
                }

                double[] outs = lat.ReadOutputs();
                
                // Read the xy coefficient from output nodes
                var spectra = lat.ReadSpectra();
                double xyOut0 = spectra[0, 4];
                double xyOut1 = spectra[1, 4];

                // The signal should propagate through to both output rows
                // Read from row 0 (most direct path from input row 0)
                double pred = -Math.Sign(xyOut0);
                bool ok = (pred == xor_exp[i]);
                if (ok) correct++;

                Console.WriteLine("  In: A={0} B={1}  XOR={2}  mu=[{3:F4},{4:F4}]  xy=[{5},{6}]  out0={7}  {8}",
                    a>0?"+1":"-1", b>0?"+1":"-1", xor_exp[i]>0?"+1":"-1",
                    outs[0], outs[1],
                    F(xyOut0), F(xyOut1), pred>0?"+1":"-1",
                    ok?"PASS":"FAIL");
            }
            Console.WriteLine("  XOR through lattice: {0}/4", correct);
            Console.WriteLine();

            // =========================================================
            // TEST 11: DIFFERENT LATTICE SIZES
            // =========================================================
            Console.WriteLine("TEST 11: XOR across different lattice sizes");
            Console.WriteLine("===========================================");
            Console.WriteLine("  size   | ticks | score | total params");
            Console.WriteLine("  -------|-------|-------|-------------");

            int[][] sizes = {
                new int[]{2,2}, new int[]{3,2}, new int[]{4,2},
                new int[]{6,2}, new int[]{4,4}, new int[]{8,4},
                new int[]{10,4}
            };

            foreach (var sz in sizes)
            {
                int w = sz[0], h = sz[1];
                correct = 0;

                for (int i = 0; i < 4; i++)
                {
                    var lat = new OctahedralLattice(w, h);
                    double a = xor_in[i][0];
                    double b = xor_in[i][1];

                    int ticks = w + 3; // wavefront arrives at ~width ticks
                    for (int t = 0; t < ticks; t++)
                    {
                        for (int row = 0; row < h; row++)
                            lat.SetInput(row, new double[]{a, b, 0});
                        lat.Tick();
                    }

                    // Read xy from output row 0 (direct path from input row 0)
                    var spectra = lat.ReadSpectra();
                    double xyOut = spectra[0, 4];

                    if (-Math.Sign(xyOut) == xor_exp[i]) correct++;
                }

                Console.WriteLine("  {0}x{1,-2}  | {2,5} | {3}/4   | {4,5}",
                    w, h, w+3, correct, w*h*64);
            }
            Console.WriteLine();

            // =========================================================
            // FINAL SUMMARY
            // =========================================================
            Console.WriteLine("==============================================");
            Console.WriteLine("  LATTICE SUMMARY");
            Console.WriteLine("==============================================");
            Console.WriteLine();
            Console.WriteLine("  Lattice = rectangular grid of octahedral nodes");
            Console.WriteLine("  Wiring: 4 neighbors per node via parity pairs");
            Console.WriteLine("  2 channels per neighbor x 4 neighbors = 8 channels");
            Console.WriteLine("  2(D+1) = 2^D determines the topology");
            Console.WriteLine();
            Console.WriteLine("  No layers. One continuous wave medium.");
            Console.WriteLine("  Input on left edge. Output on right edge.");
            Console.WriteLine("  Boundary condition = 1.0 where no neighbor.");
            Console.WriteLine("  Standing waves propagate through the lattice.");
            Console.WriteLine("  Computational depth = lattice width.");
        }
    }
}
