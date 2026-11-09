import re, shutil, subprocess, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
ENGINE = HERE / "engine"
L0 = np.arange(12.0, 20.5, 0.5)
LAM3 = [-0.35, -0.25, -0.15]
TAU = -0.25


def relax(cell):
    l0, lam3 = cell
    out = HERE / "relax" / f"l0={l0}_lam3={lam3}_tau={TAU}"
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = shutil.copytree(ENGINE / f"GradientDescent_{1 if l0.is_integer() else 2}l", Path(tmp) / "src")
        (src / "nr.h").write_text((src / "nr.h").read_text().replace("#define el_not 4", f"#define el_not {int(l0)}"))
        main = re.sub(r"double lambda3 = [^;]+;", f"double lambda3 = {lam3};", (src / "main.cpp").read_text())
        (src / "main.cpp").write_text(re.sub(r"const double tau = [^;]+;", f"const double tau = {TAU};", main))
        subprocess.run(["g++", "-std=c++0x", "-O3", "main.cpp", "-o", "main", f"-I{ENGINE}/wigxjpf-1.13/inc",
                        f"-I{ENGINE}/eigen-3.4.0", f"-L{ENGINE}/wigxjpf-1.13/lib", "-lwigxjpf", "-lm"], cwd=src, check=True)
        subprocess.run([src / "main"], cwd=out, check=True)


if __name__ == "__main__":
    with ProcessPoolExecutor(16) as pool:
        list(pool.map(relax, [(l0, lam3) for l0 in L0 for lam3 in LAM3]))
