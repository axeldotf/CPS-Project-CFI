
'''
----------------------------------------ASM PARSER---------------------------------------------------------
This code reads the file obtained from disassembling the code executed on QEMU (RISCV) and parses the code,
allowing each program counter value (hexadecimal), its executed instruction (RISCV ISA), and the target
register to be exported to a json file (trace_asm.json). It also allows filtering of executed instructions
by going to select only those instructions that are useful for judging a jump safe or unsafe.
-----------------------------------------------------------------------------------------------------------
'''
import json
import re
from tqdm import tqdm

def asmparser(filename):

    with open('source/'+ filename + '_dSnum.log', 'r') as file:
        extracted_info = []
        discarded_info = []
        total_lines = sum(1 for _ in file)
        file.seek(0)
        progress_bar = tqdm(total=total_lines, desc='Parsing ASM file', unit=' instr', ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")

        for line in file:
            parts = line.strip().split()

            if len(parts) >= 3:    
                pc = parts[0][:-1] 
                instruction = parts[2]
                dest_reg = []
                source1_reg = []
                source2_reg = []

                if parts[2] in ["add", "sub", "and", "or", "xor", "sll", "srl", "sra", "mul", "mulh", "mulhu", "mulhsu", "slt", "sltu", "div", "divu", "rem", "remu"]:
                    instruction = "OP"
                    reg0 = parts[3].split(',')
                    dest_reg = reg0[0]
                    source1_reg = reg0[1]
                    source2_reg = reg0[2]

                elif parts[2] in ["addi", "subi", "andi", "ori", "xori", "slli", "srli", "srai", "slti", "sltiu", "mv", "not", "neg"]:
                    instruction = "OPi"
                    reg0_1 = parts[3].split(',')
                    dest_reg = reg0_1[0]
                    source1_reg = reg0_1[1]

                elif parts[2] in ["lw", "lh", "lb", "ld", "lbu", "lhu", "lwu"]:
                    reg1 = parts[3].split(',') 
                    dest_reg = reg1[0]

                elif parts[2] == "li":
                    reg1_1 = parts[3].split(',')  
                    dest_reg = reg1_1[0]    

                elif parts[2] == "jal":
                    if ',' in parts[3]: 
                        reg2 = parts[3].split(',')  
                        dest_reg = reg2[0]
                    else:
                        dest_reg = "x1"

                elif parts[2] == "ret":
                    dest_reg = "x1"

                elif parts[2] == "jalr":
                    if ',' in parts[3]:
                        reg3 = parts[3].split(',')  
                        dest_reg = reg3[0]
                    elif '(' in parts[3]:
                        reg3_1 = re.split(r'\(|\)', parts[3]) 
                        dest_reg = reg3_1[1] 
                    else:                   
                        dest_reg = parts[3] 

                elif parts[2] == "jr":
                    if ',' in parts[3]:
                        reg4 = parts[3].split(',')  
                        dest_reg = reg4[0]
                    elif '(' in parts[3]:
                        reg4_1 = re.split(r'\(|\)', parts[3])
                        dest_reg = reg4_1[1] 
                    else:                   
                        dest_reg = parts[3] 
                        
                else:
                    discarded_info.append({
                        "PC": pc,  
                        "Instruction": instruction,
                        "Destination": parts[3:]
                    })

                if dest_reg:
                    extracted_info.append({
                        "PC": pc,  
                        "Instruction": instruction,
                        "Source 1": source1_reg,
                        "Source 2": source2_reg,      
                        "Destination": dest_reg  
                    })

            progress_bar.update(1)

    progress_bar.close()

    print("-" * 100)
    print("\nSaving data into file \"trace_asm.json\".")

    with open(filename + "/trace_asm.json", "w") as json_file:
        json.dump(extracted_info, json_file, indent=4)

    with open(filename + "/discarded_asm.json", "w") as json_file:
        json.dump(discarded_info, json_file, indent=4)

    print("Data successfully exported to \"trace_asm.json\".\n")
    print("-" * 100)