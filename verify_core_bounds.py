"""Run general bounds and companion finite checks (Python standard library only)."""
from src.bounds_and_moments import simulate
from src.verify_n7_certificate import verify
from src.verify_bounds import run
from src.verify_one_step_family import check_one_step
from src.verify_n4_exact import verify_n4
from src.packing import test_packing
from src.verify_saturation import run as run_saturation

from src.verify_multiround_amplification import run as run_amplification
from src.verify_log_separation import run as run_log_separation

if __name__=='__main__':
    print('Bound checks:',run(128))
    print('Seven-coordinate certificate:',verify())
    print('Exact n=4:',verify_n4())
    print('Bit-state packing:',test_packing())
    for n in range(2,9): print('One-step uniform formula:',check_one_step(n))
    cases=[(7,1,1),(15,1,1),(19,2,2),(31,3,2),(50,5,4),(5,2,3),(63,1,3)]
    for n,t,q in cases:
        print('Moment sketch',n,t,q,'simulations=',simulate(n,t,q,250))
    print('Forced-pair saturation checks:', run_saturation())
    print('Multiround pair-amplification cases:',len(run_amplification()))
    print('Logarithmic-gap integer certificates:',len(run_log_separation('certificates/log_separation_parameters.csv')))
    print('PASS: core bounds, encoders, and multiround counts')
