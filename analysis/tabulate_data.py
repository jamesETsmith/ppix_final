import numpy as np
import pandas as pd
from scipy.constants import physical_constants

from myplot_utils import get_casscf_data, get_nevpt2_data


#
# Full Protoporphyrin Stucture
#
# fmt: off
neutral_pt2 = get_nevpt2_data("../neutral/_energies/", n_states=3)
neutral_cas = get_casscf_data("../neutral/_energies/SA-3-CASSCF(4,4).txt")
anion_pt2 = get_nevpt2_data("../anion/_energies/", n_states=3)
anion_cas = get_casscf_data("../anion/_energies/SA-3-CASSCF(4,4).txt")
dianion_pt2 = get_nevpt2_data("../dianion/_energies/", n_states=3)
dianion_cas = get_casscf_data("../dianion/_energies/SA-3-CASSCF(4,4).txt")

dianion_pt_chg_cas = get_casscf_data("../scenario4/_energies/SA-3-CASSCF(4,4).txt")
dianion_pt_chg_pt2 = get_nevpt2_data("../scenario4/_energies/", n_states=3)

apc_1_cas = get_casscf_data("../scenario1/_energies/SA-3-CASSCF(4,4).txt")
apc_1_pt2 = get_nevpt2_data("../scenario1/_energies/", n_states=3)
apc_2_cas = get_casscf_data("../scenario2/_energies/SA-3-CASSCF(4,4).txt")
apc_2_pt2 = get_nevpt2_data("../scenario2/_energies/", n_states=3)
apc_3_cas = get_casscf_data("../scenario3/_energies/SA-3-CASSCF(4,4).txt")
apc_3_pt2 = get_nevpt2_data("../scenario3/_energies/", n_states=3)
# fmt: on


ddict = {"species": [], "Qx": [], "Qy": []}


def add_to_ddict(species: str, Qx: float, Qy: float, dd: dict):
    dd["species"].append(species)
    dd["Qx"].append(Qx)
    dd["Qy"].append(Qy)


add_to_ddict("Neutral", neutral_pt2[1], neutral_pt2[2], ddict)
add_to_ddict("Anion", anion_pt2[1], anion_pt2[2], ddict)
add_to_ddict("Scenario 1", apc_1_pt2[1], apc_1_pt2[2], ddict)
add_to_ddict("Scenario 2", apc_2_pt2[1], apc_2_pt2[2], ddict)
add_to_ddict("Scenario 3", apc_3_pt2[1], apc_3_pt2[2], ddict)
add_to_ddict("Dianion", dianion_pt2[1], dianion_pt2[2], ddict)
add_to_ddict("Scenario 4", dianion_pt_chg_pt2[1], dianion_pt_chg_pt2[2], ddict)


df = pd.DataFrame(ddict)
df["\u0394(Qy-Qx)"] = df["Qy"] - df["Qx"]

print("In HARTREES")
print(df, "\n")

df["Qx"] *= physical_constants["hartree-inverse meter relationship"][0] * 1e-2
df["Qy"] *= physical_constants["hartree-inverse meter relationship"][0] * 1e-2
df["\u0394(Qy-Qx)"] *= (
    physical_constants["hartree-inverse meter relationship"][0] * 1e-2
)

print("\n\nIN WAVENUMBERS")
print(df.to_string(float_format="%.0f"), "\n")
df.to_csv("sa-3-mcscf_nevpt2.csv", index=False)


df["\u0394\u0394(Qy-Qx)"] = df["\u0394(Qy-Qx)"]
n_split = 3150
a_split = 2890
d_split = 2510


df.at[0, "\u0394\u0394(Qy-Qx)"] -= n_split
df.at[1, "\u0394\u0394(Qy-Qx)"] -= a_split
df.at[2, "\u0394\u0394(Qy-Qx)"] -= a_split
df.at[3, "\u0394\u0394(Qy-Qx)"] -= a_split
df.at[4, "\u0394\u0394(Qy-Qx)"] -= a_split
df.at[5, "\u0394\u0394(Qy-Qx)"] -= d_split
df.at[6, "\u0394\u0394(Qy-Qx)"] -= d_split

print(df.to_string(float_format="%.0f"))
