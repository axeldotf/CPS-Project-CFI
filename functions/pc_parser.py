'''
----------------------------------------PC PARSER------------------------------------
This code allow us to read the trace file of the program executed on QEMU and transforms it into
a json file (trace_pc.json) where each program counter value (hexadecimal number) is associated
with a relative index indicating the order of execution 
'''
import json
from tqdm import tqdm

def pcparser(filename):

    with open("source/" + filename + "_pc.log", "r") as file:
        table = []
        total_lines = sum(1 for _ in file)
        file.seek(0)
        progress_bar = tqdm(total=total_lines, desc='Parsing PC file', unit=' instr', ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")

        for index, line in enumerate(file, start=1):
            progress_bar.update(1)
            if line.startswith("pc"):
                hex_value = line.split()[1].lstrip("0")
                table.append({"Index": index, "PC": hex_value})

        progress_bar.close()

    iterations = len(table)
    namefile = filename

    print("-" * 100)
    print("\nSaving data into file \"trace_pc.json\".")

    with open(filename + "/trace_pc.json", "w") as json_file:
        json.dump(table, json_file, indent=4)

    #---------------------------Exporting stats to a json file-----------------------------------
    stats_data = {
        "Name": namefile,
        "Instructions": iterations
    }

    with open(filename + "/stats.json", "w") as json_file:
        json.dump(stats_data, json_file, indent=4)
    #--------------------------------------------------------------------------------------------

    print("Data successfully exported to \"trace_pc.json\".\n")
    print("# instructions executed:", iterations)
    print("\n" + "-" * 100)