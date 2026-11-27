from pathlib import Path
from math import cos,sin,pi
out=Path(__file__).resolve().parents[2]/'figures';out.mkdir(exist_ok=True)
def svg(name,body,w=860,h=440):
    (out/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#f8fafc"/><g font-family="Arial,sans-serif" fill="#172e47">{body}</g></svg>')
b='<text x="32" y="40" font-size="25" font-weight="bold">Second threefold cycle: shared read and Walsh dual</text><text x="32" y="68" font-size="15">Exact principal plane, 60° between the unoriented projector lines</text>'
cx,cy,r=237,238,145
for i in range(3):
    a=-pi/2+i*2*pi/3;x,y=cx+r*cos(a),cy+r*sin(a); xx,yy=cx-r*cos(a),cy-r*sin(a)
    b+=f'<line x1="{xx}" y1="{yy}" x2="{x}" y2="{y}" stroke="#8598ad" stroke-dasharray="5 5"/><line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#386a9a" stroke-width="3"/><circle cx="{x}" cy="{y}" r="15" fill="#386a9a"/><text x="{x}" y="{y+5}" text-anchor="middle" font-size="14" fill="white">{i}</text>'
b+='<circle cx="237" cy="238" r="5" fill="#172e47"/><path d="M237 184 A54 54 0 0 1 284 265" stroke="#ba8236" fill="none" stroke-width="3"/><text x="293" y="212" font-size="15" fill="#985f22">120°</text><g font-size="19"><text x="470" y="137">C³ = I</text><text x="470" y="180">⟨v, Cv⟩ = −1/2</text><text x="470" y="223">Three projected returns: −1/8</text><text x="470" y="266">Intensity: 1/64</text></g><text x="470" y="320" font-size="15">Reversible rotation and projected read</text><text x="470" y="342" font-size="15">are different operations.</text><text x="32" y="416" font-size="13">Abstract operator plane, not a physical vortex trajectory.</text>'
svg('shared_zone_walsh_rotation.svg',b)
b='<text x="32" y="40" font-size="25" font-weight="bold">Minimal exchange-even Walsh completion</text><text x="32" y="67" font-size="14">Full invariant space: 22 modes (includes zero orbit)</text>'
for i,(name,rank,common,m,dark,leak) in enumerate([('Q: shared saturation',14,8,6,2,6),('P+: even completion',18,16,2,2,2),('P−: odd completion',18,14,4,0,4)]):
    y=115+93*i;b+=f'<text x="32" y="{y}" font-size="17" font-weight="bold">{name}</text><text x="828" y="{y}" text-anchor="end" font-size="15">rank {rank} · leakage {leak}</text>'
    x=32
    for n,col,label in [(common,'#386a9a','common'),(2*m,'#ba8236','mixing'),(dark,'#82909d','dark')]:
        if n:
            ww=796*n/22;b+=f'<rect x="{x}" y="{y+12}" width="{ww}" height="28" fill="{col}"/><text x="{x+ww/2}" y="{y+31}" text-anchor="middle" font-size="13" fill="white">{n} {label if ww>90 else ""}</text>';x+=ww
b+='<text x="32" y="418" font-size="14">Even completion removes four mixing planes without activating the two original dark modes.</text>'
svg('shared_zone_even_completion.svg',b)
