# Installation Instructions

This guide will help you set up the WFCRL environment on your system using conda. (Tested on Linux Mint 22.2 Zara)

## Prerequisites

- Git
- Conda/Miniconda
- CMake (`sudo apt install cmake` on Ubuntu/Debian)

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ifpen/wfcrl-env.git
   cd wfcrl-env
   ```

2. **Create the conda environment**
   ```bash
   conda env create --file environment.yaml
   ```
   
   The environment includes the following dependencies:
   - gymnasium 0.29.*
   - mpi4py 3.1.*
   - numpy 1.26.*
   - pandas 2.2.*
   - pettingzoo 1.24.*
   - pyYAML 6.0.*
   - FLORIS 3.5.*
   - ipykernel
   - seaborn
   - gfortran_linux-64
   - pip
   - tensorboard-data-server 0.6.*
   - tensorboard-plugin-wit 1.8.*
   - tensorboard 2.11.*
   - tyro 0.8.*
   - wandb
   - python-dotenv

3. **Activate the environment**
   ```bash
   conda activate wfcrl
   ```

4. **Install the package in development mode**
   ```bash
   pip install -e .
   ```

5. **Build the FastFarm simulator**
   ```bash
   wfcrl-simulator fastfarm
   ```
   
   > **Note**: This step requires CMake to be installed on your system.

6. **Test the installation**
   ```bash
   python examples/example_fastfarm.py
   ```

## Environment File Structure

The `environment.yaml` file defines a conda environment named `wfcrl` with all necessary dependencies for wind farm control reinforcement learning applications.

## Troubleshooting

- Ensure you have CMake installed before building the simulator
- If you encounter issues with gfortran, make sure the `gfortran_linux-64` package is properly installed via conda
- For any build issues, check that all dependencies are correctly installed in the conda environment