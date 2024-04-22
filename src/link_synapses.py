import neuprint
import pandas as pd
from heal_skeleton import get_euclidean_distance


def find_closest(synapse: pd.Series, healed_skeleton: pd.DataFrame) -> tuple:

    """Find the minimum distance and the index of the segment that is the closest neighbor to the selected segment.
    
    Args:
        synapse (pandas.core.series.Series):  A Series representing a single synapse.
        skeleton (pd.DataFrame): DataFrame containing all the segments to find the closest one from.

    Returns:
        tuple: A tuple containing the index (int) and the minimum distance (float) to the closest segment.
    """

    coords = (synapse['x'], synapse['y'], synapse['z'])
    min_distance = float('inf')
    min_index = -1

    for index, row in healed_skeleton.iterrows():
        distance = get_euclidean_distance(coords, (row['x'], row['y'], row['z']))
        if distance < min_distance:
            min_distance = distance
            min_index = row['rowId']
    return min_index, min_distance


def link_synapse_to_closest(synapses: pd.DataFrame, index: int, min_index: int):
    
    """Link the synapse to its closest segment.

    Args:
        synapses (pd.DataFrame): DataFrame containing all the synapses of a selected neuron.
        index (int): An index of the particular synapse to be linked.
        min_index (int): Row index of the closest fragment.
    """

    synapses.at[index, 'linksTo'] = min_index


def link_synapses(bodyId: int, healed_skeleton: pd.DataFrame) -> pd.DataFrame:

    """Link all the synapses of a selected neuron to their closest segments.

    Arguments:
        bodyId (int): ID of the neuron containing the synapses to be linked with their closest segments.

    Returns:
        pd.DataFrame: Synapses of the given neuron with additional column 'linksTo', pointing at the closest segment rowId.
    """

    synapses = neuprint.fetch_synapses(bodyId)
    synapses.to_csv('../data/synapses.csv')
    synapses['linksTo'] = None

    for index, synapse in synapses.iterrows():
        min_index, min_distance = find_closest(synapse, healed_skeleton)
        link_synapse_to_closest(synapses, index, min_index)
    
    synapses.to_csv('../data/linked_synapses.csv')
    return synapses
