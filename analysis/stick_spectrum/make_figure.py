import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.constants import physical_constants


def get_reference_data():
    filename = "ProtoporphyrinUVVis.txt"
    df = pd.read_csv(filename, sep="\t")
    df.fillna(0, inplace=True)
    df.columns = ["M cm^-1", "M Abs", "D cm^-1", "D Abs"]
    return df


if __name__ == "__main__":
    import subprocess
    from scipy.constants import physical_constants

    #
    # Get Data
    #
    df_ref = get_reference_data()
    df_pyscf = pd.read_csv("../stable_sa-3-mcscf.csv")
    df_orca = pd.read_csv("../orca_data.csv")

    ev_2_cm_1 = physical_constants["electron volt-inverse meter relationship"][0] * 1e-2
    mono_cm_1 = np.array([2.0982, 2.2845]) * ev_2_cm_1
    di_cm_1 = np.array([2.0646, 2.2353]) * ev_2_cm_1

    #
    # Plotting
    #
    plt.figure()
    sns.set_style("darkgrid")
    sns.set_palette("muted")
    bar_height = 0.002
    filename = "stick_spectrum.pdf"

    # Monoanion
    plt.subplot(2, 1, 1)
    plt.title("Monoanion Absorption")
    s_i = np.argsort(df_ref["M cm^-1"])
    plt.plot(df_ref["M cm^-1"][s_i], df_ref["M Abs"][s_i], c="k", label="Expt.")
    plt.bar(mono_cm_1, [bar_height] * 2, label="TDDFT", width=120)
    plt.bar(
        df_pyscf.iloc[1, 1:3].values,
        [bar_height * 1.1] * 2,
        label="PySCF NEVPT2",
        width=120,
    )
    plt.bar(
        df_orca.iloc[1, 1:3].values, [bar_height] * 2, label="ORCA NEVPT2", width=120,
    )
    plt.xlim((14000, 21000))
    plt.ylabel("Abs. (arb.)")
    plt.legend(loc="upper right")

    # Dianion
    plt.subplot(2, 1, 2)
    plt.title("Dianion Absorption")
    plt.plot(df_ref["D cm^-1"], df_ref["D Abs"], c="k", label="Expt.")
    plt.bar(di_cm_1, [bar_height] * 2, label="TDDFT", width=120)

    plt.bar(
        df_pyscf.iloc[5, 1:3].values,
        [bar_height * 1.1] * 2,
        label="PySCF NEVPT2",
        width=120,
    )
    plt.bar(
        df_orca.iloc[5, 1:3].values, [bar_height] * 2, label="ORCA NEVPT2", width=120,
    )
    plt.xlim((14000, 21000))
    plt.ylabel("Abs. (arb.)")
    plt.xlabel("Energy cm$^{-1}$")

    plt.tight_layout()
    plt.savefig(filename)

    #
    # Convert to TIFF
    #

    subprocess.run(["convert", filename, f"{filename[:4]}.tiff"])

