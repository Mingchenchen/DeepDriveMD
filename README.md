# DeepDriveMD
Deep-Learning Driven Adaptive Molecular Simulations for Protein Folding

Implementation of: https://arxiv.org/pdf/1909.07817.pdf

Project location: https://github.com/braceal/DeepDriveMD.git

# Instructions

Initial setup on Summit https://www.olcf.ornl.gov/summit/
```
git clone https://github.com/braceal/DeepDriveMD.git
cd DeepDriveMD/

module load python/3.7.0
conda env create python=3.7 -p ./conda-env -f environment.yml
conda activate ./conda-env
conda install -p ./conda-env -c omnia openmm-setup
```

This project uses openmm for molecular dynamics simulations which requires anaconda to install.
First update your conda environment:
```
conda update conda
```
Then install openmm:
```
conda install -c omnia openmm-setup
```
