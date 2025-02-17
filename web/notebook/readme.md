# The Notebook's Secret 

Author: Dante 

>Difficulty: medium

Flag: `magpieCTF{cryp70_k3y_4cc3ss_gr4nt3d}`

## Backstory

Another late night at the precinct, another piece of evidence to sift through. This time, it's Professor Richard Hash's research notebook.
Your partner, Edward Cors, leans back in his chair. "I don't know, this feels like it's pointing straight at Hash. The guy's always preaching
about transparency, about making everything public. Maybe he decided to take matters into his own hands." But something about the notebook
catches your eye. The last entry, dated February 21st, 1933, one day before Krypto's murder, hints at an unexpected development. It seems Krypto and
Hash were on the verge of announcing something big. 

## Solve

1. Open the Jupyter notebook, find the SSH key thats in `/home/rhash/.local/share/research_data` using system commands.
2. Use the SSH key to log into ckrypto’s account on the machine.
3. After logging in, retrieve the flag from `/home/ckrypto/.private/partnership_agreement`.
