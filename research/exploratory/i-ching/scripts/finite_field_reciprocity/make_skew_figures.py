from pathlib import Path
from xml.sax.saxutils import escape
import math
out=Path(__file__).resolve().parents[2]/'figures';out.mkdir(exist_ok=True)
def svg(name,w,h,body):
    (out/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#f8fafc"/><g font-family="Arial,sans-serif" fill="#18324b">{body}</g></svg>')
def text(x,y,s,size=16,weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}">{escape(s)}</text>'
b=text(30,42,'Hexagram Walsh read: the 28 skew channels',25,'bold')+text(30,69,'The normalized Walsh matrix maps the symplectic read to matrix transposition.',14)
for i in range(8):
    for j in range(8):
        color='#a6bfd5' if i==j else '#4079a9' if i<j else '#cb913d'
        b+=f'<rect x="{35+j*33}" y="{105+i*33}" width="30" height="30" rx="3" fill="{color}"/>'
b+=text(337,131,'W(X) = H Xᵀ H',22,'bold')+text(337,172,'Y = XH  →  Yᵀ',22)+text(337,220,'36 symmetric directions (+1)',18)+text(337,262,'28 skew directions (−1)',18)+text(337,302,'28 = 7 nonzero shifts × 4 signs',17)+text(35,406,'The two triangles are paired: the lower triangle is not a separate physical register.',14)
svg('walsh_skew_channels.svg',780,435,b)
b=text(30,40,'Two exact averaging laws — distinct domains',25,'bold')+text(30,67,'Conditional on the complete signed shift and linear relabeling symmetry.',14)
for x,y,w,h,stroke in [(30,94,330,215,'#4079a9'),(390,94,360,215,'#cb913d')]: b+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="{stroke}" stroke-width="2"/>'
b+=text(48,123,'28 × 28 channel covariance',18,'bold')+text(48,155,'Signed shift / phase twirl',16)+text(48,183,'↓  kills off-diagonal entries',15)+text(48,212,'GL(3,2) relabeling',16)+text(48,241,'↓  equalizes all 28 diagonal entries',15)+text(48,279,'tr(C) I / 28',22,'bold')
b+=text(408,123,'8 × 8 trigram operator',18,'bold')+text(408,155,'Average skew conjugation',16)+text(408,184,'Φ(X) = (tr(X) I − Xᵀ) / 7',19,'bold')+text(408,220,'1        common mode (1)',16)+text(408,250,'−1/7   symmetric traceless (35)',16)+text(408,280,'+1/7   skew (28)',16)
b+=text(30,345,'Marked Heaven–Earth symmetry alone allows unequal channel weights.',17,'bold')+text(30,374,'Neither average derives the physical gain or the additive inverse-action law.',15)
svg('skew_channel_action.svg',780,400,b)
