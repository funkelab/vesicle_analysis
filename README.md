This repository contains scripts to analyse vesicles predictions (provided as a
CSV file) and store the result as a JSON file. The JSON file contains, for each
vesicle, its

* position
* score
* label
* the bouton it belongs to
* the distances to the closes active zone, boundary, and mitochondria



Scripts
=======

1. `01_convert_csv_to_json.py`
  * converts CSVs of vesicles into JSON
  * ⇒ creates `temp/<name>_vesicles.json`

2. `02_find_boutons.py`
  * identifies boutons from a neuron segmentation
  * this scripts takes a while to run and will need a lot of memory
  * ⇒ creates `<name>.zarr/volumes/boutons` (`uint64` segmentation)

3. `03_create_bouton_json.py`
  * creates a look-up of boutons to neuron IDs
  * ⇒ creates `temp/<name>_bouton_to_neuron.json`

4. `04_obj_to_area.py`
  * creates look-ups of active zones and mitochondria to neurons and boutons
  * ⇒ creates `temp/<name>_[az,mito]_to_neuron.json`

5. `05_vesicle_and_bouton_mapping.py`
  * creates a look-up of vesicles to boutons
  * ⇒ creates `temp/<name>_vesicle_to_bouton.json`

6. `06_distance_to_obj.py`
  * measures the distances of vesicles to active zones, mitochondria, and
    bouton boundaries
  * ⇒ creates `temp/<name>_vesicle_distance_to_[az,mito].py`

7. `07_compile_stats.py`
  * combines all stats into a single JSON
  * ⇒ creates `stats_<name>.json`
