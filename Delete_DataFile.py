
"""
Created on Wed Jul 26 17:31:39 2023

@author: khatereh
"""

import time

def delete_text_from_file(file_path, start_string):
    start_time = time.time()  # Start the timer
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        start_index = content.find(start_string)

        if start_index != -1:
            new_content = content[:start_index]

            with open(file_path, 'w') as file:
                file.write(new_content)
            print(f"Text successfully deleted from {file_path}.")
        else:
            print(f"Specified text not found in {file_path}.")
    
    except FileNotFoundError:
        print(f"File not found: {file_path}. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred with {file_path}: {e}")
    finally:
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time
        print(f"Runtime for {file_path}: {elapsed_time:.4f} seconds")

def process_multiple_files(file_paths, start_string):
    for file_path in file_paths:
        delete_text_from_file(file_path, start_string)


if __name__ == "__main__":
    file_paths = [
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_93.6507.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_5.85ps_pxld_9.0702_prxn3_3.741496.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_10.925ps_pxld_19.1609_prxn3_14.2857.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_15.625ps_pxld_29.024_prxn3_25.17.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_22ps_pxld_39.0022_prxn3_36.3945.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_30.85ps_pxld_49.0929_prxn3_46.9387.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_36.475ps_pxld_54.0816_prxn3_52.3809.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_47.1ps_pxld_59.070_prxn3_57.8231.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_64.1ps_pxld_64.0589_prxn3_62.9251.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_79.375ps_pxld_69.0476_prxn3_68.367.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_156.1ps_pxld_79.0249_prxn3_77.5510.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_111.725ps_pxld_74.0362_prxn3_73.1292.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/3/Seq_180/poly_rep_1_453K_time_220.675ps_pxld_84.0136_prxn3_82.993.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_244.975ps_pxld_84.0136_prxn3_83.33.data',
        '/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq_120/poly_rep_1_393K_time_444.325ps_pxld_89.002_prxn3_88.4353.data'     
    ]
    start_string = 'bond_react_props_internal'

    process_multiple_files(file_paths, start_string)

