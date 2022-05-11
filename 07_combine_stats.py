import json
import glob


read_files = glob.glob("17_1A_extended_2119-253*.json")

stats = {}
for f in read_files:
	with open(f, 'r') as json_in:
		data_dict = json.load(json_in)
	stats = {**stats, **data_dict}


with open('stats_17_1A_extended_2119-2535_vesicles.json', 'w') as json_out:
	json.dump(stats, json_out, indent=4)