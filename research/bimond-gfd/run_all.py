"""Run every script in this folder and report."""
import subprocess, sys, glob
bad=0
for f in sorted(glob.glob('0*.py')):
    r=subprocess.run([sys.executable,f],capture_output=True,text=True)
    n_pass=r.stdout.count('PASS'); n_fail=r.stdout.count('FAIL')
    print(f"{f:34s} PASS {n_pass:2d}  FAIL {n_fail}  exit {r.returncode}"); bad+=n_fail+(r.returncode!=0)
sys.exit(1 if bad else 0)
