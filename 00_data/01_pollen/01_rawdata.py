from pathlib import Path

import pandas as pd, requests

HERE = Path(__file__).parent
HEADERS = {"User-Agent": "pollen_ornamentation_morphospace_research"}

for r in pd.read_csv(HERE / "metadata.csv").itertuples():
    entry = requests.get(f"https://3d.nih.gov/api/entries/{r.nih3d_id}", headers=HEADERS, timeout=30).json()
    sub = max((s for s in entry["submissions"] if int(s["version"]) == int(r.doi[-1])), key=lambda s: s["version"])
    stl = next(f for run in sub["workflowRuns"] for f in run["outputFiles"] if f["fileFormat"] == "STL")
    mesh = requests.get("https://3d.nih.gov/api/download", params={"submissionId": sub["submissionId"], "fileIds": stl["fileId"]},
                        headers=HEADERS, timeout=300).content
    dst = HERE / "pollen" / r.seed_group.lower() / f"{r.species.replace(' ', '_')}_{r.nih3d_id}.stl"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(mesh)
