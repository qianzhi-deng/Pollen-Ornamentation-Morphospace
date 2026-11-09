# Pollen Ornamentation Morphospace

English | [中文](README_zh.md)

Analysis code for [the paper]([URL]). When using this repository, please cite:

> Deng Q, Ishihara K. 2026. Pollen Ornamentation Morphospace: Interpretable Quantification by Persistent Homology. *bioRxiv*. doi: 10.1101/[DOI]

If you use the pollen meshes or the theoretical pollen, please also cite the original sources below; the other data sources are cited in the paper.

- Pollen meshes (3D Pollen Library): Hayes AJ. 2017. Production of 3D printed scale models from microscope volume datasets for use in STEM education. *EMS Engineering Science Journal* 1: 002.
- Theoretical pollen: Radja A, Horsley EM, Lavrentovich MO, Sweeney AM. 2019. Pollen cell wall patterns form from modulated phases. *Cell* 176: 856–868.

## 1. Installation

Python and R are installed in a single conda environment, `morphospace`:

```bash
conda create -n morphospace -c conda-forge python=3.12 r-base=4.4 r-remotes c-compiler cxx-compiler \
  r-ape=5.8_1 r-caper=1.0.4 r-nlme=3.1_170 r-phytools=2.5_2 r-effsize=0.8.1 \
  r-ggplot2 r-gt r-rmarkdown r-rvest r-sf r-tidyr r-e1071 r-ff r-ipred r-rsqlite r-xtable
conda activate morphospace
pip install numpy==2.5.2 pandas==3.0.5 scipy==1.18.0 requests==2.34.2 trimesh==5.0.0 embreex==4.4.0 gudhi==3.13.0
Rscript -e 'options(repos = "https://cloud.r-project.org"); remotes::install_github(c("jinyizju/V.PhyloMaker2@7af3fb5", "matildabrown/rWCVP@77330c4", "matildabrown/rWCVPdata@65bed76"), upgrade = "never")'
```

The theoretical pollen additionally requires a system C++ compiler (`g++`) and `make`.

## 2. Data

The model program of Radja et al. (2019) and its dependencies must be prepared by hand; run the following from the folder containing `README.md`:

```bash
mkdir -p 02_fabrication/engine
git clone https://github.com/asjaradja/PollenPhaseTransitionPaper.git /tmp/radja && git -C /tmp/radja checkout 428056b
cp -R /tmp/radja/PhaseDiagramCalculations/GradientDescent_1l /tmp/radja/PhaseDiagramCalculations/GradientDescent_2l 02_fabrication/engine/
curl -L https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz | tar xz -C 02_fabrication/engine
curl -L https://fy.chalmers.se/subatom/wigxjpf/wigxjpf-1.13.tar.gz | tar xz -C 02_fabrication/engine
make -C 02_fabrication/engine/wigxjpf-1.13
```

## 3. Structure

```
pipeline.py               ρ field → signed persistence → morphospace coordinates (I, D, P)
00_data/                  data preparation
├── 01_pollen/            pollen meshes (3D Pollen Library)
├── 02_pollination/       pollination modes (EcoFlora)
├── 03_names/             accepted names (WCVP)
└── 04_tree/              phylogenetic tree (GBOTB)
01_morphospace/           real pollen: sphericity, coordinates (I, D, P)
02_fabrication/           theoretical pollen: Radja model, coordinates, wavenumber and spine prediction
03_function/              pollination mode: species table, insect vs wind comparison
04_phylogeny/             Asteraceae: phylogenetic signal, ancestral states
```

## 4. Running

Run all commands from the folder containing `README.md`.

Activate the environment:

```bash
conda activate morphospace
export LC_ALL=en_US.UTF-8
```

Data preparation: download the pollen meshes, query the pollination modes, standardise species names to WCVP accepted names and build the phylogeny.

```bash
python 00_data/01_pollen/01_rawdata.py
python 00_data/02_pollination/pollination.py
Rscript 00_data/03_names/names.R
Rscript 00_data/04_tree/tree.R
```

Real pollen: compute sphericity, then cast rays on the meshes to compute the morphospace coordinates (I, D, P).

```bash
python 01_morphospace/01_sphericity.py
python 01_morphospace/02_coordinates.py
```

Theoretical pollen: run the model of Radja et al., compute the morphospace coordinates (I, D, P) and predict wavenumber and spine number from D and P. `01_relax.py` runs 16 processes in parallel by default; on machines with fewer cores, change `ProcessPoolExecutor(16)` in that file.

```bash
python 02_fabrication/01_relax.py
python 02_fabrication/02_coordinates.py
python 02_fabrication/03_recovery.py
```

Pollination mode: assemble the species table and compare insect- and wind-pollinated species.

```bash
python 03_function/01_assemble.py
Rscript 03_function/02_stats.R
```

Asteraceae: estimate phylogenetic signal and ancestral states.

```bash
Rscript 04_phylogeny/01_signal.R
Rscript 04_phylogeny/02_ancestral.R
```
