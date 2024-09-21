# Code Manual

## Folder Structure and Setup

To correctly run the analysis, ensure that your working folder contains the following elements:

1. **`main.py`**: The main script to execute the program analysis.
2. **`supercounter.py`** (optional): This script can be included if further counting or analysis is required.
3. **Subfolders**:
   - **`source`**: This folder contains the code (or programs) that you want to process and analyze.
   - **`functions`**: This folder contains any helper functions or scripts used by `main.py` to parse, analyze, and generate statistics.

## How to Execute the Code

To start the analysis of a program, navigate to the working folder in your terminal and run the following command:

```bash
python main.py <program name>
```

- Replace `<program name>` with the specific name of the program you wish to analyze (located in the `source` folder).

## Execution Process

- During the execution of the code, a new subfolder will be created inside the working folder. This subfolder will be named after the program being analyzed and will contain several **JSON** files. Each of these files will include detailed statistics and analysis related to the program's execution, such as parsed instructions, safe/unsafe jumps, and performance metrics.
  
- Once the analysis is complete, a file named **`total_stats.csv`** will be updated with the statistics of the program. If the program has already been analyzed before, this CSV file will be updated with the new results.

The **`total_stats.csv`** file stores cumulative statistics for all programs processed, allowing for easy comparison and tracking of results over time.

