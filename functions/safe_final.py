'''
----------------------------------------PC PARSER------------------------------------
This code is used to check every jumps and applies criteria that let us define if a
jump is safe or not It reports the number safe backward and forward jumps, unsafe
backward and forward jumps, and the percentage of each one
'''

import json
from tqdm import tqdm

def regreset(filename):
    with open(filename + "/safe_list.json", "w") as json_file:
        reg_list = [{"Register": f"x{i}", "Safe": True} for i in range(32)]
        json.dump(reg_list, json_file, indent=4)

def safelist(filename):

    regreset(filename)
    
    with open(filename + "/merge_list.json", "r") as json_file:
        merge_data = json.load(json_file)

    with open(filename + "/safe_list.json", "r") as json_file:
        safe_data = json.load(json_file)

    safe_fw_cnt = 0
    unsafe_fw_cnt = 0
    safe_bw_cnt = 0
    unsafe_bw_cnt = 0

    progress_bar = tqdm(total=len(merge_data), desc='Updating safety table', unit=' instr', ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")

    for item in merge_data:

        progress_bar.update(1)
        # index = item["Index"]
        # pc = item["PC"]
        destination = item["Destination"]
        instruction = item["Instruction"]
        source1 = item["Source 1"]
        source2 = item["Source 2"]

        break_flag = False

        if instruction in ["OP", "OPi"]:
            for safe_item in safe_data:
                if break_flag:
                    break_flag = False
                    break
                if safe_item["Register"] == source1 or safe_item["Register"] == source2:
                    if not safe_item["Safe"]:
                        for safe_item in safe_data:
                            if safe_item["Register"] == destination:
                                safe_item["Safe"] = False
                                break_flag = True
                    elif safe_item["Safe"]:
                        for safe_item in safe_data:
                            if safe_item["Register"] == destination:
                                safe_item["Safe"] = True
    
        elif instruction in ["lw", "lh", "lb", "ld", "lbu", "lhu", "lwu"]:
            for safe_item in safe_data:
                if safe_item["Register"] == destination:
                    safe_item["Safe"] = False
                    break
        
        elif instruction == "li":
            for safe_item in safe_data:
                if safe_item["Register"] == destination:
                    safe_item["Safe"] = True
                    break

        elif instruction == "jal":
            for safe_item in safe_data:
                if safe_item["Register"] == destination:
                    safe_item["Safe"] = True
                    break

        elif instruction in ["jalr", "jr"]:
            for safe_item in safe_data:
                if safe_item["Register"] == "x1":
                    safe_item["Safe"] = True        
                if safe_item["Register"] == destination:
                    if safe_item["Safe"]:
                        safe_fw_cnt += 1
                    else:
                        unsafe_fw_cnt += 1
                        safe_item["Safe"] = True
                    break

        elif instruction == "ret":
            for safe_item in safe_data:
                if safe_item["Register"] == "x1":
                    if safe_item["Safe"] == True:
                        safe_bw_cnt += 1
                    else:
                        unsafe_bw_cnt += 1
                        safe_item["Safe"] = True
                    break

        else:
            print(f"Error: Unknown instruction of kind \"{instruction}\"")

    progress_bar.close()

    with open(filename + "/safe_list.json", "w") as json_file:
        json.dump(safe_data, json_file, indent=4)

    tot_fw_cnt = safe_fw_cnt + unsafe_fw_cnt
    tot_bw_cnt = safe_bw_cnt + unsafe_bw_cnt
    tot_cnt = tot_fw_cnt + tot_bw_cnt

    fw_p = (tot_fw_cnt / tot_cnt) * 100
    bw_p = (tot_bw_cnt / tot_cnt) * 100

    safe_fw_p = (safe_fw_cnt / tot_fw_cnt) * 100
    unsafe_fw_p = (unsafe_fw_cnt / tot_fw_cnt) * 100
    safe_bw_p = (safe_bw_cnt / tot_bw_cnt) * 100
    unsafe_bw_p = (unsafe_bw_cnt / tot_bw_cnt) * 100

    new_stats_data = {
        "Jumps": tot_cnt,
        "FW Jumps": tot_fw_cnt,
        "BW Jumps": tot_bw_cnt,
        "Safe FW": safe_fw_cnt,
        "Unsafe FW": unsafe_fw_cnt,
        "Safe BW": safe_bw_cnt,
        "Unsafe BW": unsafe_bw_cnt
    }

    with open(filename + '/stats.json', 'r') as stats_file:
        old_stats_data = json.load(stats_file)

    old_stats_data.update(new_stats_data)

    with open(filename + "/stats.json", "w") as stats_file:
        json.dump(old_stats_data, stats_file, indent=4)

    print("-"*100)
    print("\nSafety table \"safe_list.json\" updated succesfully.\n")

    print(f"Total jumps:\t {tot_cnt}\n")
    print(f"Total fw jumps:\t {tot_fw_cnt} ({fw_p:.1f}%)")
    print(f"Safe fw:\t {safe_fw_cnt} ({safe_fw_p:.1f}%)")
    print(f"Unsafe fw:\t {unsafe_fw_cnt} ({unsafe_fw_p:.1f}%)\n")
    print(f"Total bw jumps:\t {tot_bw_cnt} ({bw_p:.1f}%)")
    print(f"Safe bw:\t {safe_bw_cnt} ({safe_bw_p:.1f}%)")
    print(f"Unsafe bw:\t {unsafe_bw_cnt} ({unsafe_bw_p:.1f}%)\n")

    print("-"*100)