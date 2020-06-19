from pyscf import gto, dft
from pyscf.tools import molden

#
# Set up molecule
#
mol = gto.Mole()
mol.atom = """
N                 -2.36795500    1.79184900    0.02421900
C                  1.81694500    0.89020200   -0.39468100
C                  2.69329200    2.04388100   -0.46235700
C                  1.90056000    3.16914000   -0.32481300
C                  0.52776300    2.72750300   -0.18605500
C                 -0.61020300    3.51691800   -0.04369000
C                 -1.94855000    3.08839300    0.04632200
C                 -3.07627800    4.01052300    0.16397000
C                 -4.21061400    3.22783300    0.17985100
C                 -3.72737200    1.83349300    0.11702000
C                 -4.55590600    0.70785700    0.21954800
C                 -4.18927300   -0.64204000    0.17403000
C                 -5.05465100   -1.78412200    0.28349200
C                 -4.26023400   -2.92864000    0.16262200
C                 -2.89183100   -2.48558300   -0.00946200
C                 -1.74197800   -3.27006700   -0.16129400
C                 -0.41928700   -2.83122300   -0.29345100
C                  0.72705200   -3.74476700   -0.43773100
C                  1.83592400   -2.94958500   -0.52300500
C                  1.33242100   -1.56323700   -0.42883100
C                  2.18669800   -0.45057900   -0.47788600
H                 -0.43605200    4.59335700   -0.00933300
H                 -5.61615400    0.90135000    0.37009100
H                 -1.89848900   -4.34884200   -0.17388800
H                  3.26111500   -0.65738300   -0.54797900
N                 -0.02301600   -1.52399300   -0.29619500
N                 -2.91099000   -1.11832500   -0.00075000
H                 -2.08174300   -0.53724800   -0.10789500
C                  0.64047400   -5.24068600   -0.47198200
H                  0.23200700   -5.64934100    0.46938700
H                 -0.01467900   -5.59743100   -1.28639800
H                  1.63164400   -5.69290900   -0.62122700
C                 -6.53209100   -1.71754600    0.51952400
H                 -6.83986700   -0.73218800    0.89723500
H                 -7.10751100   -1.91057100   -0.40374700
H                 -6.84682000   -2.47365600    1.25676800
C                 -2.97447700    5.50511500    0.20495300
H                 -2.29114200    5.84342500    1.00234800
H                 -2.58214100    5.91215400   -0.74378100
H                 -3.95208200    5.97751400    0.37971200
C                  2.32989300    4.60523100   -0.32352200
H                  1.81619800    5.18549900   -1.10918400
H                  2.10250800    5.09455000    0.63932900
H                  3.41185900    4.69717900   -0.49057800
C                 -4.63909700   -4.33477900    0.22077900
H                 -3.80879500   -5.02585900    0.40015700
C                 -5.86274900   -4.87880900    0.07981700
H                 -6.75432500   -4.28877700   -0.13355100
H                 -5.99485300   -5.96019800    0.15838700
C                 -5.58396600    3.72307300    0.23948600
H                 -5.70818300    4.67114600    0.77830600
C                 -6.68823300    3.18568000   -0.31078200
H                 -6.65778800    2.27685100   -0.91515200
H                 -7.66061800    3.66905300   -0.18856000
C                  4.18076700    1.96741600   -0.65633300
H                  4.41976700    1.13737300   -1.33797600
H                  4.53752200    2.89112300   -1.14003500
C                  4.98365200    1.76302000    0.65148900
H                  4.80246100    2.60465500    1.33621300
H                  4.67051600    0.82314300    1.12741500
C                  6.48394200    1.73308000    0.33563300
C                  3.28304100   -3.33034900   -0.65794800
H                  3.76392400   -2.67641300   -1.40180400
H                  3.34745900   -4.35806900   -1.05043300
C                  4.10995600   -3.22268300    0.65524200
H                  3.46696300   -2.84434500    1.47025400
H                  4.46597000   -4.21044200    0.98500500
C                  5.34103700   -2.27756200    0.60963300
O                  6.30140200   -2.54578800    1.33353000
O                  5.21441700   -1.24946000   -0.16788100
O                  6.97534500    0.58653800   -0.09749600
O                  7.16195900    2.74479500    0.43146800
H                  6.28450200   -0.19725800   -0.08634900
N                  0.53849800    1.35786600   -0.23665800
H                 -0.28368000    0.76548500   -0.15155400"""
mol.symmetry = True
mol.verbose = 5
mol.max_memory = 40000
mol.spin = 0
mol.charge = -1
mol.output = "_logs/_dft.out"
mol.basis = "ccpvdz"
mol.build()

#
# Mean Field Calculation
#
mf = dft.RKS(mol)
mf.xc = "b3lyp"
mf.chkfile = "_chk/pp_dz_b3lyp.chk"
mf.kernel()
mf.analyze()

#
# Dump orbitals
#
molden.dump_scf(mf, "_molden/pp_ccpvdz_b3lyp.molden")
