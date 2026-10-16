#!/usr/bin/env python3
"""Extract shear stress–strain data from a LAMMPS log file."""

from argparse import ArgumentParser
from pathlib import Path
import tempfile

import log  # Pizza.py
import numpy as np


WARNING_TEXT = (
    "WARNING: Bond/angle/dihedral extent > half of "
    "periodic box length"
)


def parse_arguments():
    parser = ArgumentParser(
        description="Extract shear stress–strain data from a LAMMPS log."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the LAMMPS log file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Directory for the extracted CSV file.",
    )
    return parser.parse_args()


def remove_problematic_warnings(input_file, temporary_file):
    """Copy the log while excluding lines that Pizza.py cannot parse."""

    with input_file.open("r", encoding="utf-8", errors="replace") as source:
        cleaned_lines = [
            line for line in source
            if WARNING_TEXT not in line
        ]

    temporary_file.write_text(
        "".join(cleaned_lines),
        encoding="utf-8",
    )


def extract_shear_data(log_file):
    """Extract shear strain, stress, and direction from a LAMMPS log."""

    thermo = log.log(str(log_file))

    return thermo.get(
        "Step",
        "v_etruexy",
        "v_etruexz",
        "v_etrueyz",
        "f_sxx_ave",
        "f_syy_ave",
        "f_szz_ave",
        "f_sxy_ave",
        "f_sxz_ave",
        "f_syz_ave",
        "v_dir",
    )


def main():
    args = parse_arguments()

    input_file = args.input_file.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not input_file.is_file():
        raise FileNotFoundError(
            f"LAMMPS log file was not found: {input_file}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temporary_directory:
        cleaned_log = (
            Path(temporary_directory)
            / f"{input_file.stem}_cleaned.log.lammps"
        )

        remove_problematic_warnings(input_file, cleaned_log)
        extracted_columns = extract_shear_data(cleaned_log)

    data = np.column_stack(extracted_columns)

    output_stem = input_file.name.removesuffix(".log.lammps")
    output_file = (
    output_dir
    / f"{output_stem}_stress_strain_data.csv"
)
    header = (
        "timestep,"
        "true_strain_xy,"
        "true_strain_xz,"
        "true_strain_yz,"
        "normal_stress_x,"
        "normal_stress_y,"
        "normal_stress_z,"
        "shear_stress_xy,"
        "shear_stress_xz,"
        "shear_stress_yz,"
        "direction"
    )

    np.savetxt(
        output_file,
        data,
        delimiter=",",
        header=header,
        comments="",
    )

    print(f"Input log: {input_file}")
    print(f"Extracted rows: {len(data)}")
    print(f"Output CSV: {output_file}")


if __name__ == "__main__":
    main()
