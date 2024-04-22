import neuprint
from heal_skeleton import get_euclidean_distance


def find_closest(synapse, healed_skeleton):

    coords = (synapse['x'], synapse['y'], synapse['z'])
    min_distance = float('inf')
    min_index = -1

    for index, row in healed_skeleton.iterrows():
        distance = get_euclidean_distance(coords, (row['x'], row['y'], row['z']))
        if distance < min_distance:
            min_distance = distance
            min_index = row['rowId']
    return min_index, min_distance


def link_synapse_to_closest(synapses, index, min_index):
    
    synapses.at[index, 'linksTo'] = min_index

def heal_synapses(bodyId, healed_skeleton):

    synapses = neuprint.fetch_synapses(bodyId)
    synapses.to_csv('../data/synapses.csv')
    synapses['linksTo'] = None

    for index, synapse in synapses.iterrows():
        min_index, min_distance = find_closest(synapse, healed_skeleton)
        link_synapse_to_closest(synapses, index, min_index)
    
    synapses.to_csv('../data/linked_synapses.csv')
    return synapses
