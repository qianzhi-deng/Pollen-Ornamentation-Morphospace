import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
DATA = HERE.parent / "00_data"
names = pd.read_csv(DATA / "03_names" / "names.csv")
tips = set(re.findall(r"[(,]([^(),:;]+)", (DATA / "04_tree" / "tree.nwk").read_text()))

vector = pd.read_csv(DATA / "02_pollination" / "pollination.csv").merge(names).groupby("accepted").vector.agg(lambda s: s.iloc[0] if s.nunique() == 1 else None)

grains = pd.read_csv(HERE.parent / "01_morphospace" / "coordinates.csv").merge(pd.read_csv(DATA / "01_pollen" / "metadata.csv")).merge(names)
grains["vector"] = grains.accepted.map(vector)
grains["tip"] = grains.accepted.str.replace(" ", "_")
grains[grains.tip.isin(tips)].groupby("tip", as_index=False).agg(
    species=("accepted", "first"), family=("family", "first"), vector=("vector", "first"),
    I=("I", "mean"), D=("D", "mean"), P=("P", "mean")
).to_csv(HERE / "species.csv", index=False)
