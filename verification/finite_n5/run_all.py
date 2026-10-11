from src.verify_n5_saturation import verify
from pathlib import Path
import json, subprocess, sys
base=Path(__file__).resolve().parent
c=json.loads((base/'certificates/n5_q2_capacity.json').read_text())
assert verify()==c
print('n=5, q=2 capacity bound: PASS')
subprocess.run([sys.executable,str(base/'src/verify_n5_q1.py')],check=True)
print('ALL VERIFICATION TESTS PASSED')
