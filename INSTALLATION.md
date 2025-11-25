# Installation Instructions

Set up the WFCRL environment on your system using conda. (Tested on Linux Mint 22.2 Zara)

## Prerequisites

- git
- conda

The following can already be installed on the system or can be installed into the conda environment
- cmake 
- fortran compiler
- c compiler

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ifpen/wfcrl-env.git
   cd wfcrl-env
   ```

2. **Create the conda environment**
    remove the cmake, gfortran_linux-64, or gxx_linux-64 if they are not needed
   ```bash
   conda env create --file environment.yaml
   ```
   

3. **Activate the environment**
   ```bash
   conda activate wfcrl
   ```

4. **Install the wfcrl package in development mode**
    This installs the package in an editable version in its pre-existing location
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

## Troubleshooting

- Ensure you have cmake installed before building the simulator
- If you encounter issues with gfortran, make sure the `gfortran_linux-64` package is properly installed via conda

