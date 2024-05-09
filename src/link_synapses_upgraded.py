import numpy as np
import pandas as pd
import os
import neuprint
from utils import get_euclidean_distance


def find_closest_upgraded(synapse: pd.Series, healed_skeleton: pd.DataFrame, threshold: int = 100) -> tuple:

    """Find the index of the two segments that are the given synapse's closest neighbors.
    
    Args:
        synapse (pandas.core.series.Series): A Series representing a single synapse.
        skeleton (pd.DataFrame): DataFrame containing all the segments to find the two closest ones from.
        threshold (int): Maximum distance between synapse and segments to calculate the distance within.
            For example, if threshold = 100, the difference between xyz coordinates of the synapse and of the segment must be at most equal to 100.
            Otherwise, distance is not calculated.
            WARNING: When too low, find_closest function may not link some synapses to any segment.
    
    Returns:
        tuple: A tuple containing the indices of the two closest segments to the given synapse.
    """

    coords = (synapse['x'], synapse['y'], synapse['z'])
    min_index = -1
    min_distance = float('inf')

    for _, row in healed_skeleton.iterrows():
        if (abs(coords[0] - row['x']) <= threshold and abs(coords[1] - row['y']) <= threshold and abs(coords[2] - row['z']) <= threshold):
            distance = get_euclidean_distance(coords, (row['x'], row['y'], row['z']))
            if distance < min_distance:

                min_distance = distance
                min_index = row['rowId']

                children = healed_skeleton[healed_skeleton['link'] == min_index]
                parent = healed_skeleton[healed_skeleton['rowId'] == row['link']]

                min_neighbor_index = -1
                min_neighbor_distance = float('inf')

                for _, child in children.iterrows():
                    distance = get_euclidean_distance(coords, (child['x'], child['y'], child['z']))
                    if distance < min_neighbor_distance:
                        min_neighbor_distance = distance
                        min_neighbor_index = child['rowId']

                distance = get_euclidean_distance(coords, (parent['x'], parent['y'], parent['z']))
                if distance < min_neighbor_distance:
                    min_neighbor_distance = distance
                    min_neighbor_index = parent['rowId']
    
    return int(min_index), int(min_neighbor_index)


def find_intersection_point(S1: tuple, S2: tuple, synapse: tuple) -> tuple:

    """Find the intersection point in 3D space between a line defined by two segments and the perpendicular line passing through a given synapse.

    Args:
        S1 (tuple): The coordinates of the first segment.
        S2 (tuple): The coordinates of the second segment.
        synpase (tuple): The coordinates of the synapse through which the perpendicular line passes.

    Returns:
        tuple: The coordinates of the intersection point of the two lines.

    Notes:
        If the direction vector of the line is parallel to any axis, the function
        may produce incorrect results.
    """

    # find direction vector and vector from S1 to synapse
    V = np.asarray(S2) - np.asarray(S1)
    D = np.asarray(synapse) - np.asarray(S1)
    
    # find normal vector
    N = np.cross(V, np.array([1, 0, 0]))

    # calculate t parameter
    t_param = np.dot(D, V) / np.dot(V, V)
    
    # return intersection point
    return tuple(S1 + t_param * V)


# TODO: implement this function
def add_segment(coords: tuple, healed_skeleton: pd.DataFrame) -> pd.DataFrame:

    # new_row = pd.DataFrame([-1, *coords, 0, -1])
    # healed_skeleton = pd.concat([healed_skeleton, new_row], ignore_index=True)
    pass


def link_synapses_upgraded(bodyId: int, healed_skeleton: pd.DataFrame = None) -> pd.DataFrame:

    """Link all the synapses of a selected neuron to a line between their two closest segments and create a new segment there.

    Args:
        bodyId (int): ID of the neuron containing the synapses to be linked with their closest segments.

    Returns:
        pd.DataFrame: Synapses of the given neuron with additional column 'linksTo', pointing at the closest segment rowId.
    """

    current_dir = os.path.dirname(os.path.realpath(__file__))

    if not healed_skeleton:
        healed_skeleton = pd.read_csv(f'{current_dir}/../data/healed_skeleton_{bodyId}.csv')
    
    synapses = neuprint.fetch_synapses(bodyId)
    synapses.to_csv(f'{current_dir}/../data/synapses_{bodyId}.csv')
    synapses['linksTo'] = None

    for index, synapse in synapses.iterrows():
        min_index, min_neighbor_index = find_closest_upgraded(synapse, healed_skeleton)
        print(f'Linking synapse no. {index} to segment no. {min_index}')
        print(f'Neighbor\'s rowId: {min_neighbor_index}')
        
        S1 = healed_skeleton[healed_skeleton['rowId'] == min_index]
        S2 = healed_skeleton[healed_skeleton['rowId'] == min_neighbor_index]

        S1_coords = tuple(S1[['x', 'y', 'z']].iloc[0])
        S2_coords = tuple(S2[['x', 'y', 'z']].iloc[0])

        new_coords = find_intersection_point(S1_coords, S2_coords, (synapse['x'], synapse['y'], synapse['z']))
        print(f'New segment at: {new_coords}')
        add_segment(new_coords, healed_skeleton)

    # TODO: modify healed skeleton and synapses CSV files by adding new segments and links
    # synapses.to_csv(f'{current_dir}/../data/linked_synapses_{bodyId}.csv')
    # healed_skeleton.to_csv(f'{current_dir}/../data/linked_synapses_{bodyId}.csv')
    
    return synapses
