import subprocess
import sys
from pathlib import Path
subprocess.run([sys.executable, str(Path(__file__).with_name('exact_cover.py'))], check=True)
print('All temporal-template checks passed.')
