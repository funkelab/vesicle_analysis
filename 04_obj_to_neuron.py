import zarr
import numpy as np
import json
#import tqdm
from skimage.measure import label
zarr_containers = [
    '/nrs/funke/sheridana/hausser/paintera_ingest/new_test_vols_2_14_22/17_1A_extended_2119-2535_converted_2_consolidated.zarr'
    ]

def create_object_to_neuron_json(zarr_container, object_type):

    print("Reading neuron segmentation...")
    neurons = zarr.open(zarr_container, 'r')['volumes/neurons'][230, :, :]
    if object_type == 'az':
        print("Reading active zone segmentation...")
        objects = zarr.open(zarr_container, 'r')['volumes/synapses'][230, :, :]
        objects = label(active_zones, connectivity=1)
    if object_type == 'mito':
        print("Reading mitochondria segmentation...")
        objects = zarr.open(zarr_container, 'r')['volumes/mito'][:10, :, :]
    print("Finding matches...")
    print(np.unique(objects))
    object_to_neuron = {}
    mult_max = np.uint64(np.amax(neurons) + 1)

    assert mult_max <= 4294967296, "Neuron IDs are dangerously high!"
    assert objects.max() <= 4294967296, "Object IDs are dangerously high!"

    mult_matrix = (objects*mult_max + neurons).flatten()
    unique_vals = np.unique(mult_matrix)
    
    for value in unique_vals:
        obj_id = value // mult_max
        neuron_id = value % mult_max
        if obj_id == 0 or neuron_id == 0:
            continue
        object_to_neuron[int(obj_id)] = int(neuron_id)

    print(object_to_neuron)

    with open(zarr_container.split('/')[-1][:-5]+object_type+"_to_neuron.json", "w") as json_out:
        json.dump(object_to_neuron, json_out)

if __name__ == '__main__':

    for zarr_container in zarr_containers:
        active_zones = create_object_to_neuron_json(zarr_container, 'az')
    for zarr_container in zarr_containers:
        mito = create_object_to_neuron_json(zarr_container, 'mito')

