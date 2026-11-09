import numpy as np, trimesh, gudhi

ICO = trimesh.creation.icosphere(subdivisions=6)
DIRS = ICO.vertices
EDGES = np.asarray(ICO.edges_unique, dtype=np.int64)

def barcode(rho):
    rho = rho / np.nanmax(rho)
    edges = EDGES[np.isfinite(rho)[EDGES].all(1)]
    verts = np.unique(edges)
    p = []
    for vals in (rho, -rho):
        st = gudhi.SimplexTree()
        st.insert_batch(verts[None], vals[verts])
        st.insert_batch(edges.T, vals[edges].max(1))
        st.compute_persistence()
        bars = st.persistence_intervals_in_dimension(0)
        bars = bars[np.isfinite(bars[:, 1])]
        p.append(bars[:, 1] - bars[:, 0])
    return np.concatenate(p), np.r_[-np.ones(len(p[0])), np.ones(len(p[1]))]


def coordinates(p, sig):
    pi = p / p.sum()
    return {
        "I": float(np.log(p.mean())),
        "D": float(-np.sum(pi * np.log(pi))),
        "P": float(np.arctanh(np.sum(pi * sig))),
    }
