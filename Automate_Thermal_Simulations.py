# -*- coding: utf-8 -*-
"""
Creating LAMMPS script and directories for each equilibrated degree of cure and run Tg simulations
Author: Khatereh Kashmari

"""

from pathlib import Path
import shutil
import subprocess


simulation_folder_pattern = "PolyL10_rep_*s_pxld_*_Equilibrated"		#Folder names from equilibration simulations
output_file_pattern = "PolyL10*_p*_Equilibrated.data"	#Outputs from equilibration simulations

Tg_results = Path("Tg_Simulation_Runs")

lammps_template_script = "Tg_Simulations.in" #LAMMPS script template
New_lammps_output = "PolyL10_Tg_Simulations_100K_700K.in"	# generated LAMMPS script

pbs_file = "job.pbs"
submit_jobs = True


#Check if all the required files exist

if not Path(lammps_template_script).is_file():
    raise FileNotFoundError(f"Missing {lammps_template_script}")

if not Path(pbs_file).is_file():
    raise FileNotFoundError(f"Missing {pbs_file}")

Tg_results.mkdir(exist_ok=True)

Tg_template_script = Path(lammps_template_script).read_text()

#------------------------------------------------

#Generating new folders

for sim_dir in Path(".").glob(simulation_folder_pattern):

    if not sim_dir.is_dir():
        continue

    for data_file in sim_dir.glob(output_file_pattern):

        structure_name = data_file.stem

        run_dir = Tg_results / sim_dir.name / structure_name
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"Creating Tg run: {run_dir}")

        Input_data = run_dir / data_file.name
        shutil.copy(data_file, Input_data)
        shutil.copy(pbs_file, run_dir / pbs_file)

        lammps_Tg_script = Tg_template_script.replace("$DATAFILE$", data_file.name)
        (run_dir / New_lammps_output).write_text(lammps_Tg_script)
        if submit_jobs:
            subprocess.run(["qsub", pbs_file], cwd=run_dir, check=True)	#Optional

print("\nAll Tg simulation folders created.")