import json

dataset_name = "17_1A_extended_2119-2535"

# VESICLES
# csv info, bouton id, distance to az, distance to mito, distance to boundary

vesicle_dict = json.load(open(f'temp/{dataset_name}_vesicles.json'))["vesicles"]
vesicles = {
        vesicle['vesicle_id']:vesicle
        for vesicle in vesicle_dict
        }


vesicle_to_bouton =json.load(open(f'temp/{dataset_name}_vesicle_to_bouton.json'))["vesicle_to_bouton"]
vesicle_to_bouton = {
        int(k): v
        for k, v in vesicle_to_bouton.items()
        }

distance_to_az = json.load(open(f'temp/{dataset_name}_vesicle_dist_to_az.json'))['vesicle_distance_to_az']
distance_to_boundary = json.load(open(f'temp/{dataset_name}_vesicle_dist_to_az.json'))['vesicle_distance_to_boundary'][0]
distance_to_mito = json.load(open(f'temp/{dataset_name}_vesicle_dist_to_mito.json'))['vesicle_distance_to_mito']
#print("DISTANCE TO BOUNDARY")
#print(distance_to_boundary[0])
for vesicle in vesicles:
    #print("VESICLE ID", vesicle)
    #print("VESICLES[VESICLE]", vesicles[vesicle])
    #print("VESICLE_TO_BOUTON[vesicle]", vesicle_to_bouton[vesicle])
    if vesicle in vesicle_to_bouton:
        vesicles[vesicle]["bouton_id"] = vesicle_to_bouton[vesicle]
    if str(vesicle) in distance_to_az:
        vesicles[vesicle]["distance_to_az"] = distance_to_az[str(vesicle)]
    if str(vesicle) in distance_to_boundary:
        vesicles[vesicle]["distance_to_boundary"] = distance_to_boundary[str(vesicle)]
    if str(vesicle) in distance_to_mito:
        vesicles[vesicle]["distance_to_mito"] = distance_to_mito[str(vesicle)]

#print(vesicles)
# BOUTONS
# id, neuron id, volume, vesicles

bouton_dict = json.load(open(f'temp/{dataset_name}_boutons.json'))
#print(bouton_dict)
bouton_to_vesicle = json.load(open(f"temp/{dataset_name}_vesicle_to_bouton.json"))["bouton_to_vesicle"]
    
bouton_to_vesicle = {
	int(k): v
	for k, v in bouton_to_vesicle.items()
}

#print("BOUTON TO VESICLE")
#print(bouton_to_vesicle)
for bouton_id in bouton_dict:
    if bouton_id in bouton_to_vesicle:
        bouton_dict[bouton_id]['vesicles'] = bouton_to_vesicle[bouton_id]
#print("BOUTON_DICT")
#print(bouton_dict)

# MITOCHONDRIA/ACTIVE ZONES
# id, neuron id, bouton id, volume

az_to_neuron_dict = json.load(open(f'temp/{dataset_name}_azs_to_neurons.json'))["azs"]
mito_to_neuron_dict = json.load(open(f'temp/{dataset_name}_mitos_to_neurons.json'))["mitos"]
az_to_bouton_dict = json.load(open(f'temp/{dataset_name}_azs_to_boutons.json'))["azs"]
mito_to_bouton_dict = json.load(open(f'temp/{dataset_name}_mitos_to_boutons.json'))["mitos"]

azs_neurons = {
    az["az_id"]: az
    for az in az_to_neuron_dict
    }
azs_boutons = {
    az["az_id"]: az
    for az in az_to_bouton_dict
    }
for az in azs_neurons:
    azs_neurons[az]["bouton_id"] = azs_boutons[az]["bouton_id"]
#print(azs_neurons)

mitos_neurons = {
    mito["mito_id"]: mito
    for mito in mito_to_neuron_dict
    }
mitos_boutons = {
    mito["mito_id"]: mito
    for mito in mito_to_bouton_dict
    }
for mito in mitos_neurons:
    mitos_neurons[mito]["bouton_id"] = azs_boutons[az]["bouton_id"]
#print(mitos_neurons)
# COMBINE
combined_dicts = {"vesicles": vesicles, "boutons":bouton_dict["boutons"],
        "active_zones": azs_neurons, "mitos": mitos_neurons} # add vesicles here

#print(combined_dicts)

with open(f'stats_{dataset_name}.json', 'w') as json_out:
	json.dump(combined_dicts, json_out, indent=4)
