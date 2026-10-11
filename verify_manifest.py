#!/usr/bin/env python3
"""Verify SHA-256 sums of the clean source package."""
import hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
records=[x.split('  ',1) for x in (root/'SHA256SUMS').read_text().splitlines() if x.strip()]
for digest, rel in records:
    f=root/rel
    assert f.is_file(),rel
    actual=hashlib.sha256(f.read_bytes()).hexdigest()
    assert digest==actual,rel
print(f'PASS: {len(records)} SHA-256 records')
