import sys
import os
import time
from functions.pc_parser import pcparser
from functions.asm_parser import asmparser
from functions.merge_parser import mergeparser
from functions.instr_counter import icounter
from functions.safe_final import safelist
from functions.json_csv import json_to_csv


def main():
    # Pass arguments to imported functions
    if len(sys.argv) > 1:

        # Path of the subfolder
        folder_path = os.path.join(os.path.dirname(__file__), sys.argv[1])

        # Check if the subfolder already exists
        if not os.path.exists(folder_path):
            # Create the subfolder
            os.makedirs(sys.argv[1])
            print(f"\nFolder '{sys.argv[1]}' created successfully.\n")
        else:
            print(f"\nFolder '{sys.argv[1]}' already exists: output files will be saved in this folder.\n")
        print("-" * 100)

        # Start the timer
        t1 = time.time()

        # Pass arguments to functions
        pcparser(sys.argv[1])
        asmparser(sys.argv[1])
        mergeparser(sys.argv[1])
        icounter(sys.argv[1])
        safelist(sys.argv[1])

        # Export data to CSV
        csv_name = "total_stats.csv"
        json_to_csv(sys.argv[1], csv_name)

        # Stop timer and calculate time
        t2 = time.time()
        tt = t2 - t1

        print(f"Data export from file \"{sys.argv[1]}.c\" completed successfully in {round(tt, 1)} seconds.")
        print(f"Data saved in the folder \"{sys.argv[1]}\".\n")
        print(f"\"{sys.argv[1]}\" statistics exported into file \"stats.json\".")
        print(f"Statistics added to the global statistics file \"{csv_name}\".\n")

if __name__ == "__main__":
    main()