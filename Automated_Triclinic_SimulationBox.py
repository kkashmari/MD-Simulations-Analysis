# -*- coding: utf-8 -*-
"""
Creating LAMMPS script and directories for each equilibrated degree of cure and make the sim box triclinic to make it prepared for shear simulations
Author: Khatereh Kashmari

"""

from pathlib import Path
import shutil
import subprocess


simulation_folder_pattern = "PolyL10_rep_*s_pxld_*_Equilibrated"		#Folder names from equilibration simulations
output_file_pattern = "PolyL10*_p*_Equilibrated.data"	#Outputs from equilibration simulations
triclinic_sim_box_results = Path("triclinic_sim_box_Simulation_Runs")

lammps_template_script = "triclinic_sim_box_Simulation.in" #LAMMPS script template
New_lammps_output = "PolyL10_triclinic_sim_box_Simulation.in"	# generated LAMMPS script

pbs_file = "job.pbs"
submit_jobs = True


#Check if all the required files exist

if not Path(lammps_template_script).is_file():
    raise FileNotFoundError(f"Missing {lammps_template_script}")

if not Path(pbs_file).is_file():
    raise FileNotFoundError(f"Missing {pbs_file}")

triclinic_sim_box_results.mkdir(exist_ok=True)

triclinic_sim_box_template_script = Path(lammps_template_script).read_text()

#------------------------------------------------

#Generating new folders

for sim_dir in Path(".").glob(simulation_folder_pattern):

    if not sim_dir.is_dir():
        continue

    for data_file in sim_dir.glob(output_file_pattern):

        structure_name = data_file.stem

        run_dir = triclinic_sim_box_results / sim_dir.name / structure_name
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"Creating triclinic_sim_box run: {run_dir}")

        Input_data = run_dir / data_file.name
        shutil.copy(data_file, Input_data)
        shutil.copy(pbs_file, run_dir / pbs_file)

        rendered_script = triclinic_sim_box_template_script.replace("$DATAFILE$", data_file.name)
        (run_dir / New_lammps_output).write_text(triclinic_sim_box_template_script)
        if submit_jobs:
            subprocess.run(["qsub", pbs_file], cwd=run_dir, check=True)	#Optional

print("\nAll triclinic simulation box folders are created.")
