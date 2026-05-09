# -*- coding: utf-8 -*-
"""
Creating LAMMPS script and directories for each triclinic sim box degree of cure and run shear deformation simulations in xy, xz and yz directions
Author: Khatereh Kashmari
"""

from pathlib import Path
import shutil
import subprocess

simulation_folder_pattern = "PolyL10_rep_*s_pxld_*_Equilibrated_triclinic_box"		#Folder names from triclinic box simulations
output_file_pattern = "PolyL10*_p*_Equilibrated_triclinic_box.data"	#Outputs from triclinic box simulations
direction = [1, 2, 3]	#Change deformation directions
direction_map = {
    1: "xy",
    2: "xz",
    3: "yz"
}
ShearM_results = Path("Shear_Simulation_Runs")

lammps_template_script = "ShearM_Simulations.in" #LAMMPS script template
New_lammps_output = "PolyL10_ShearM_Simulations.in"	# generated LAMMPS script

pbs_file = "job.pbs"
submit_jobs = True
#Check if all the required files exist
if not Path(lammps_template_script).is_file():
    raise FileNotFoundError(f"Missing {lammps_template_script}")

if not Path(pbs_file).is_file():
    raise FileNotFoundError(f"Missing {pbs_file}")

ShearM_results.mkdir(exist_ok=True)

ShearM_template_script = Path(lammps_template_script).read_text()

#------------------------------------------------

#Generating new folders
for sim_dir in Path(".").glob(simulation_folder_pattern):

    if not sim_dir.is_dir():
        continue

    for data_file in sim_dir.glob(output_file_pattern):

        structure_name = data_file.stem

        run_dir = ShearM_results / sim_dir.name / structure_name
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"Creating Shear deformation run: {run_dir}")

        Input_datafile = run_dir / data_file.name
        shutil.copy(data_file, Input_datafile)
        shutil.copy(pbs_file, run_dir / pbs_file)
        for direction, direction_name in direction_map.items():
            lammps_ShearM_script = ShearM_template_script.replace("$DATAFILE$", data_file.name)
            lammps_ShearM_script = lammps_ShearM_script.replace("$DIR$", str(direction))
            final_output_script = f"L10_ShearM_{direction_name}.in"
            (run_dir / final_output_script).write_text(lammps_ShearM_script)
        if submit_jobs:
            subprocess.run(["qsub", pbs_file], cwd=run_dir, check=True)	#Optional

print("\nAll Shear simulation folders created.")