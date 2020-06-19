import pandas as pd

orca = pd.read_csv("orca_data.csv")
pyscf = pd.read_csv("sa-3-mcscf_nevpt2.csv")


with open("NEVPT2_summary.txt", "w") as f:
    f.write("PySCF Results (in cm^-1)\n")
    f.write(pyscf.to_string(float_format="%.0f", index=False))
    f.write("\n\n")

    f.write("ORCA Results (in cm^-1)\n")
    f.write(orca.to_string(float_format="%.0f", index=False))
    f.write("\n\n")

    f.write("PySCF-ORCA Results Differences (in cm^-1)\n")

    pyscf["Qx"] -= orca["Qx"]
    pyscf["Qy"] -= orca["Qy"]
    pyscf["\u0394(Qy-Qx)"] -= orca["\u0394(Qy-Qx)"]
    print(pyscf.to_string(float_format="%.0f", index=False))
    f.write(pyscf.to_string(float_format="%.0f", index=False))

