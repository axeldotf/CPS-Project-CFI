# CPS-Project-CFI 

Link for material: https://drive.google.com/drive/folders/1C_GEVq41TuyQl_IAJTJzGnX_BCcgs0N5?usp=sharing

# CPS Project - Insecure Edge Counting for Control Flow Integrity

## Overview

This project aims to analyze and enhance Control Flow Integrity (CFI) by monitoring the flow of a program's execution, identifying safe and unsafe instructions, and generating statistics on forward/backward jumps. It leverages the RISC-V instruction set architecture and tools like Embench and QEMU for testing and analysis.

## Prerequisites

- **Embench**: Downloaded and set up to compile programs.
- **QEMU**: Used to emulate RISC-V execution and obtain trace data.
- **RISC-V Toolchain**: Specifically, `riscv64-unknown-elf-gcc` and `riscv64-unknown-elf-objdump` for compiling and disassembling the executables.
  
## Workflow

### 1. Download and Build Programs from Embench

- Download Embench.
- Compile all programs with the following command:

  ```bash
  ./build_all.py --arch riscv32 --chip generic --board ri5cyverilator \
  --cc riscv64-unknown-elf-gcc --cflags="-c -march=rv32imc -mabi=ilp32 -Os -ffunction-sections -fdata-sections" \
  --ldflags="-Wl,-gc-sections -march=rv32imc -mabi=ilp32 -Os" --user-libs="-lm" --clean
  ```

- The compilation generates **ELF files** for each executable in the program pool.

### 2. QEMU Tracing

- Obtain the trace of CPU registers and save the output to a `.log` file:

  ```bash
  qemu-riscv32 -singlestep -d nochain,cpu main 2>main.log
  grep -o 'pc\s*[0-9a-fA-F]\{8}' main.log >main_small.log
  ```

- Disassemble the target program and save the assembly code to a `.log` file:

  ```bash
  riscv64-unknown-elf-objdump -D -S -M numeric main >main_DSnum.log
  ```

### 3. Parsing the Logs

- Extract the program counter (PC) values from `main_small.log` and export them in JSON format:

  ```bash
  pc_parser.py -> trace_pc.json
  ```

- Parse the disassembled file (`main_DSnum.log`) to export relevant instructions (PC, instruction name, source and destination registers) to another JSON file:

  ```bash
  asm_parser.py -> trace_asm.json
  ```

- Save discarded instructions (instructions that do not produce results) in a separate JSON file:

  ```bash
  discarded_asm.json
  ```

### 4. Merging and Analyzing the Data

- Compare the data in `trace_pc.json` and `trace_asm.json` and associate each instruction with its corresponding PC value. Only instructions that produce results are considered. The output is saved to:

  ```bash
  merge_parser.py -> merge_list.json
  ```

- A counter is set up for each type of instruction.

### 5. Safe/Unsafe Analysis

- A table with 32 registers is initialized with all registers marked as "safe" (true). The program flow is simulated to update the safety of each register and keep a count of safe or unsafe jumps:

  ```bash
  safe_final.py -> safe_list.json
  ```

- Statistics are generated regarding the number of instructions and the number of forward/backward safe/unsafe jumps. This information is saved in:

  ```bash
  stats.json
  ```

### 6. Exporting Statistics

- The `stats.json` file is used to generate a CSV file containing statistics for all analyzed programs. Each row in the CSV corresponds to the results from a single program. If a program is reanalyzed, the table is updated:

  ```bash
  total_stats.csv
  ```

---

### File Structure

- `trace_pc.json`: Contains PC values in execution order.
- `trace_asm.json`: Contains parsed instructions.
- `discarded_asm.json`: Contains discarded instructions.
- `merge_list.json`: Merged data of PC values and corresponding instructions.
- `safe_list.json`: Safe/unsafe status of registers.
- `stats.json`: Detailed statistics for each analyzed program.
- `total_stats.csv`: Aggregated statistics for all programs analyzed.

## Contact
For questions or contributions, feel free to open an issue or contact the project maintainers.
