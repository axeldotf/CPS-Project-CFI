'''
----------------------------------------INSTRUCTION COUNTER------------------------------------
This code is used to count the number of each type of instruction in the merge_list.json file
-----------------------------------------------------------------------------------------------
'''

import json
from tqdm import tqdm

def icounter(filename):

    with open(filename + "/merge_list.json", "r") as json_file:
        merge_data = json.load(json_file)

    merged_inst = len(merge_data)

    jal_cnt = 0
    op_cnt = 0
    opi_cnt = 0
    jalr_cnt = 0
    l_cnt = 0
    jr_cnt = 0
    li_cnt = 0
    ret_cnt = 0

    progress_bar = tqdm(total=merged_inst, desc='Counting Instructions', unit=' instr', ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")

    for item in merge_data:
        instruction = item["Instruction"]

        if instruction == "jal":
            jal_cnt += 1
        elif instruction == "OP":
            op_cnt += 1
        elif instruction == "OPi":
            opi_cnt += 1
        elif instruction == "jalr":
            jalr_cnt += 1
        elif instruction in ["lw", "lh", "lb", "ld"]:
            l_cnt += 1
        elif instruction == "jr":
            jr_cnt += 1
        elif instruction == "li":
            li_cnt += 1
        elif instruction == "ret":
            ret_cnt += 1

        progress_bar.update(1)

    progress_bar.close()

    jal_p = (jal_cnt / merged_inst) * 100
    jalr_p = (jalr_cnt / merged_inst) * 100
    l_p = (l_cnt / merged_inst) * 100
    jr_p = (jr_cnt / merged_inst) * 100
    li_p = (li_cnt / merged_inst) * 100
    op_p = (op_cnt / merged_inst) * 100
    opi_p = (opi_cnt / merged_inst) * 100
    ret_p = (ret_cnt / merged_inst) * 100

    new_stats_data = {
        "JAL": jal_cnt,
        "OP": op_cnt,
        "OPi": opi_cnt,
        "JALR": jalr_cnt,
        "JR": jr_cnt,
        "RET": ret_cnt,
        "LI": li_cnt,
        "LOAD": l_cnt
    }

    with open(filename + '/stats.json', 'r') as stats_file:
        old_stats_data = json.load(stats_file)

    old_stats_data.update(new_stats_data)

    with open(filename + "/stats.json", "w") as stats_file:
        json.dump(old_stats_data, stats_file, indent=4)

    print("-" * 100)
    print("\n# inspected instructions:", merged_inst)
    print(f"# op:\t {op_cnt} ({op_p:.2f}%)")
    print(f"# opi:\t {opi_cnt} ({opi_p:.2f}%)")
    print(f"# jal:\t {jal_cnt} ({jal_p:.2f}%)")
    print(f"# jalr:\t {jalr_cnt} ({jalr_p:.2f}%)")
    print(f"# jr:\t {jr_cnt} ({jr_p:.2f}%)")
    print(f"# ret:\t {ret_cnt} ({ret_p:.2f}%)")
    print(f"# li:\t {li_cnt} ({li_p:.2f}%)")
    print(f"# l:\t {l_cnt} ({l_p:.2f}%)\n")
    print("-" * 100)