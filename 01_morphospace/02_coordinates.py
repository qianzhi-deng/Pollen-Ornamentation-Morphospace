import sys
from pathlib import Path

import numpy as np, pandas as pd, trimesh
from trimesh.ray.ray_pyembree import RayMeshIntersector

HERE = Path(__file__).parent
sys.path.append(str(HERE.parent)); from pipeline import DIRS, ICO, barcode, coordinates

SRC, OUT = HERE.parent / "00_data" / "01_pollen", HERE / "mesh" / "angiosperm"


def envelope(mesh):
    c = mesh.center_mass
    hits, ray, _ = RayMeshIntersector(mesh).intersects_location(np.tile(c, (len(DIRS), 1)), DIRS, multiple_hits=True)
    rho = np.full(len(DIRS), np.nan)
    np.fmax.at(rho, ray, np.linalg.norm(hits - c, axis=1))
    return rho


OUT.mkdir(parents=True, exist_ok=True)
grains = pd.read_csv(SRC / "metadata.csv").merge(pd.read_csv(HERE / "sphericity.csv"))
rows = []
for g in grains[(grains.seed_group == "Angiosperm") & (grains.sphericity > 0.7)].itertuples():
    name = f"{g.species.replace(' ', '_')}_{g.nih3d_id}.stl"
    rho = envelope(trimesh.load(SRC / "pollen" / "angiosperm" / name))
    trimesh.Trimesh(rho[:, None] * DIRS, ICO.faces).export(OUT / name)
    rows.append({"nih3d_id": g.nih3d_id, **coordinates(*barcode(rho))})
pd.DataFrame(rows).to_csv(HERE / "coordinates.csv", index=False)
