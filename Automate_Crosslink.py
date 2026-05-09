
# -*- coding: utf-8 -*-
"""
Directory and LAMMPS input generator for L10 Crosslinking simulations

Author: Khatereh Kashmari
"""

import os
import shutil
from pathlib import Pat
import subprocess

# User Inputs

template_file = "L10_ Crosslinking_template.in"

replicates = [1, 2, 3, 4, 5]	#Change replicates

temperatures = [393, 413, 433, 453]	#Change Temperature

output_lmp_script = "CE_react_step_seq.in"	#Customized LAMMPS Script


common_files = [		# Reacter templates and map files in every directory
    "job.pbs",
    "Pre1_typed_IFF_merged.moltemp",
    "POST1_typed_IFF_merged.moltemp",
    "PRE2_typed_IFF_merged.moltemp",
    "POST2_typed_IFF_merged.moltemp",
    "PRE4_typed_IFF_merged.moltemp",
    "POST4_typed_IFF_merged.moltemp",
    "pre1post1_rxnmap.txt",
    "pre2post2_rxnmap.txt",
    "pre3post3_rxnmap.txt"
]

pbs_file = "job.pbs"

submit_jobs = True	#change to False if you dont want to submit the job automatically

with open(template_file, "r") as f: 	# Read LAMMPS templates
    template = f.read()

# Generating Directories and LAMMPS script for each temperature and replicates

for rep in replicates:
    datafile = f"CEmono_NPT0{rep}.data"		# Input data file
    if not os.path.isfile(datafile):
        print(f"WARNING: Missing file -> {datafile}")		   # Check file exists
        continue

    for temp in temperatures:
        dirname = f"L10_Replicate_{rep}_{temp}K"	# Directory name
        print(f"\nCreating: {dirname}")
        os.makedirs(dirname, exist_ok=True)
        shutil.copy(datafile, dirname)

        for file in common_files:	        # Copy common files
            if os.path.isfile(file):
                shutil.copy(file, dirname)
            else:
                print(f"WARNING: Missing common file -> {file}")


        new_script = template   # Generate LAMMPS input script 
        new_script = new_script.replace("$REPLICATE$", str(rep))
        new_script = new_script.replace("$TEMPERATURE$", str(temp))
        new_script = new_script.replace("$DATAFILE$", datafile)

        output_path = os.path.join(dirname,"CE_react_step_seq.in")

        with open(output_path, "w") as f:
            f.write(new_script)

        print(f"Created {dirname}")

        if submit_jobs:			#This could be optional
            try:
                subprocess.run(["qsub", pbs_file], cwd=dirname, check=True)
                print(f"Job submitted for {dirname}")
            except Exception as e:
                print(f"FAILED to submit job for {dirname}: {e}")	

    print("All simulations generated.")
