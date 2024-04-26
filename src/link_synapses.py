import neuprint
import pandas as pd
import os
from heal_skeleton import get_euclidean_distance


def find_closest(synapse: pd.Series, healed_skeleton: pd.DataFrame, threshold: int = 100) -> tuple:

    """Find the minimum distance and the index of the segment that is the closest neighbor to the selected segment.
    
    Args:
        synapse (pandas.core.series.Series): A Series representing a single synapse.
        skeleton (pd.DataFrame): DataFrame containing all the segments to find the closest one from.
        threshold (int): Maximum distance between synapse and segments to calculate the distance within.
            For example, if threshold = 100, the difference between xyz coordinates of the synapse and of the segment must be at most equal to 100.
            Otherwise, distance is not calculated.
            WARNING: When too low, find_closest function may not link some synapses to any segment.
    
    Returns:
        tuple: A tuple containing the index (int) and the minimum distance (float) to the closest segment.
    """

    coords = (synapse['x'], synapse['y'], synapse['z'])
    min_distance = float('inf')
    min_index = -1

    for index, row in healed_skeleton.iterrows():
        if (abs(coords[0] - row['x']) <= threshold and abs(coords[1] - row['y']) <= threshold and abs(coords[2] - row['z']) <= threshold):
            distance = get_euclidean_distance(coords, (row['x'], row['y'], row['z']))
            if distance < min_distance:
                min_distance = distance
                min_index = row['rowId']
    return int(min_index), min_distance


def link_synapse_to_closest(synapses: pd.DataFrame, index: int, min_index: int):
    
    """Link the synapse to its closest segment.

    Args:
        synapses (pd.DataFrame): DataFrame containing all the synapses of a selected neuron.
        index (int): An index of the particular synapse to be linked.
        min_index (int): Row index of the closest fragment.
    """

    synapses.at[index, 'linksTo'] = min_index


def link_synapses(bodyId: int, healed_skeleton: pd.DataFrame = None) -> pd.DataFrame:

    """Link all the synapses of a selected neuron to their closest segments.

    Arguments:
        bodyId (int): ID of the neuron containing the synapses to be linked with their closest segments.

    Returns:
        pd.DataFrame: Synapses of the given neuron with additional column 'linksTo', pointing at the closest segment rowId.
    """

    current_dir = os.path.dirname(os.path.realpath(__file__))

    if not healed_skeleton:
        healed_skeleton = pd.read_csv(f'../data/healed_skeleton_{bodyId}.csv')
    
    synapses = neuprint.fetch_synapses(bodyId)
    synapses.to_csv(f'{current_dir}/../data/synapses_{bodyId}.csv')
    synapses['linksTo'] = None

    for index, synapse in synapses.iterrows():
        min_index, min_distance = find_closest(synapse, healed_skeleton)
        print(f'minimal distance: {min_distance}, linking synapse no. {index} to segment no. {min_index}')
        link_synapse_to_closest(synapses, index, min_index)
    
    synapses.to_csv(f'{current_dir}/../data/linked_synapses_{bodyId}.csv')
    return synapses
