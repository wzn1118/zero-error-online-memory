"""Rebuild the V3 manuscript from the unchanged V2 research source."""
from pathlib import Path
here=Path(__file__).resolve().parent
root=here.parent
old=(root/'paper.tex').read_text(encoding='utf-8')
section=(here/'extension.tex').read_text(encoding='utf-8')
anchor=r'\section{Multiround pair-counting converse}'
assert old.count(anchor)==1
old=old.replace(anchor,section+'\n'+anchor)
old=old.replace('Global One-Write Saturation, Sharp Storage Gaps, and Syndrome Compatibility','State-Alphabet Deficits, Sharp Storage Gaps, and Syndrome Compatibility')
abstract_anchor=' Further results include uniform bounds over all horizons,'
assert old.count(abstract_anchor)==1
old=old.replace(abstract_anchor,
    r' We also prove an exact one-write state-alphabet saturation threshold and the integer-valued law'
    r' $2^n-\kappa_1(n,n-2)=\Theta(2^n/n)$ at every length, using antipodal distance-three codes'
    r' and a forced-edge converse. Perfect Hamming codes sharpen the constructive constant.'
    +abstract_anchor)
old=old.replace(r'\section{Conclusion}',
    r'\section{Conclusion}'+'\n'+r'The one-write label alphabet saturates exactly for $q\ge n-1$. At $q=n-2$, antipodal-code packing and a forced-edge converse give a state deficit of order $\Theta(2^n/n)$ for all lengths. These integer statements refine the rounded-bit theorems.'+'\n')
old=old.replace(r'\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black,citecolor=blue!45!black}',
 r'\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black,citecolor=blue!45!black,pdfauthor={Zinan Wang},pdftitle={Zero-Error Online Memory under Blind Overwrites: State-Alphabet Deficits, Sharp Storage Gaps, and Syndrome Compatibility}}')
assert old.count(section)==1
(here/'paper.tex').write_text(old,encoding='utf-8')
print('Assembled V3 paper.tex:',len(old),'characters')
