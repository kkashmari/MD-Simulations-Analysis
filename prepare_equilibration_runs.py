# -*- coding: utf-8 -*-
"""
Creating LAMMPS script and directories for each degree of cure and run equilibration simulations
Author: Khatereh Kashmari
"""
from pathlib import Path
import shutil
import subprocess

simulation_folder_pattern = "L10_Replicate_*_*K"	#Folder names from crosslinking simulations

output_file_pattern = "poly_rep_*_time_*ps_pxld_*.data"	#Output files from crosslinking simulations

Equilibration_lammps_template = "Equilibration_Simulation_template.in"	#LAMMPS Equilibration Templates
Equilibration_lammps_output = "PolyL10_Equilibrated.in"	# generated Customized LAMMPS script 

Results_Folder = Path("Equilibration_Runs")	#output folder
pbs_file = "job.pbs"

submit_jobs = True #Change to False if you dont want to submit the job automatically


if not Path(Equilibration_lammps_template).is_file():
    raise FileNotFoundError(f"Missing {Equilibration_lammps_template}")

if not Path(pbs_file).is_file():
    raise FileNotFoundError(f"Missing {pbs_file}")

Results_Folder.mkdir(exist_ok=True)

template_script = Path(Equilibration_lammps_template).read_text()

#Loop over existing simulation_folder_pattern 
for sim_dir in Path(".").glob(simulation_folder_pattern):

    if not sim_dir.is_dir():
        continue

    for data_file in sim_dir.glob(output_file_pattern):

        structure_name = data_file.stem		# Generating new folders
        run_dir = Results_Folder / sim_dir.name / structure_name
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"Creating Equilibration run: {run_dir}")

        input_data = run_dir / data_file.name	#inputs from crosslinking sims
        shutil.copy(data_file, input_data)
        shutil.copy(pbs_file, run_dir / pbs_file)	#Pbs files


        Equilibration_analysis = template_script.replace("$DATAFILE$", data_file.name)	#LAMMPS script for each run
        (run_dir / Equilibration_lammps_output).write_text(Equilibration_analysis)

        if submit_jobs:
            subprocess.run(["qsub", pbs_file], cwd=run_dir, check=True)

print("\nAll Equilibration analysis folders created.")
