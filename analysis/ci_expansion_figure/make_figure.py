import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


def parse_sa_output(filename: str, spin=0, nelecas=4, trev=False) -> dict:
    """Hardcoded for a 4 orbital active space"""

    start_tok = "** Largest CI components **"
    end_tok = " ** Mulliken pop on meta-lowdin orthogonal AOs  **"
    start_tok_found = False
    end_tok_found = False

    ci_info = {}
    output_gen = (line for line in open(filename))
    while not end_tok_found:
        # Search file
        next_line = next(output_gen)

        # # Get CAS space
        # if "CAS" in next_line and "ncore =" in next_line:
        #     lsplit = next_line.split()
        #     ncore = int(lsplit[5].replace(",", ""))  # in 1-based indexing
        #     cas_mo = list(range(ncore, ncore + 4))  # in 0-based indexing
        #     print("CAS MO indices (0-based indexing) =", cas_mo)
        #     ci_info["cas_mo"] = cas_mo
        #     ci_info["cas_mo_energies"] = []

        # # Get CAS MO Energies
        # if "<i|F|i>" in next_line:
        #     if int(next_line.split()[2]) - 1 in ci_info["cas_mo"]:
        #         ci_info["cas_mo_energies"].append(float(next_line.split()[-1]))
        #         # print(ci_info["cas_mo_energies"])

        # Collect data
        if start_tok in next_line:
            start_tok_found = True

            # Iterate through data
            current_key = ""
            while not end_tok_found:
                next_line = next(output_gen)
                if end_tok in next_line:
                    end_tok_found = True
                    # fmt: off
                    ci_info[current_key]["ci"] = np.array(ci_info[current_key]["ci"])
                    ci_info[current_key]["a_occ"] = np.array(ci_info[current_key]["a_occ"])
                    ci_info[current_key]["b_occ"] = np.array(ci_info[current_key]["b_occ"])
                    # fmt: on
                    break
                else:
                    lsplit = next_line.strip().replace("[", "").replace("]", "").split()
                    if "state" in next_line:
                        if current_key != "":
                            # Wrap up old dictionary
                            # fmt: off
                            ci_info[current_key]["ci"] = np.array(ci_info[current_key]["ci"])
                            ci_info[current_key]["a_occ"] = np.array(ci_info[current_key]["a_occ"])
                            ci_info[current_key]["b_occ"] = np.array(ci_info[current_key]["b_occ"])
                            # fmt: on

                        # Create State Dictionary
                        key = lsplit[4] + " " + lsplit[5]
                        ci_info[key] = {}
                        ci_info[key]["ci"] = []
                        ci_info[key]["a_occ"] = []
                        ci_info[key]["b_occ"] = []

                        current_key = key

                    else:
                        nalpha = int((nelecas - spin) / 2)
                        ci = float(lsplit[-1])

                        if trev:
                            if np.isclose(ci, ci_info[key]["ci"], rtol=1e-4).any():
                                idx = np.flatnonzero(
                                    np.isclose(ci, ci_info[key]["ci"], rtol=1e-4)
                                )[0]
                                ci_info[key]["ci"][idx] *= np.sqrt(2)
                            else:
                                a_occ = [int(occ) for occ in lsplit[0:nalpha]]
                                b_occ = [int(occ) for occ in lsplit[nalpha:nelecas]]
                                ci_info[key]["ci"].append(ci)
                                ci_info[key]["a_occ"].append(a_occ)
                                ci_info[key]["b_occ"].append(b_occ)
                        else:
                            a_occ = [int(occ) for occ in lsplit[0:nalpha]]
                            b_occ = [int(occ) for occ in lsplit[nalpha:nelecas]]
                            ci_info[key]["ci"].append(ci)
                            ci_info[key]["a_occ"].append(a_occ)
                            ci_info[key]["b_occ"].append(b_occ)

    # Sort MO occ if MOs aren't in order
    # in_order = (np.arange(4) == np.argsort(ci_info["cas_mo_energies"])).all()
    # if not in_order:
    #     print("Sorting MO")
    #     si = np.argsort(ci_info["cas_mo_energies"])
    print(ci_info)
    # print(in_order)
    # exit(0)
    return ci_info


def make_det_diag(coeff, mask_a, mask_b, norbs, x_center=0):
    levels = list(range(norbs))
    x = np.linspace(-1, 1, len(levels)) + x_center
    arrow_height = 0.5
    arrow_lw = 5
    arrow_xshift = 0.3
    arrow_head_width = 0.05
    arrow_head_length = 0.03
    arrow_length_tot = arrow_head_length + arrow_height

    # plt.figure()
    # ax = plt.axes()
    ax = plt.gca()
    for i in range(len(levels)):
        # Plot energy levels
        plt.plot(x, [levels[i]] * len(levels), c="k", lw=2)

        if i in mask_a:
            ax.arrow(
                x_center - arrow_xshift,
                levels[i] - arrow_length_tot / 2,
                0,
                arrow_height,
                lw=arrow_lw,
                head_width=arrow_head_width,
                head_length=arrow_head_length,
                fc="k",
                ec="k",
            )

        if i in mask_b:
            ax.arrow(
                x_center + arrow_xshift,
                levels[i] + arrow_length_tot / 2,
                0,
                -arrow_height,
                lw=arrow_lw,
                head_width=arrow_head_width,
                head_length=arrow_head_length,
                fc="k",
                ec="k",
            )

    # Axis ticks and labels
    plt.gca().get_xaxis().set_visible(False)

    # Add Ket Symbol
    plt.text(x_center, -1, f"${coeff:.2f}$", ha="center", va="center", fontsize=20)


def make_ci_wfn_diagram(
    state: dict,
    filename: str,
    norbs: int,
    figsize: tuple = (8, 6),
    x_spacing: float = 3,
    y_label_pos: float = -2,
):
    """Create a diagram for the most important configurations in a CI wavefunction.

    Parameters
    ----------
    state : dict
        A dict with data about the state. Must have keys, "ci", "a_occ", and "b_occ".
    filename : str
        Filename to save figure to.
    norbs : int
        Size of active space or number of orbitals to consider.
    figsize : tuple, optional
        Change figuresize, adjust this when plotting more than 4-6 configurations, by default (8, 6).
    x_spacing : float, optional
        Change the spacing between determinants, try adjusting figsize first, by default 3.
    y_label_pos : float, optional
        Sets position of y-axis labels, try adjusting figsize first, by default -2.

    Raises
    ------
    AssertionError
        Checks that state["ci"] and state["a_occ"] are the same length.

    Examples
    --------
    >>> make_ci_wfn_diagram(mono_state_0, "monoanion_S_0", 4)
    """
    ci = state["ci"]
    a_occ = state["a_occ"]
    b_occ = state["b_occ"]

    if ci.size != a_occ.shape[0]:
        raise AssertionError("Data arrays not the same size")

    plt.figure(figsize=figsize)

    x_center = 0
    for i, ci_i in enumerate(ci):
        make_det_diag(ci_i ** 2, a_occ[i], b_occ[i], norbs, x_center)
        x_center += x_spacing

    # Labels

    plt.text(
        y_label_pos,
        1.5,
        "Configuration\nOccupations",
        ha="center",
        va="center",
        fontsize=20,
        rotation=90,
    )
    plt.text(
        y_label_pos, -1, "Weight", ha="center", va="center", fontsize=20, rotation=90
    )

    plt.ylim(-1, 4)
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        "{}.png".format(filename),
        dpi=900,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()


def make_all_diagrams(mcscf_output, output_base, ncas, trev=False):
    ci_info = parse_sa_output(mcscf_output, trev=trev)
    for k, v in ci_info.items():
        if k not in ["state 0", "state 1", "state 2"]:
            print(f"Skipping {k}")
            continue
        print(k, v)
        print("State {}".format(k[-1]))
        print(v["ci"].size)
        figsize = (v["ci"].size // 2 * 4, 6)
        print(figsize)
        # exit(0)
        make_ci_wfn_diagram(
            v, output_base + "S_{}".format(k[-1]), ncas, figsize=figsize
        )


if __name__ == "__main__":
    import os
    import subprocess

    path_base = "/home/jasm3285/projects/rs_projects/ppix_final"
    make_all_diagrams(
        os.path.join(path_base, "dianion/_logs/_sa_mcscf.out"),
        "dianion_",
        4,
        trev=True,
    )

    make_all_diagrams(
        os.path.join(path_base, "anion/_logs/_sa_mcscf.out"), "anion_", 4, trev=True,
    )

    make_all_diagrams(
        os.path.join(path_base, "scenario4/_logs/_sa_mcscf.out"),
        "scenario4_",
        4,
        trev=True,
    )

    make_all_diagrams(
        os.path.join(path_base, "scenario1/_logs/_sa_mcscf.out"),
        "scenario1_",
        4,
        trev=True,
    )

    make_all_diagrams(
        os.path.join(path_base, "scenario2/_logs/_sa_mcscf.out"),
        "scenario2_",
        4,
        trev=True,
    )

    make_all_diagrams(
        os.path.join(path_base, "scenario3/_logs/_sa_mcscf.out"),
        "scenario3_",
        4,
        trev=True,
    )

    # for f in os.listdir():
    #     if f.endswith(".pdf"):
    #         tiff_name = f"{f[:-4]}.tiff"
    #         print(f"{f} {tiff_name}")
    #         subprocess.run(["convert", f"{f}", f"{tiff_name}"])
    #         os.remove(f)
