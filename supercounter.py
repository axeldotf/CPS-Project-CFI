import json
from collections import Counter

def count_all(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    instruction_values = []
    pc_values = []

    for item in data:
        instruction_values.append(item["Instruction"])
        pc_values.append(item["PC"])

    instruction_counts = Counter(instruction_values)

    print("-" * 100)
    print(f"Analysis of {json_file}:\n")
    for instruction, count in instruction_counts.items():
        print(f"Instruction: {instruction}, Occurrences: {count}")

def count_pc(json_file, pcvalue):
    with open(json_file, "r") as file:
        data = json.load(file)

    pc_values = []

    for item in data:
        pc_values.append(item["PC"])

    print(f"The PC value '{pcvalue}' occurs {pc_values.count(pcvalue)} times in '{json_file}'.\n")

def main():
    print("-"*35, "Welcome to the SuperCounter!", "-"*35)

    filechoice = input("\nWhich file do you want to analyze? Enter the name of the subfolder:\n").lower()

    while True:
        mergename = filechoice + "/merge_list.json"
        discardedname = filechoice + "/discarded_list.json"
        choice = input("\nWhich instructions do you want to count? Enter 'merge' or 'discarded' (or 'exit' to quit):\n").lower()
        if choice == "merge":
            count_all(mergename)
            print("-" * 100)
            print("Do you want to count the occurrences of a specific PC value? Enter 'yes' or 'exit' to quit.")
            pc_choice = input().lower()
            if pc_choice == "yes":
                count_pc(mergename, input("Enter the PC value:\n"))
            elif pc_choice == "exit":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'exit'.\n")
        elif choice == "discarded":
            count_all(discardedname)
            print("-" * 100)
            print("Do you want to count the occurrences of a specific PC value? Enter 'yes' or 'exit' to quit.")
            pc_choice = input().lower()
            if pc_choice == "yes":
                count_pc(discardedname, input("Enter the PC value:\n"))
            elif pc_choice == "exit":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'exit'.\n")
        elif choice == "exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 'merge', 'discarded', 'pc' (or 'exit' to quit).\n")

if __name__ == "__main__":
    main()