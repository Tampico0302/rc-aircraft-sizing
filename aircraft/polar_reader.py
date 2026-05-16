import numpy as np


def read_xfoil_polar(polar_file):
    alpha = []
    cl = []
    cd = []
    cm = []

    with open(polar_file, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            parts = line.split()

            if len(parts) < 5:
                continue

            try:
                alpha_i = float(parts[0])
                cl_i = float(parts[1])
                cd_i = float(parts[2])
                cm_i = float(parts[4])
            except ValueError:
                continue

            alpha.append(alpha_i)
            cl.append(cl_i)
            cd.append(cd_i)
            cm.append(cm_i)

    if len(alpha) < 4:
        raise RuntimeError(f"Not enough valid XFOIL polar points in {polar_file}")

    return {
        "alpha": np.array(alpha, dtype=float),
        "cl": np.array(cl, dtype=float),
        "cd": np.array(cd, dtype=float),
        "cm": np.array(cm, dtype=float),
    }