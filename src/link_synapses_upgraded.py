import numpy as np
import pandas as pd
import os
import neuprint
from utils import get_euclidean_distance
from link_synapses import link_synapse_to_closest


def find_closest_upgraded(synapse: pd.Series, healed_skeleton: pd.DataFrame, num_segments: int, threshold: int = 100) -> tuple:

    """Find the index of the two segments that are the given synapse's closest neighbors.
    
    Args:
        synapse (pandas.core.series.Series): A Series representing a single synapse.
        skeleton (pd.DataFrame): DataFrame containing all the segments to find the two closest ones from.
        num_segments (int): The number of initial segments.
        threshold (int): Maximum distance between synapse and segments to calculate the distance within.
            For example, if threshold = 100, the difference between xyz coordinates of the synapse and of the segment must be at most equal to 100.
            Otherwise, distance is not calculated.
            WARNING: When too low, find_closest function may not link some synapses to any segment.
    
    Returns:
        tuple: A tuple containing the indices of the two closest segments to the given synapse.
    """

    coords = (float(synapse['x']), float(synapse['y']), float(synapse['z']))

    min_parent_index = -1
    min_parent_distance = float('inf')

    for _, row in healed_skeleton[:num_segments].iterrows():
        if (abs(coords[0] - row['x']) <= threshold and abs(coords[1] - row['y']) <= threshold and abs(coords[2] - row['z']) <= threshold):

            selected_coords = float(row['x']), float(row['y']), float(row['z'])
            distance = get_euclidean_distance(coords, selected_coords)
            if distance < min_parent_distance:

                min_parent_distance = distance
                min_parent_index = row['rowId']

                children = healed_skeleton[healed_skeleton['link'] == min_parent_index]
                parent = healed_skeleton[healed_skeleton['rowId'] == row['link']]

                min_child_index = -1
                min_child_distance = float('inf')

                if not children.empty:
                    for _, child in children.iterrows():
                        child_coords = float(child['x']), float(child['y']), float(child['z'])
                        distance = get_euclidean_distance(coords, child_coords)
                        if distance < min_child_distance:
                            min_child_distance = distance
                            min_child_index = child['rowId']                    

                if not parent.empty:
                    parent_coords = float(parent['x'].iloc[0]), float(parent['y'].iloc[0]), float(parent['z'].iloc[0])
                    distance = get_euclidean_distance(coords, parent_coords)
                    if distance < min_child_distance:
                        min_child_distance, min_parent_distance = min_parent_distance, distance 
                        min_child_index, min_parent_index = min_parent_index, parent['rowId'].iloc[0]
                
                if parent.empty and children.empty:
                    min_child_index, min_child_distance = min_parent_index, min_parent_distance
    
    return int(min_child_index), int(min_parent_index)


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

    # if S1 and S2 are the same point, return S1 (or S2) as the intersection point
    if np.all(V < 10e-6):
        return tuple(S1)

    # calculate t parameter
    t_param = np.dot(D, V) / np.dot(V, V)
    
    # return intersection point
    return tuple(S1 + t_param * V)


def calculate_radius(R1: float, R2: float, coords_first: tuple, coords_second: tuple, selected_coords: tuple) -> float:

    """Calculate the radius of a new segment.
    Mathematically said: calculate the radius of a conical frustrum for a given height (based on triangle similarity).
    
    Args:
        R1 (float): Radius of the first segment.
        R2 (float): Radius of the second segment.
        coords_first (tuple): Coordinates (xyz) of the first segment.
        coords_second (tuple): Coordinates (xyz) of the second segment.
        selected_coords (tuple): Coordinates of the intersection point of the line defined by two segments
        and the perpendicular line passing through a given synapse.

    Returns:
        float: The radius of the new segment.
    """

    if R1 < R2:
        R1, R2 = R2, R1
        coords_first, coords_second = coords_second, coords_first
    
    if coords_first == coords_second:
        return R1
    
    distance = get_euclidean_distance(coords_first, coords_second)
    h0 = get_euclidean_distance(coords_first, selected_coords)

    return R2 + (((R1 - R2) * abs(distance - h0)) / distance)


def update_skeleton(healed_skeleton: pd.DataFrame, new_coords: tuple, row_id: int, min_child_index: int, min_parent_index: int,
                    child_coords: tuple, parent_coords: tuple):
    
    """Add a new row representing a segment to the DataFrame of all segments.

    Args:
        healed_skeleton (pd.DataFrame): DataFrame containing all the segments.
        new_coords (tuple): The coordinates of the new segment.
        row_id (int): Row ID of the new segment.
        min_child_index (int): Index of the nearest child segment.
        min_parent_index (int): Index of the nearest parent segment.
        child_coords (tuple): The coordinates of the child segment.
        parent_coords (tuple): The coordinates of the parent segment.

    Returns:
        pd.DataFrame: Updated DataFrame with the new segment added.
    """

    radius = calculate_radius(healed_skeleton.at[min_child_index - 1, 'radius'], healed_skeleton.at[min_parent_index - 1, 'radius'],
                              child_coords, parent_coords, new_coords)
    
    new_segment = pd.DataFrame({'rowId': [row_id], 'x': [round(new_coords[0], 1)], 'y': [round(new_coords[1], 1)],
                                'z': [round(new_coords[2], 1)], 'radius': [round(radius, 4)], 'link': [min_parent_index]})
    
    healed_skeleton = pd.concat([healed_skeleton, new_segment], ignore_index=True)
    healed_skeleton.at[min_child_index - 1, 'link'] = row_id

    return healed_skeleton


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
    num_segments = healed_skeleton.shape[0] + 1
    row_id = healed_skeleton['rowId'].iloc[-1] + 1

    for index, synapse in synapses.iterrows():
        min_child_index, min_parent_index = find_closest_upgraded(synapse, healed_skeleton, num_segments)
        
        child = healed_skeleton[healed_skeleton['rowId'] == min_child_index]
        parent = healed_skeleton[healed_skeleton['rowId'] == min_parent_index]

        child_coords = tuple(child[['x', 'y', 'z']].iloc[0])
        parent_coords = tuple(parent[['x', 'y', 'z']].iloc[0])
        synapse_coords = (synapse['x'], synapse['y'], synapse['z'])

        new_coords = find_intersection_point(child_coords, parent_coords, synapse_coords)
        healed_skeleton = update_skeleton(healed_skeleton, new_coords, row_id, min_child_index, min_parent_index, child_coords, parent_coords)
        
        link_synapse_to_closest(synapses, index, row_id)
        row_id += 1

    healed_skeleton = healed_skeleton.drop('Unnamed: 0', axis=1)
    synapses.to_csv(f'{current_dir}/../data/linked_synapses_upgraded_{bodyId}.csv')
    healed_skeleton.to_csv(f'{current_dir}/../data/healed_skeleton_upgraded_{bodyId}.csv')
    
    return synapses
