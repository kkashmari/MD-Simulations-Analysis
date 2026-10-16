# Molecular Dynamics Simulation Automation and Analysis

![Python](https://img.shields.io/badge/Python-Scientific%20Computing-3776AB?logo=python&logoColor=white)
![LAMMPS](https://img.shields.io/badge/LAMMPS-Molecular%20Dynamics-C0392B)
![Research](https://img.shields.io/badge/Status-Research%20Development-17365D)
![Access](https://img.shields.io/badge/Source-All%20Rights%20Reserved-555555)

## Overview

I developed this collection of Python workflows to automate molecular-dynamics simulations and analyze the thermal, mechanical, rheological, and transport properties of polymeric materials.

The repository includes tools for preparing LAMMPS simulation directories, generating customized input files, submitting HPC jobs, extracting simulation results, and calculating material properties from molecular-dynamics trajectories and log files.

My goal is to create reproducible workflows that reduce repetitive setup work and provide consistent analysis across multiple systems, temperatures, deformation directions, degrees of cure, and independent replicates.
`extract_shear_data.py` uses the `log` module distributed with Pizza.py
to read LAMMPS log files. Pizza.py must be installed or its directory
must be included in `PYTHONPATH`.

## Research areas

- Polymer molecular dynamics
- Thermoset and crosslinked-network simulations
- Mechanical-property prediction
- Thermal-property analysis
- Glass-transition-temperature estimation
- Viscoelastic and rheological analysis
- Green–Kubo transport-property calculations
- Automated LAMMPS workflows
- High-performance computing

## Workflow

```text
Molecular structure
        │
        ▼
LAMMPS system preparation
        │
        ▼
Crosslinking and equilibration
        │
        ├── Thermal simulations
        ├── Tensile deformation
        ├── Shear deformation
        ├── Oscillatory deformation
        └── Transport-property simulations
                 │
                 ▼
        Python post-processing
                 │
                 ▼
     Material properties and figures
