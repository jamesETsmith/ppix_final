"""
Read in state-average CASSCF with small active space CAS(4e,4o) and perform PT2
for anion-like species plus a point charge to approximate the deprotonated 
carboxylic acid.

For now I the location of the point charge was chosen to be the location of the
deprotonated oxygen on the -COO- group to try to keep the position of the minus
charge as similar as possible.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 2/14/2020
"""
import sys
import numpy as np
from pyscf import dft, qmmm, mcscf, mrpt, lib
from pyscf.lib import chkfile

#
# Check args
#
if len(sys.argv) != 2:
    raise AssertionError(
        "Incorrect # of args\n"
        "Use like: python pt2.py 1\n"
        "Where 1 is the root you want to target."
    )
target_state = int(sys.argv[-1])

#
# Load MF orbitals
#
chkname = "_chk/pp_anion_pt_chg_dz_b3lyp.chk"
mol = chkfile.load_mol(chkname)
mol.max_memory = int(1e5)
mf = dft.RKS(mol)
mf.__dict__.update(chkfile.load(chkname, "scf"))

# Need to add this back in bc it's not loaded from chkfile
# Old O location from -COO- group
chg_coords = np.array([[-5.7124, -3.6452, 0.1326]])
mf = qmmm.mm_charge(mf, chg_coords, [-1.0])

#
# Load SA-MCSCF
#
nelecas, ncas = (4, 4)
n_states = 3
weights = np.ones(n_states) / n_states

mc0 = mcscf.CASSCF(mf, ncas, nelecas).state_average_(weights)
mc0.fix_spin(ss=0)
mc0.chkfile = "_chk/pp_anion_pt_chg_dz_cas_4e_4o.chk"
mc0.__dict__.update(chkfile.load(mc0.chkfile, "mcscf"))

#
# NEVPT2
#
mc = mcscf.CASCI(mf, ncas, nelecas)
mc.fix_spin(ss=0)
mc.fcisolver.nroots = n_states
mc.kernel(mc0.mo_coeff)
np.savetxt(f"_energies/SA-{n_states}-CASSCF({nelecas},{ncas}).txt", mc.e_tot)


lib.num_threads(1)
print(f"NUM THREADS NOW = {lib.num_threads()}")
e_corr = mrpt.NEVPT(mc, root=target_state).kernel()
e_tot = mc.e_tot[target_state] + e_corr

np.savetxt(f"_energies/NEVPT2-{target_state}.txt", np.array([e_tot]))
lib.num_threads(24)
print(f"NUM THREADS NOW = {lib.num_threads()}")
