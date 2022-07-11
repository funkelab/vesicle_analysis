import zarr
import numpy as np
import json
#import tqdm
from skimage.measure import label

dataset_name = "17_1A_extended_2119-2535"
bouton_zarr = f'{dataset_name}_converted_2_consolidated.zarr'
zarr_container = f'/nrs/funke/sheridana/hausser/paintera_ingest/new_test_vols_2_14_22/{dataset_name}_converted_2_consolidated.zarr'

def create_object_to_area_json(zarr_container, object_type, area_type):
    
    if area_type == 'neuron':
        print("Reading neuron segmentation...")
        area_objects = zarr.open(zarr_container, 'r')['volumes/neurons'][:, :, :]
    if area_type == 'bouton':
        print("Reading bouton segementation...")
        area_objects = zarr.open(bouton_zarr, 'r')['volumes/boutons'][:, :, :]
    if object_type == 'az':
        print("Reading active zone segmentation...")
        objects = zarr.open(zarr_container, 'r')['volumes/synapses'][:, :, :]
        objects = label(objects, connectivity=1)
    if object_type == 'mito':
        print("Reading mitochondria segmentation...")
        objects = zarr.open(zarr_container, 'r')['volumes/mito'][:, :, :]
    print("Finding matches...")
    print(np.unique(objects))
    object_to_area = {}
    mult_max = int(np.amax(area_objects) + 1)

    assert mult_max <= 4294967296, "Neuron IDs are dangerously high!"
    assert objects.max() <= 4294967296, "Object IDs are dangerously high!"

    mult_matrix = (objects*mult_max + area_objects).flatten()
    unique_vals, counts = np.unique(mult_matrix, return_counts=True)
    unique_vals = list(map(int, unique_vals))

    # co-sort unique_vals and counts by counts
    pairs = zip(*sorted(zip(counts, unique_vals), reverse=True))
    counts, unique_vals = [list(pair) for pair in pairs]
    
    object_list = []
    obj_ids = set()
    for value in unique_vals:
        obj_dict = {}
        obj_id = value // mult_max
        area_obj_id = value % mult_max

        if obj_id == 0 or area_obj_id == 0:
            continue
        if obj_id in obj_ids:
            continue

        obj_volume = int((objects == obj_id).sum())
        obj_dict[object_type+"_id"] = obj_id
        obj_dict['volume_vx'] = obj_volume

        obj_dict[area_type+'_id'] = area_obj_id
        #object_to_neuron[int(obj_id)] = int(neuron_id)

        object_list.append(obj_dict)
        obj_ids.add(obj_id)

    print(object_list)


    data = {}
    data[object_type+"s"] = object_list
    with open(f'temp/{dataset_name}_{object_type}s_to_{area_type}s.json', "w") as json_out:
        json.dump(data, json_out)

if __name__ == '__main__':

    active_zones_to_neurons = create_object_to_area_json(zarr_container, 'az', 'neuron')
    mito_to_neurons = create_object_to_area_json(zarr_container, 'mito','neuron')
    active_zones_to_boutons = create_object_to_area_json(zarr_container,'az', 'bouton')
    mito_to_boutons = create_object_to_area_json(zarr_container,'mito','bouton')

