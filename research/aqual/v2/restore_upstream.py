#!/usr/bin/env python3
"""Hydrate exact original sources at the inspected commit. No changes to checkout."""
from pathlib import Path
import argparse, hashlib, json, subprocess, urllib.request, urllib.parse

ROOT=Path(__file__).resolve().parent
MANIFEST=json.loads((ROOT/'upstream/original_manifest.json').read_text())
REF=MANIFEST['commit']; REPO=MANIFEST['repository']
PROOFS=['aqual-energy-functional','constitutive-law-exchange-symmetry','constitutive-law-tug-of-war','bimetric-two-potential-energy','bimetric-lock-constitutive-law','sst-quasi-static-limit','sst-covariant-time-leg','sst-khronon-preferred-frame','net-field-rule','sst-mountain-scale','closure-surface','recursive-field-closure-response']
EXTRAS=['CLOSURE_OF_CLOSURES.md','EINSTEIN_TETA_PARTITION.md','GFD_COLES_NOTES.md','research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md','research/hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md','research/bimond-gfd/README.md','research/two-connection-dual-chamber/README.md','research/bound-gravity-and-packing/README.md','docs/02-gravitation/02-field-equation.md','docs/02-gravitation/03-constitutive-law-mu-x.md','docs/02-gravitation/05-poisson-scale-invariance.md','docs/02-gravitation/06-covariant-completion.md']

def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])

def blob_id(b): return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()

def retrieve(repo,path):
    if repo: return git(repo,'show',f'{REF}:{path}')
    url=f'https://raw.githubusercontent.com/{REPO}/{REF}/'+urllib.parse.quote(path,safe='/')
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'GFD-research-source-restore'}),timeout=30) as r: return r.read()

def write_exact(path,b):
    dest=ROOT/'upstream'/'snapshot'/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists() and dest.read_bytes()!=b: raise RuntimeError(f'Refusing to overwrite different existing file: {dest}')
    dest.write_bytes(b)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,help='Local git checkout with the pinned commit');p.add_argument('--proofs',action='store_true',help='Also copy relevant proof directories and supporting notes (requires a local checkout)');args=p.parse_args()
    if args.proofs and not args.repo: p.error('--proofs requires --repo so dependencies and all original proof files can be copied without guessing paths')
    if args.repo: git(args.repo,'cat-file','-e',REF+'^{commit}')
    for f in MANIFEST['files']:
        data=retrieve(args.repo,f['path'])
        if len(data)!=f['size'] or blob_id(data)!=f['sha']: raise RuntimeError('Blob mismatch: '+f['path'])
        write_exact(f['path'],data); print('verified',f['path'],f['sha'])
    if args.proofs:
        paths=[f'proofs/{p}' for p in PROOFS]+EXTRAS
        # Include all proof source dependencies (some Lean projects import sibling proof directories).
        names=git(args.repo,'ls-tree','-r','--name-only','-z',REF,'--',*paths).decode().split('\0')
        for name in filter(None,names): write_exact(name,retrieve(args.repo,name)); print('copied',name)
        # A complete Lean dependency checkout is available in the pinned original repository.
        print('For Lean builds use the original complete checkout at the pinned revision; selected proof copies may have sibling dependencies.')
    print('Source copy complete. New synthesis unchanged.')
if __name__=='__main__': main()
