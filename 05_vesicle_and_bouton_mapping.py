import zarr
import numpy as np
import json
from skimage.measure import regionprops
from scipy import ndimage

dataset_name = "17_1A_extended_2119-2535" 
bouton_zarr = f"{dataset_name}_converted_2_consolidated.zarr"

boutons = zarr.open(bouton_zarr, 'r')['volumes/boutons']
print(np.shape(boutons))

vesicles = json.load(open(f'temp/{dataset_name}_vesicles.json'))["vesicles"]
vesicle_to_bouton = {}
bouton_to_vesicle = {}
# count = 0
for vesicle in vesicles:
    z, y, x = vesicle["z"]//93, vesicle["y"]//62, vesicle["x"]//62
    #z, y, x = vesicle["z"]//93, vesicle["y"]//62, vesicle["x"]//62
    #print(z, y, x)
    #print(np.shape(boutons)[0], np.shape(boutons)[1], np.shape(boutons)[2])
    if z < np.shape(boutons)[0] and y< np.shape(boutons)[1] and x < np.shape(boutons)[2] and z > 0 and y > 0 and x > 0:
        bouton_id = int(boutons[z, y, x])
        if bouton_id == 0:
            continue
        if bouton_id in bouton_to_vesicle:
            bouton_to_vesicle[bouton_id].append(vesicle["vesicle_id"])
        else:
            bouton_to_vesicle[bouton_id] = [vesicle["vesicle_id"]]

        vesicle_to_bouton[vesicle["vesicle_id"]] = bouton_id

data = {}

data["vesicle_to_bouton"] = vesicle_to_bouton
data["bouton_to_vesicle"] = bouton_to_vesicle
with open(f"temp/{dataset_name}_vesicle_to_bouton.json", "w") as json_out:
    json.dump(data, json_out, indent=4)


