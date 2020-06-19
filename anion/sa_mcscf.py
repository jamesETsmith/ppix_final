"""
State-average CASSCF with small active space CAS(4e,4o).

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 1/29/2020
"""
import numpy as np
from pyscf import dft, mcscf
from pyscf.lib import chkfile
from pyscf.tools import molden

#
# Load MF orbitals
#
chkname = "_chk/pp_dz_b3lyp.chk"
mol = chkfile.load_mol(chkname)
mol.verbose = 5
mf = dft.RKS(mol)
mf.__dict__.update(chkfile.load(chkname, "scf"))

#
# SA-MCSCF
#
nelecas, ncas = (4, 4)
n_states = 3
weights = np.ones(n_states) / n_states

mc = mcscf.CASSCF(mf, ncas, nelecas).state_average_(weights)
mc.fix_spin(ss=0)
mc.natorb = True
mc.chkfile = "_chk/pp_dz_cas_4e_4o.chk"
cas_list = [147, 148, 150, 151]
mo = mcscf.sort_mo(mc, mf.mo_coeff, cas_list)
mc.mc1step(mo)


#
# Analysis and processing
#
mc.analyze()
molden.from_mcscf(mc, "_molden/pp_anion_dz_cas_4e_4o.molden")
