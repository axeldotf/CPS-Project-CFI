'''
----------------------------------------MERGE PARSER------------------------------------
This code compares data from trace_pc.json and trace_asm.json and associates every
instruction to its respective PC value contained in trace_pc.json, so that we can
obtain the order of execution of only the instructions that we are interested in and
their respective kind of instruction and destination register.
'''

import json
from tqdm import tqdm

def mergeparser(filename):

    with open(filename + '/trace_pc.json', 'r') as pc_file:
        pc_data = json.load(pc_file)

    with open(filename + '/trace_asm.json', 'r') as asm_file:
        asm_data = json.load(asm_file)

    with open(filename + '/discarded_asm.json', 'r') as discarded_file:
        discarded_data = json.load(discarded_file)

    asm_dict = {
        item['PC']: {
            'Instruction': item['Instruction'],
            'Destination': item['Destination'],
            "Source 1": item["Source 1"],
            "Source 2": item["Source 2"]
        }
        for item in asm_data
    }

    discarded_dict = {
        item['PC']: {
            'Instruction': item['Instruction'],
            'Destination': item['Destination']
        }
        for item in discarded_data
    }    

    result_list = []
    discarded_list = []

    progress_bar = tqdm(pc_data, desc='Merging parsing files', unit=' instr', ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")

    for item in progress_bar:
        pc_value = item['PC']

        if pc_value in asm_dict:
            result_list.append({
                'Index': item['Index'], 
                'PC': pc_value, 
                'Instruction': asm_dict[pc_value]['Instruction'],
                'Destination': asm_dict[pc_value]['Destination'],
                'Source 1': asm_dict[pc_value]['Source 1'],
                'Source 2': asm_dict[pc_value]['Source 2']
            })

        elif pc_value in discarded_dict:
            discarded_list.append({
                'Index': item['Index'], 
                'PC': pc_value, 
                'Instruction': discarded_dict[pc_value]['Instruction'],
                'Destination': discarded_dict[pc_value]['Destination']
            })

    progress_bar.close()

    parsed_inst = len(result_list)
    iterations = len(pc_data)
    parsed_inst_p = (parsed_inst / iterations) * 100

    discarded_l = len(discarded_list)
    discarded_p = (discarded_l / iterations) * 100

    print("-" * 100)
    print("\nSaving data into file \"merge_list.json\".")

    with open(filename + "/merge_list.json", "w") as json_file:
        json.dump(result_list, json_file, indent=4)

    with open(filename + "/discarded_list.json", "w") as json_file:
        json.dump(discarded_list, json_file, indent=4)

    new_stats_data = {
        "Analyzed": parsed_inst,
        "Discarded": discarded_l
    }

    with open(filename + '/stats.json', 'r') as stats_file:
        old_stats_data = json.load(stats_file)

    old_stats_data.update(new_stats_data)

    with open(filename + "/stats.json", "w") as stats_file:
        json.dump(old_stats_data, stats_file, indent=4)

    print("Data successfully exported to \"merge_list.json\".\n")
    print(f"# executed instructions:\t {iterations}")
    print(f"# instructions to inspect:\t {parsed_inst} ({parsed_inst_p:.2f}%)")
    print(f"# instructions discarded:\t {discarded_l} ({discarded_p:.2f}%)\n")
    print("-" * 100)