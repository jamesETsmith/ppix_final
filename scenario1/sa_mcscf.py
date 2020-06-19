"""
State-average CASSCF with small active space CAS(4e,4o)
for anion-like species plus a point charge to approximate the deprotonated 
carboxylic acid.

For now I the location of the point charge was chosen to be the location of the
deprotonated oxygen on the -COO- group to try to keep the position of the minus
charge as similar as possible.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 2/14/2020
"""
import numpy as np
from pyscf import gto, dft, qmmm, mcscf
from pyscf.tools import molden
from pyscf.lib import chkfile

#
# Set up molecule
#
mol = gto.Mole()
mol.atom = """N   0.228   1.915  -0.049
C  -3.327  -0.438   0.015
C  -4.557   0.321   0.003
C  -4.224   1.648  -0.038
C  -2.782   1.737  -0.050
C  -2.017   2.885  -0.078
C  -0.617   2.968  -0.069
C   0.099   4.238  -0.070
C   1.423   3.919  -0.025
C   1.478   2.452  -0.038
C   2.659   1.724  -0.107
C   2.800   0.339  -0.123
C   4.021  -0.406  -0.186
C   3.687  -1.748  -0.152
C   2.254  -1.835  -0.085
C   1.473  -2.989  -0.031
C   0.090  -3.064   0.015
C  -0.641  -4.336   0.065
C  -1.955  -4.005   0.088
C  -1.998  -2.538   0.053
C  -3.195  -1.814   0.052
H  -2.565   3.822  -0.102
H   3.578   2.296  -0.161
H   2.017  -3.929  -0.020
H  -4.119  -2.383   0.081
N  -0.760  -2.000   0.013
N   1.775  -0.562  -0.066
H   0.792  -0.316  -0.018
C  -0.002  -5.688   0.082
H   0.606  -5.853  -0.815
H   0.657  -5.806   0.950
H  -0.750  -6.485   0.125
C   5.384   0.199  -0.306
H   5.356   1.140  -0.863
H   5.823   0.409   0.677
H   6.060  -0.484  -0.829
C  -0.535   5.593  -0.073
H  -1.186   5.729  -0.945
H  -1.151   5.746   0.821
H   0.218   6.385  -0.089
C  -5.125   2.842  -0.064
H  -4.948   3.490   0.802
H  -4.957   3.445  -0.964
H  -6.178   2.552  -0.051
C   4.570  -2.912  -0.213
H   4.171  -3.786  -0.727
C   5.801  -2.989   0.301
H   6.246  -2.172   0.861
H   6.395  -3.891   0.194
C   2.548   4.856   0.030
H   2.455   5.748  -0.589
C   3.641   4.725   0.787
H   3.774   3.885   1.464
H   4.427   5.473   0.770
C  -5.914  -0.308   0.033
H  -6.707   0.445   0.014
C  -3.158  -4.893   0.137
H  -6.063  -0.969  -0.828
N  -2.301   0.459  -0.019
H  -1.318   0.209  -0.024
H  -6.051  -0.911   0.938
H  -2.877  -5.949   0.159
H  -3.765  -4.694   1.029
H  -3.802  -4.740  -0.737
"""
mol.symmetry = True
mol.verbose = 5
mol.unit = "Angstrom"
mol.max_memory = 40000
mol.spin = 0
mol.charge = 0
mol.output = "_logs/_sa_mcscf.out"
mol.basis = "ccpvdz"
mol.build()

#
# Mean Field Calculation
#

# Old O location from -COO- group
chg_coords = np.array([[-5.7124, -3.6452, 0.1326]])
mf = qmmm.mm_charge(dft.RKS(mol), chg_coords, [-1.0])
mf.xc = "b3lyp"
mf.chkfile = "_chk/pp_anion_pt_chg_dz_b3lyp.chk"
mf.kernel()
mf.analyze()

#
# Dump orbitals
#
molden.dump_scf(mf, "_molden/pp_anion_pt_chg_dz_b3lyp.molden")

#
# SA-MCSCF
#
nelecas, ncas = (4, 4)
n_states = 3
weights = np.ones(n_states) / n_states

mc = mcscf.CASSCF(mf, ncas, nelecas).state_average_(weights)
mc.fix_spin(ss=0)
mc.natorb = True
mc.chkfile = "_chk/pp_anion_pt_chg_dz_cas_4e_4o.chk"
cas_list = [118, 119, 120, 121]
mo = mcscf.sort_mo(mc, mf.mo_coeff, cas_list)
mc.mc1step(mo)

#
# Analysis and processing
#
mc.analyze()
molden.from_mcscf(mc, "_molden/pp_anion_pt_chg_dz_cas.molden")
molden.from_mo(mol, "_molden/pp_anion_pt_chg_dz_cas_alt.molden", mc.mo_coeff)
