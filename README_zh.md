# 花粉纹饰形态空间

[English](README.md) | 中文

本仓库为[论文]([URL])的分析代码，使用时请引用：

> Deng Q, Ishihara K. 2026. Pollen Ornamentation Morphospace: Interpretable Quantification by Persistent Homology. *bioRxiv*. doi: 10.1101/[DOI]

如使用花粉网格或理论花粉，请同时引用以下原始来源；其他数据来源见论文。

- 花粉网格（3D Pollen Library）：Hayes AJ. 2017. Production of 3D printed scale models from microscope volume datasets for use in STEM education. *EMS Engineering Science Journal* 1: 002.
- 理论花粉：Radja A, Horsley EM, Lavrentovich MO, Sweeney AM. 2019. Pollen cell wall patterns form from modulated phases. *Cell* 176: 856–868.

## 1. 安装

Python 和 R 装在同一个 conda 环境 `morphospace` 中：

```bash
conda create -n morphospace -c conda-forge python=3.12 r-base=4.4 r-remotes c-compiler cxx-compiler \
  r-ape=5.8_1 r-caper=1.0.4 r-nlme=3.1_170 r-phytools=2.5_2 r-effsize=0.8.1 \
  r-ggplot2 r-gt r-rmarkdown r-rvest r-sf r-tidyr r-e1071 r-ff r-ipred r-rsqlite r-xtable
conda activate morphospace
pip install numpy==2.5.2 pandas==3.0.5 scipy==1.18.0 requests==2.34.2 trimesh==5.0.0 embreex==4.4.0 gudhi==3.13.0
Rscript -e 'options(repos = "https://cloud.r-project.org"); remotes::install_github(c("jinyizju/V.PhyloMaker2@7af3fb5", "matildabrown/rWCVP@77330c4", "matildabrown/rWCVPdata@65bed76"), upgrade = "never")'
```

理论花粉另需系统的 C++ 编译器（`g++`）和 `make`。

## 2. 数据

Radja et al. (2019) 的模型程序及其依赖需手动准备，在 `README.md` 所在的文件夹下运行：

```bash
mkdir -p 02_fabrication/engine
git clone https://github.com/asjaradja/PollenPhaseTransitionPaper.git /tmp/radja && git -C /tmp/radja checkout 428056b
cp -R /tmp/radja/PhaseDiagramCalculations/GradientDescent_1l /tmp/radja/PhaseDiagramCalculations/GradientDescent_2l 02_fabrication/engine/
curl -L https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz | tar xz -C 02_fabrication/engine
curl -L https://fy.chalmers.se/subatom/wigxjpf/wigxjpf-1.13.tar.gz | tar xz -C 02_fabrication/engine
make -C 02_fabrication/engine/wigxjpf-1.13
```

## 3. 结构

```
pipeline.py               ρ 场 → 带符号持续度 → 形态空间坐标 (I, D, P)
00_data/                  数据准备
├── 01_pollen/            花粉网格（3D Pollen Library）
├── 02_pollination/       传粉方式（EcoFlora）
├── 03_names/             接受名（WCVP）
└── 04_tree/              系统发育树（GBOTB）
01_morphospace/           真实花粉：球度、坐标（I、D、P）
02_fabrication/           理论花粉：Radja 模型、坐标、波数与刺数预测
03_function/              传粉方式：物种表、虫媒与风媒比较
04_phylogeny/             菊科：系统发育信号、祖先状态
```

## 4. 运行

以下命令都在 `README.md` 所在的文件夹下运行。

先激活环境：

```bash
conda activate morphospace
export LC_ALL=en_US.UTF-8
```

数据准备：下载花粉网格，检索传粉方式，把物种名统一为 WCVP 接受名，建系统树。

```bash
python 00_data/01_pollen/01_rawdata.py
python 00_data/02_pollination/pollination.py
Rscript 00_data/03_names/names.R
Rscript 00_data/04_tree/tree.R
```

真实花粉：计算球度，再对网格投射射线，计算形态空间坐标 (I, D, P)。

```bash
python 01_morphospace/01_sphericity.py
python 01_morphospace/02_coordinates.py
```

理论花粉：运行 Radja 的模型，计算形态空间坐标 (I, D, P)，由 D、P 预测波数与刺数。`01_relax.py` 默认同时运行 16 个进程，核数不足时可修改其中的 `ProcessPoolExecutor(16)`。

```bash
python 02_fabrication/01_relax.py
python 02_fabrication/02_coordinates.py
python 02_fabrication/03_recovery.py
```

传粉方式：整理物种表，比较虫媒与风媒。

```bash
python 03_function/01_assemble.py
Rscript 03_function/02_stats.R
```

菊科：估计系统发育信号与祖先状态。

```bash
Rscript 04_phylogeny/01_signal.R
Rscript 04_phylogeny/02_ancestral.R
```
