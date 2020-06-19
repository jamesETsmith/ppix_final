import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.constants import physical_constants


def add_unit_conversion(func):
    """A function wrapper that adds the capability to convert from Hartrees to several other units.
    
    Parameters
    ----------
    func : function
        Function to add unit conversion capability to.
    """

    def wrapper(*args, **kwargs):
        if "units" not in kwargs:
            return func(*args, **kwargs)
        elif kwargs.get("units") == "cm^-1":
            vals = func(*args, **kwargs)
            return (
                vals
                * physical_constants["hartree-inverse meter relationship"][0]
                * 1e-2
            )
        elif kwargs.get("units") == "eV":
            vals = func(*args, **kwargs)
            return vals * physical_constants["Hartree energy in eV"][0]

    return wrapper


@add_unit_conversion
def get_casscf_data(
    filename: str = "anion/ccpvdz_sa-5-cas_4e_4o/energies/SA-5-CASSCF(4,4).txt",
    **kwargs,
):
    np.set_printoptions(precision=3)
    energies_ha = np.loadtxt(filename)
    return energies_ha - energies_ha.min()


@add_unit_conversion
def get_nevpt2_data(base_path: str, n_states: int = 5, **kwargs):
    np.set_printoptions(precision=3)

    energies_ha = []
    for i in range(n_states):
        filename = os.path.join(base_path, f"NEVPT2-{i}.txt")
        energies_ha.append(np.loadtxt(filename))
    energies_ha = np.array(energies_ha)
    return energies_ha - energies_ha.min()
