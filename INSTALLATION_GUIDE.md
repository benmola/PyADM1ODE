# Installation Guide for PyADM1ODE

This guide provides step-by-step instructions for setting up the environment to run the PyADM1ODE simulation.

## Prerequisites

- **Anaconda or Miniconda**: Ensure you have Anaconda or Miniconda installed on your system.
- **Windows OS**: This project relies on `.dll` files and `pythonnet`, which are best supported on Windows.

## Step-by-Step Installation

### 1. Create a Conda Environment

It is highly recommended to use a dedicated Conda environment to manage dependencies and avoid conflicts.

```bash
conda create -n PyADM1ODE python=3.11
conda activate PyADM1ODE
```

### 2. Install Dependencies

Install the required Python packages.

```bash
pip install numpy pandas scipy matplotlib
```

### 3. Install Python.NET and Runtime

This is the most critical step. The project uses `pythonnet` to interface with C# DLLs.

**Important:**
- Install `pythonnet` using `pip`.
- Install `vs2015_runtime` using `conda` (required for some DLLs).

```bash
pip install pythonnet
conda install anaconda::vs2015_runtime
```

### 4. Verify Installation

Check that `pythonnet` is correctly installed and that there are no conflicting packages.

```bash
pip list
```

Ensure `pythonnet` is listed.

> [!WARNING]
> **Do NOT install the `clr` package.**
> The `clr` package on PyPI is different and conflicts with `pythonnet`. If you see `clr` in your `pip list`, uninstall it immediately:
> ```bash
> pip uninstall clr
> ```

## Running the Simulation

Once the environment is set up, you can run the main simulation script:

```bash
python main.py
```

## Troubleshooting

### `AttributeError: module 'clr' has no attribute 'AddReference'`

**Cause:** The `clr` package is installed and shadowing `pythonnet`.
**Solution:** Uninstall `clr` and ensure `pythonnet` is installed.

```bash
pip uninstall clr
pip install pythonnet
```

### `ModuleNotFoundError: No module named 'PyADM1'`

**Cause:** You are running the script from outside the project directory.
**Solution:** Navigate to the project directory before running the script.

```bash
cd path/to/PyADM1ODE
python main.py
```
