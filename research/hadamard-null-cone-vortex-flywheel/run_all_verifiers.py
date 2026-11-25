"""Run the seventeen mathematical verifiers and retain their output. Stops on error."""
from pathlib import Path
import os, subprocess, sys
root=Path(__file__).resolve().parent
archive=root/'archive'/'stages-I-VI'
logs=root/'rerun_logs'; logs.mkdir(exist_ok=True)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
scripts=[archive/(n+'.py') for n in ('verify_hadamard_null_cone','verify_current_closure','verify_extended_validation','verify_core_hardening','verify_face_core_stability','verify_triforce_flywheel')]+[root/(n+'.py') for n in ('verify_sustained_flywheel','verify_open_throat','verify_coupled_origins','verify_four_port_packing','verify_corner_first','verify_hadamard_flower','verify_unified_flower','verify_optical_ports','verify_field_read','verify_spectral_read','verify_matter_charge')]
with (logs/'status.txt').open('w') as statuses:
    for script in scripts:
        print('Running',script.name,flush=True)
        with (logs/(script.stem+'.txt')).open('w') as out:
            result=subprocess.run([sys.executable,str(script)],cwd=script.parent,env=env,stdout=out,stderr=subprocess.STDOUT)
        print(script.stem,result.returncode,file=statuses,flush=True)
        result.check_returncode()
print('All seventeen mathematical verifiers passed.')
