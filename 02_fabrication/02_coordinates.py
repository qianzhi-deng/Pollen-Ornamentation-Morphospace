import sys
from pathlib import Path

import numpy as np, pandas as pd
from scipy.special import sph_harm_y

HERE = Path(__file__).parent
sys.path.append(str(HERE.parent)); from pipeline import DIRS, barcode, coordinates

AZ, POL = np.arctan2(DIRS[:, 1], DIRS[:, 0]), np.arccos(DIRS[:, 2])


def synthesize(l0, cms):
    rho, row = np.zeros(len(DIRS)), 0
    for l in [int(l0)] if l0.is_integer() else [int(l0), int(l0) + 1]:
        c = cms[row:row + l + 1, 0] + 1j * cms[row:row + l + 1, 1]
        rho += np.r_[1.0, np.full(l, 2.0)] @ (c[:, None] * sph_harm_y(l, np.arange(l + 1)[:, None], POL, AZ)).real
        row += l + 1
    return rho


rows = []
for cell in sorted((HERE / "relax").glob("l0=*")):
    p = {k: float(v) for k, v in (kv.split("=") for kv in cell.name.split("_"))}
    rows.append({**p, **coordinates(*barcode(synthesize(p["l0"], np.loadtxt(cell / "endcms.txt"))))})
pd.DataFrame(rows).to_csv(HERE / "coordinates.csv", index=False)
