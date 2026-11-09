import re
from pathlib import Path

import pandas as pd, requests

HERE = Path(__file__).parent

rows = []
for vector in ("insect", "wind"):
    html = requests.post("http://ecoflora.org.uk/show_plantlist.php", data={"char_no": "5.15", "char_value": vector},
                         headers={"User-Agent": "pollen_ornamentation_morphospace_research"}, timeout=60).text
    rows += [(" ".join(name.split()), vector) for name in re.findall(r"<li>([^<]+)", html)]
pd.DataFrame(rows, columns=["species", "vector"]).drop_duplicates().to_csv(HERE / "pollination.csv", index=False)
