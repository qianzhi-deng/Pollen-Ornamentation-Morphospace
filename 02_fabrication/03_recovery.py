from pathlib import Path

import numpy as np, pandas as pd
from scipy.stats import entropy

HERE = Path(__file__).parent
h = lambda P: entropy([(1 + np.tanh(P)) / 2, (1 - np.tanh(P)) / 2])

theory = pd.read_csv(HERE / "coordinates.csv")
theory["predicted_without_h"] = np.sqrt(np.pi * np.exp(theory.D))
theory["predicted_with_h"] = np.sqrt(np.pi * np.exp(theory.D - h(theory.P)))
theory["error_without_h"] = theory.predicted_without_h / theory.l0 - 1
theory["error_with_h"] = theory.predicted_with_h / theory.l0 - 1
theory.drop(columns=["tau", "I", "D", "P"]).to_csv(HERE / "recovery_theory.csv", index=False)

real = pd.read_csv(HERE / "spines.csv").merge(pd.read_csv(HERE.parent / "01_morphospace" / "coordinates.csv"))
real["predicted_without_h"] = np.exp(real.D)
real["predicted_with_h"] = np.exp(real.D - h(real.P))
real["error_without_h"] = real.predicted_without_h / real.spines - 1
real["error_with_h"] = real.predicted_with_h / real.spines - 1
real.drop(columns=["I", "D", "P"]).to_csv(HERE / "recovery_real.csv", index=False)
