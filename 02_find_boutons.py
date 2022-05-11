import zarr
import skimage.measure
import skimage.morphology
import skimage.filters
import numpy as np
import time
import json

zarr_containers = [
    '/nrs/funke/sheridana/hausser/paintera_ingest/new_test_vols_2_14_22/17_1A_extended_2119-2535_converted_2_consolidated.zarr'
]

def erode_dilate(mask, erode_radius=15, dilate_radius=15):

    start = time.time()

    for i in range(erode_radius):
        print(f"Erode iteration {i}...")
        mask = skimage.morphology.binary_erosion(mask)
    for i in range(dilate_radius):
        print(f"Dilate iteration {i}...")
        mask = skimage.morphology.binary_dilation(mask)

    print(f"erode_dilate took {time.time() - start}s")

    return mask

def intersect(blobs, mask):

    all_boutons = np.zeros_like(blobs)

    # for each blob:
    for blob_id in np.unique(blobs):

        if blob_id == 0:
            continue

        print(f"Blurring and thresholding blob {blob_id}...")

        # blob mask
        blob_mask = (blobs == blob_id).astype(np.float)
        blob_mask = skimage.filters.gaussian(blob_mask, sigma=100.0)
        blob_mask = blob_mask > 0.01

        # intersect with mask
        intersection = mask * blob_mask

        all_boutons[intersection==1] = blob_id

    return all_boutons

def find_boutons(zarr_container):
    
    bouton_to_neuron = {}
    # read the neuron segmentation
    print(f"Reading neuron segmentation from {zarr_container}...")

    segmentation = zarr.open(zarr_container, 'r')['volumes/neurons'][:10, :, :]

    print("Finding neuron IDs...")
    neuron_ids = np.unique(segmentation)
    all_boutons = np.zeros_like(segmentation)
    max_bouton_id = 0
    bouton_id = 1
    for neuron_id in neuron_ids:

        if neuron_id == 0:
            continue
        print(f"Processing neuron {neuron_id}...")

        mask = segmentation == neuron_id

        print(f"Eroding/dilating...")
        bouton_mask = erode_dilate(mask)

        print(f"Label connected components...")
        bouton_blobs = skimage.measure.label(bouton_mask)

        boutons = intersect(bouton_blobs, mask)

        num_boutons = boutons.max()
        boutons[boutons > 0] += max_bouton_id
        all_boutons = all_boutons + boutons
        max_bouton_id += num_boutons

        bouton_to_neuron[bouton_id] = int(neuron_id)
        bouton_id += 1

    return all_boutons, bouton_to_neuron

def create_bouton_to_neuron_json(bouton_to_neuron, zarr_container):
    with open(zarr_container.split('/')[-1][:-5]+"_bouton_to_neuron.json", "w") as json_out:
        json.dump(bouton_to_neuron, json_out)

if __name__ == '__main__':

    for zarr_container in zarr_containers:
        boutons, bouton_to_neuron  = find_boutons(zarr_container)
        create_bouton_to_neuron_json(bouton_to_neuron, zarr_container)
        print("Storing boutons...")
        basename = zarr_container.split('/')[-1]
        f = zarr.open(basename, 'a')
        f['volumes/boutons'] = boutons.astype(np.uint64)
        f['volumes/boutons'].attrs['resolution'] = (93, 62, 62)

    # for each vesicle (from the JSON):
        # look up bouton ID in 'boutons'
        # if 0, continue
        # if != 0, store bouton ID for this vesicle in JSON
