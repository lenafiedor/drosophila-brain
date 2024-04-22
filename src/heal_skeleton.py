import neuprint
import pandas as pd
from utils import get_euclidean_distance


def find_closest(segment: pd.Series, skeleton: pd.DataFrame) -> tuple:

    """Find the minimum distance and the index of the segment that is the closest neighbor to the selected segment.
    
    Args:
        segment (pandas.core.series.Series):  A Series representing a segment with no link.
        skeleton (pd.DataFrame): DataFrame containing all the segments to find the neighbour from.

    Returns:
        tuple: A tuple containing the index (int) and the minimum distance (float) to the closest neighbor segment.
    """

    coords_selected = (segment['x'],  segment['y'], segment['z'])
    min_distance = float('inf')
    min_index = -1

    for index, row in skeleton.iterrows():
        coords = (row['x'], row['y'], row['z'])
        distance = get_euclidean_distance(coords_selected, coords)
        if distance < min_distance and segment['rowId'] != row['rowId']:
            min_distance = distance
            min_index = row['rowId']
    
    return min_index, min_distance


def link_fragment_to_closest(skeleton: pd.DataFrame, index: int, min_index: int):

    """Link the segment to its closest neighbour.

    Args:
        skeleton (pd.DataFrame): DataFrame containing all the segments.
        index (int): An index of the segment with no link.
        min_index (int): Row index of the closest neighbour.
    """

    skeleton.at[index, 'link'] = min_index


def heal_skeleton(bodyId: int):

    """Link all the segments with no children to their closest neighbours.

    Args:
        bodyId (int): ID of the neuron to be healed.

    Returns:
        pd.DataFrame: Healed skeleton of the given neuron.
    """
    
    skeleton = neuprint.fetch_skeleton(body=bodyId, format='pandas')
    skeleton.to_csv('../data/skeleton.csv')
    no_link = skeleton[skeleton['link'] == -1]

    for index, segment in no_link.iterrows():
        min_index, min_distance = find_closest(segment, skeleton)
        link_fragment_to_closest(skeleton, index, min_index)

    skeleton.to_csv('../data/healed_skeleton.csv')
    return skeleton