from pyscf import gto, dft
from pyscf.tools import molden

#
# Set up molecule
#
mol = gto.Mole()
mol.atom = """ 
 N                 -2.16259500   -1.85354400   -0.22533800
 C                  2.11156600   -0.97870500   -0.14784400
 C                  2.97208400   -2.14097400   -0.32975800
 C                  2.14061400   -3.23536800   -0.49641100
 C                  0.76982100   -2.76612400   -0.41494900
 C                 -0.38170400   -3.53693000   -0.52322100
 C                 -1.72835500   -3.12712000   -0.42800200
 C                 -2.84917800   -4.05732700   -0.52801000
 C                 -3.99324100   -3.30497900   -0.34474600
 C                 -3.52528300   -1.91564000   -0.18219300
 C                 -4.36369800   -0.79826400   -0.07819400
 C                 -3.98434600    0.54257600    0.06834700
 C                 -4.83689700    1.68909600    0.17752400
 C                 -4.01589700    2.81543600    0.32622400
 C                 -2.64318000    2.35310400    0.29816100
 C                 -1.47322800    3.11900000    0.40176400
 C                 -0.14334400    2.69114500    0.34980700
 C                  0.99418500    3.61950100    0.47214600
 C                  2.12088700    2.84994900    0.37447100
 C                  1.63067500    1.46212100    0.18706900
 C                  2.48354000    0.35288600    0.03607300
 H                 -0.20632700   -4.60002400   -0.69352000
 H                 -5.43427200   -0.98378400   -0.13809400
 H                 -1.61640500    4.19076600    0.53859000
 H                  3.55469500    0.54993100    0.05847100
 N                  0.26845400    1.39634200    0.18222900
 N                 -2.68596400    0.99522600    0.14834300
 H                 -1.86646400    0.39293200    0.09109600
 C                  0.89405600    5.10195200    0.67458000
 H                  0.50733700    5.34460200    1.68311000
 H                  1.87954300    5.58268000    0.53914900
 H                  0.19481000    5.55635600   -0.05042000
 C                 -6.33299800    1.65194400    0.11547000
 H                 -6.79261000    1.86587600    1.09753500
 H                 -6.72049300    2.40824000   -0.58786100
 H                 -6.70251200    0.67019000   -0.21317900
 C                 -2.73066700   -5.53698900   -0.73687700
 H                 -2.11814400   -5.77313500   -1.62365600
 H                 -2.24354000   -6.03151400    0.12224000
 H                 -3.71328900   -6.01373000   -0.87147800
 C                  2.53719500   -4.66123600   -0.73644100
 H                  1.98213700   -5.34337900   -0.06882700
 H                  2.30205200   -4.96770400   -1.77324500
 H                  3.61804500   -4.80530500   -0.55495300
 C                 -4.37653100    4.21851800    0.46357400
 H                 -3.53576700    4.91326800    0.36986600
 C                 -5.58764500    4.76701700    0.68878600
 H                 -6.49481400    4.17774500    0.82231900
 H                 -5.69041400    5.85234500    0.75998400
 C                 -5.35315500   -3.83243100   -0.31603100
 H                 -5.49767800   -4.75183400   -0.89892300
 C                 -6.42684300   -3.36701400    0.35150800
 H                 -6.37668900   -2.49496400    1.00618800
 H                 -7.39087300   -3.87675100    0.27453800
 C                  4.47393400   -2.11732800   -0.31532200
 H                  4.81367900   -1.11413900   -0.62076500
 H                  4.85743300   -2.84554600   -1.04888600
 C                  5.12552600   -2.52506100    1.03130700
 H                  4.42919800   -2.39469900    1.87699200
 H                  5.98106100   -1.86102400    1.24833300
 C                  5.68419700   -4.00102000    1.08419200
 C                  3.55828300    3.28482400    0.42435600
 H                  4.17173300    2.44933300    0.80241500
 H                  3.66113100    4.12442600    1.13146700
 C                  4.13359200    3.81749900   -0.91256100
 H                  5.17241000    3.46297000   -1.04131100
 H                  3.57747500    3.42683900   -1.78149900
 C                  4.18683600    5.39145100   -1.03660400
 O                  3.83817100    6.05486800   -0.01699800
 O                  4.59716200    5.80622800   -2.14092100
 O                  5.58644000   -4.68429900    0.02280900
 O                  6.18324500   -4.32265200    2.18203900
 N                  0.81156200   -1.41080600   -0.20541400
 H                  0.01240100   -0.78770300   -0.11904600
"""
mol.symmetry = True
mol.verbose = 5
mol.max_memory = 40000
mol.spin = 0
mol.charge = -2
mol.output = "_logs/_dft.out"
mol.basis = "ccpvdz"
mol.build()

#
# Mean Field Calculation
#
mf = dft.RKS(mol)
mf.xc = "b3lyp"
mf.chkfile = "_chk/pp_dianion_dz_b3lyp.chk"
mf.kernel()
mf.analyze()

#
# Dump orbitals
#
molden.dump_scf(mf, "_molden/pp_dianion_ccpvdz_b3lyp.molden")