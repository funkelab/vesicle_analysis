import csv
import json
import glob

vesicle_list = []

csvfilenames = glob.glob('*.csv')

for csvfilename in csvfilenames:

    print(f"Converting {csvfilename}...")

    csvfile = open(csvfilename)

    # skip first line (just meta-data)
    for line in csvfile:
        break

    # skip "# " in the first line
    csvfile.read(2)

    reader = csv.DictReader(csvfile)
    id_count = 0
    for row in reader:
        row = {
            key.strip(): value
            for key, value in row.items()
        }
        vesicle_dict = {
            "vesicle_id": id_count,
            "z": (int(row['z'].strip())*93),
            "y": (int(row['y'].strip())*62),
            "x": (int(row['x'].strip())*62),
            "score": float(row['score'].strip()),
            "label": int(row['label'].strip())
        }
        id_count+=1
        vesicle_list.append(vesicle_dict)

    json_data = { 'vesicles': vesicle_list }

    with open(csvfilename.replace('.csv', '.json'), "w") as json_out:
        json_out.write(json.dumps(json_data, indent=4))
