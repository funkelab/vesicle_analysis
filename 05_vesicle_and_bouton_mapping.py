import zarr
import numpy as np
import json
from skimage.measure import regionprops
from scipy import ndimage

zarr_container =  '17_1A_extended_2119-2535_test_volume.zarr'


boutons = zarr.open(zarr_container, 'r')['volumes/boutons']
print(np.shape(boutons))

vesicles = json.load(open('17_1A_extended_2119-2535_vesicles.json'))["vesicles"]
vesicle_to_bouton = {}
bouton_to_vesicle = {}
# count = 0
for vesicle in vesicles: 
	z, y, x = vesicle["z"]//93, vesicle["y"]//62, vesicle["x"]//62
	print(z, y, x)

	if z < np.shape(boutons)[0] and y< np.shape(boutons)[1] and x < np.shape(boutons)[2]: # just doing this because we are using testing voluem for now 
		print(np.shape(boutons))
		bouton_id = int(boutons[z, y, x])
		if bouton_id != 23 and bouton_id != 19: # JUST FOR DEBUGGING
			continue
		if bouton_id == 0:
			continue
		if bouton_id in bouton_to_vesicle:
			bouton_to_vesicle[bouton_id].append(vesicle["vesicle_id"])
		else:
			bouton_to_vesicle[bouton_id] = [vesicle["vesicle_id"]]

		vesicle_to_bouton[vesicle["vesicle_id"]] = bouton_id

		# count +=1
			#print("in bouton")
	# if count >=5:
	# 	break


data = {}

data["vesicle_to_bouton"] = vesicle_to_bouton
data["bouton_to_vesicle"] = bouton_to_vesicle
with open(zarr_container.split('/')[-1][:-5]+"_vesicle_to_bouton.json", "w") as json_out:
    json.dump(data, json_out, indent=4)


