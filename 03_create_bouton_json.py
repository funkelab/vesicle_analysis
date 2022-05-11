import zarr
import numpy as np
import json
#import tqdm

zarr_containers = [
   # '/nrs/funke/sheridana/hausser/paintera_ingest/new_test_vols_2_14_22/17_1A_extended_2119-2535_converted_2_consolidated.zarr'
   '17_1A_extended_2119-2535_converted_2_consolidated.zarr'
]


def create_bouton_json(zarr_container):

    # FIXME: don't use the test volume
    # bouton_zarr = zarr_container.split('/')[-1]
    bouton_zarr = '17_1A_extended_2119-2535_test_volume.zarr'
    print("Reading neuron segmentation...")
    neurons = zarr.open(zarr_container, 'r')['volumes/neurons'][10, :, :]
    print("Reading bouton segmentation...")
    boutons = zarr.open(bouton_zarr, 'r')['volumes/boutons'][10, :, :]
    overlaps = np.stack([neurons, boutons])
    print("Finding matches...")
    

    bouton_to_neuron = {}
    mult_max = np.amax(neurons) + 1

    assert mult_max <= 4294967296, "Neuron IDs are dangerously high!"
    assert boutons.max() <= 4294967296, "Bouton IDs are dangerously high!"

    mult_matrix = (boutons*mult_max + neurons).flatten()
    unique_vals, unique_indices = np.unique(mult_matrix, return_index = True) 

    for value in unique_vals:
        bouton_id = value // mult_max
        neuron_id = value % mult_max
        bouton_to_neuron[bouton_id] = neuron_id

    print(bouton_to_neuron)

    """
    matches = [
        np.unique(overlaps[:,z,:,:], axis=0)
        for z in tqdm.tqdm(range(neurons.shape[0]))
    ]
    matches = np.unique(np.concatenate(matches), axis=1)
    print("Exporting matches...")
    bouton_to_neuron = {}
    for match in matches:
        if np.prod(match) != 0:
            assert match[1] not in bouton_to_neuron
            bouton_to_neuron[match[1]] = match[0]
    """
    data = {}
    data["bouton_to_neuron"] = bouton_to_neuron
    with open(bouton_zarr[:-5]+"_bouton_to_neuron.json", "w") as json_out:
        json.dump(bouton_to_neuron, json_out)

if __name__ == '__main__':

    for zarr_container in zarr_containers:
        boutons = create_bouton_json(zarr_container)
