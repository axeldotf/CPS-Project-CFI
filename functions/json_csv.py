'''
----------------------------------------JSON TO CSV---------------------------------------
This function takes the statistics file in JSON format (one for each analyzed program)
and converts it into a CSV file (unique). If the CSV file already exists, the function
will update the existing data with the new data. If the CSV file does not exist, the
function will create a new file and write the data into it.
------------------------------------------------------------------------------------------
'''
import csv
import json
import os

def json_to_csv(filename, csv_file):
    with open(filename + "/stats.json", "r") as jf:
        data = json.load(jf)

    name = data["Name"]

    file_exists = os.path.exists(csv_file)

    rows = []

    if file_exists:
        with open(csv_file, 'r') as cf:
            reader = csv.DictReader(cf)
            for row in reader:
                if row["Name"] == name:
                    row = data
                rows.append(row)
    
    if not any(row["Name"] == name for row in rows):
        rows.append(data)

    with open(csv_file, 'w', newline='') as cf:
        writer = csv.DictWriter(cf, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows(rows)