import zarr
import numpy as np
import json
from skimage.measure import regionprops
from scipy import ndimage

dataset_name = "17_1A_extended_2119-2535"
bouton_zarr =  f'{dataset_name}_converted_2_consolidated.zarr'
zarr_container = f'/nrs/funke/sheridana/hausser/paintera_ingest/new_test_vols_2_14_22/{dataset_name}_converted_2_consolidated.zarr'


def distance_to_object(zarr_container, object_type):

    if object_type == 'mito':
        print("Reading mitochondria segmentation...")
        objects = zarr.open(zarr_container, 'r')['volumes/mito'][:, :, :]

    if object_type == 'az':
        print("Reading active zone segmentation...")
        objects = zarr.open(zarr_container, 'r')['volumes/synapses'][:, :, :]

    print("Reading bouton segmentation...")
    boutons = zarr.open(bouton_zarr, 'r')['volumes/boutons'][:, :, :]

    bouton_to_vesicle = json.load(open(f"temp/{dataset_name}_vesicle_to_bouton.json"))["bouton_to_vesicle"]

    bouton_to_vesicle = {
    int(k): v
    for k, v in bouton_to_vesicle.items()
    }
    print("BOUTON TO VESICLE")
    print(bouton_to_vesicle)

    vesicles = json.load(open(f'temp/{dataset_name}_vesicles.json'))["vesicles"]
    vesicles = {
        vesicle['vesicle_id']: vesicle
        for vesicle in vesicles
    }


    props = regionprops(boutons)
    obj_distance_list = {}
    bounding_boxes = {}
    for prop in props:
        bounding_boxes[prop.label] = prop.bbox

    distance_to_outside = {}

    for label, area in bounding_boxes.items():
        z_left, y_left, x_left, z_right, y_right, x_right = area[0], area[1], area[2], area[3], area[4], area[5]
        if z_left != 0:
            z_left -= 1
        if y_left != 0:
            if y_left < 5: 
                y_left = 0
            y_left -= 5
        if x_left != 0:
            if x_left < 5: 
                x_left = 0
            x_left -= 5
        if z_right != np.shape(boutons)[0]:
            z_right += 1
        if y_right != np.shape(boutons)[1]:
            if y_right > np.shape(boutons)[1] - 5:
                y_right = np.shape(boutons)[1]
            y_right = y_right + 5
        if x_right != np.shape(boutons)[2]:
            if x_right > np.shape(boutons)[2] - 5:
                x_right = np.shape(boutons)[2]
            x_right = x_right + 5

        obj_crop = objects[z_left:z_right, y_left:y_right, x_left:x_right]
        obj_crop[obj_crop > 0] = 1
        bouton_crop = boutons[z_left:z_right, y_left:y_right, x_left:x_right] == label
        combined_crop = 1 - obj_crop*bouton_crop
        dist_transform = ndimage.distance_transform_edt(combined_crop, sampling=[93,62,62])
        dist_transform_boundary = ndimage.distance_transform_edt(bouton_crop, sampling=[93,62,62])

        z, y, x = [], [], []
        obj_distances = {}
        if label in bouton_to_vesicle:
            for vesicle_id in bouton_to_vesicle[label]:
                vesicle = vesicles[vesicle_id]
                shifted_z = int(vesicle["z"]/93) - z_left
                shifted_y = int(vesicle["y"]/62) - y_left
                shifted_x = int(vesicle["x"]/62) - x_left
                z.append(shifted_z)
                y.append(shifted_y)
                x.append(shifted_x)

                if (shifted_z < (z_right - z_left)) and (shifted_y < (y_right - y_left)) and (shifted_x < (x_right - x_left)) and shifted_z >= 0 and shifted_y >= 0 and shifted_x >= 0:
                    distance_to_outside[vesicle_id] = dist_transform_boundary[shifted_z, shifted_y, shifted_x]
                    obj_distances[vesicle_id] = dist_transform[shifted_z, shifted_y, shifted_x]
        obj_distance_list = {**obj_distance_list, **obj_distances}

    data = {}

    data["vesicle_distance_to_"+object_type] = obj_distance_list
    data["vesicle_distance_to_boundary"] = [distance_to_outside]


    with open(f'temp/{dataset_name}_vesicle_dist_to_{object_type}.json', "w") as json_out:
        json.dump(data, json_out, indent=4)

if __name__ == '__main__':

    distance_to_object(zarr_container, 'mito')
    distance_to_object(zarr_container, 'az')
