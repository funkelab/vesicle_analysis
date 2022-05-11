Scripts
=======

1. `01_convert_csv_to_json.py`
	⇒ creates `<name>_vesicles.json`

2. `02_find_boutons.py`
	⇒ creates `<name.zarr>/volumes/boutons` (`uint64` segmentation)

3. `03_create_bouton_json.py`
	⇒ creates `<name>_bouton_to_neuron.json`

4. `04_obj_to_neuron.py`
	⇒ creates `<name>_[az,mito]_to_neuron.json`

5. `05_vesicle_and_bouton_mapping.py`
	⇒ creates `<name>_vesicle_to_bouton.json`

6. `06_distance_to_obj.py`
	⇒ creates `<name>_vesicle_distance_to_[az,mito,boundary].py`

7. `07_combine_stats.py`
	⇒ creates `stats_<name>.json`
