from pathlib import Path

import numpy as np, pandas as pd, trimesh

HERE = Path(__file__).parent

rows = []
for f in sorted((HERE.parent / "00_data" / "01_pollen" / "pollen").glob("*/*.stl")):
    mu = np.linalg.eigvalsh(np.cov(trimesh.load(f).vertices.T))
    rows.append({"nih3d_id": f.stem.split("_")[-1], "sphericity": np.sqrt(mu[0] / mu[-1])})
pd.DataFrame(rows).to_csv(HERE / "sphericity.csv", index=False)
