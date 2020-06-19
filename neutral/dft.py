from pyscf import gto, dft
from pyscf.tools import molden

#
# Set up molecule
#
mol = gto.Mole()
mol.atom = """
 N                 -2.20950500    1.84222500   -0.04450500
 C                  1.89655600    0.78785700   -0.60550200
 C                  2.81546000    1.90264900   -0.61988800
 C                  2.07603900    3.04880200   -0.45712600
 C                  0.69053000    2.65991000   -0.34106500
 C                 -0.40355600    3.49269600   -0.17409700
 C                 -1.74611800    3.11446300   -0.05002800
 C                 -2.83161400    4.08339300    0.09042100
 C                 -3.98050600    3.35155500    0.15525000
 C                 -3.55653100    1.94218000    0.09742400
 C                 -4.42577400    0.86527000    0.25272700
 C                 -4.10714300   -0.49078200    0.23243400
 C                 -5.00857300   -1.59642300    0.39310000
 C                 -4.26130900   -2.75752800    0.28036200
 C                 -2.88990100   -2.36776800    0.06177000
 C                 -1.78812700   -3.19937300   -0.11745300
 C                 -0.46536100   -2.81848100   -0.33511900
 C                  0.61786700   -3.78320200   -0.53333100
 C                  1.74571300   -3.04267000   -0.72138000
 C                  1.32328300   -1.63951700   -0.62653300
 C                  2.20537900   -0.55721100   -0.73444400
 H                 -0.18677100    4.56026300   -0.13809400
 H                 -5.47276900    1.10580000    0.42379700
 H                 -1.99214500   -4.26927700   -0.09768200
 H                  3.25426800   -0.77999800   -0.92226300
 N                 -0.00607300   -1.54089300   -0.39589800
 N                 -2.85769200   -1.00663200    0.03984100
 H                 -2.01903000   -0.44778500   -0.09494100
 C                  0.45747300   -5.26966900   -0.53571400
 H                  0.09892500   -5.64088200    0.43767800
 H                 -0.27451200   -5.59371700   -1.29187800
 H                  1.40449200   -5.78150600   -0.75396200
 C                 -6.47135600   -1.46716200    0.66671900
 H                 -6.70590000   -0.51623800    1.16343700
 H                 -7.06695200   -1.51041300   -0.25989500
 H                 -6.81882800   -2.28369100    1.31521300
 C                 -2.67010800    5.56856500    0.10890100
 H                 -1.98075900    5.89031000    0.90527400
 H                 -2.26000400    5.94043500   -0.84373200
 H                 -3.62991300    6.07613800    0.27036900
 C                  2.56444500    4.45957200   -0.38720000
 H                  2.08265100    5.08948200   -1.15092200
 H                  2.34539500    4.91164200    0.59280700
 H                  3.64934000    4.51662000   -0.54192900
 C                 -4.69553600   -4.14908400    0.38511200
 H                 -3.93150900   -4.85626500    0.72203200
 C                 -5.91158100   -4.63131200    0.11013700
 H                 -6.71905900   -4.00277100   -0.26619500
 H                 -6.12782500   -5.69334200    0.23637300
 C                 -5.34191500    3.88150000    0.26188100
 H                 -5.44994100    4.77873700    0.88107500
 C                 -6.43441200    3.40580700   -0.34350600
 H                 -6.39642200    2.54731800   -1.01683900
 H                 -7.40431600    3.88565900   -0.20078400
 C                  4.30609000    1.78068100   -0.69822900
 H                  4.58914500    0.91362700   -1.31355700
 H                  4.72808300    2.66512300   -1.19741300
 C                  4.95477400    1.65224000    0.69422600
 H                  4.67994400    2.52178100    1.30549400
 H                  4.59225800    0.74359800    1.19729000
 C                  6.46874500    1.64995600    0.57749400
 C                  3.13452200   -3.54891800   -0.97944500
 H                  3.66049500   -2.91284000   -1.70720500
 H                  3.07400500   -4.54676200   -1.43577500
 C                  4.02168100   -3.67284700    0.27971400
 H                  3.47338100   -4.19012900    1.08157300
 H                  4.91341700   -4.26690300    0.03495300
 C                  4.53666700   -2.33096100    0.74046200
 O                  5.40988100   -1.73974700    0.14443400
 O                  7.04436600    0.46550400    0.34065500
 O                  7.12570500    2.65745000    0.64243700
 H                  6.38825500   -0.26311000    0.33673600
 N                  0.64470000    1.29842900   -0.42771400
 H                 -0.20484500    0.74272900   -0.38069400
 O                  3.98457900   -1.77374000    1.82326400
 H                  3.23637200   -2.30639300    2.13283500"""
mol.symmetry = True
mol.verbose = 5
mol.max_memory = 40000
mol.spin = 0
mol.charge = 0
mol.output = "_logs/_dft.out"
mol.basis = "ccpvdz"
mol.build()

#
# Mean Field Calculation
#
mf = dft.RKS(mol)
mf.xc = "b3lyp"
mf.chkfile = "_chk/pp_neutral_dz_b3lyp.chk"
mf.kernel()
mf.analyze()

#
# Dump orbitals
#
molden.dump_scf(mf, "_molden/pp_neutral_ccpvdz_b3lyp.molden")
