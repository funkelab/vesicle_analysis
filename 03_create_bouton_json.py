import zarr
import numpy as np
import json
#import tqdm

dataset_name = "17_1A_extended_2119-2535"
zarr_containers = [
    f'/nrs/funke/sheridana/hausser/paintera_ingest/new_test_vols_2_14_22/{dataset_name}_converted_2_consolidated.zarr'
]


def create_bouton_json(zarr_container):

    bouton_zarr = f'{dataset_name}_converted_2_consolidated.zarr'
    print("Reading neuron segmentation...")
    neurons = zarr.open(zarr_container, 'r')['volumes/neurons'][:, :, :] 
    print("Reading bouton segmentation...")
    boutons = zarr.open(bouton_zarr, 'r')['volumes/boutons'][:,:,:]
    print(type(boutons))
    print(boutons.shape)
    overlaps = np.stack([neurons, boutons])
    print("Finding matches...")
    

    #boutons = []
    mult_max = int(np.amax(neurons) + 1)

    assert mult_max <= 4294967296, "Neuron IDs are dangerously high!"
    #boutons = np.array(boutons)
    #print(type(boutons))
    #print(boutons.shape)
    assert np.max(boutons) <= 4294967296, "Bouton IDs are dangerously high!"
    
    mult_matrix = (boutons*mult_max + neurons).flatten()
    unique_vals  = list(map(int, np.unique(mult_matrix)))
    bouton_list = []
    for value in unique_vals:
        bouton_dict = {}
        bouton_id = value // mult_max
        neuron_id = value % mult_max
        if neuron_id == 0 or bouton_id == 0:
            continue
        bouton_volume = int((boutons == bouton_id).sum())
        bouton_dict['bouton_id'] = bouton_id
        bouton_dict['neuron_id'] = neuron_id
        bouton_dict['volume_vx'] = bouton_volume
        bouton_list.append(bouton_dict)

    print(boutons)

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
    data["boutons"] = bouton_list
    with open(f"temp/{dataset_name}_boutons.json", "w") as json_out:
        json.dump(data, json_out)

if __name__ == '__main__':

    for zarr_container in zarr_containers:
        boutons = create_bouton_json(zarr_container)
