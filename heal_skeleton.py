import neuprint
import math
import pandas as pd


def get_euclidean_distance(coords_first: tuple, coords_second:tuple) -> float:

    """Calculate the distance between two points in the Euclidean space.
    
    Args:
        coords_selected (tuple): Euclidean coordinates of the first segment (x, y, z).
        coords_second (tuple): Euclidean coordinates of the second segment (x, y, z).

    Returns:
        float: The Euclidean distance between the two points.
    """

    return math.sqrt((coords_first[0]-coords_second[0])**2 + (coords_first[1]-coords_second[1])**2 + (coords_first[2]-coords_second[2])**2)


def find_closest(segment: pd.Series, skeleton: pd.DataFrame) -> tuple:

    """Find the minimum distance and the index of the segment that is the closest neighbor to the selected segment.
    
    Args:
        segment (pandas.core.series.Series):  A Series representing a segment with no link.
        skeleton (pd.DataFrame): DataFrame containing all the segments to find the neighbour from.

    Returns:
        tuple: A tuple containing the index (int) and the minimum distance (float) of the closest neighbor segment.
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


def link_closest(skeleton: pd.DataFrame, index: int, min_index: int):

    """Link the segment to its closest neighbour.

    Args:
        skeleton (pd.DataFrame): DataFrame containing all the segments.
        index (int): An index of the segment with no link.
        min_index (int): Row index of the closest neighbour.
    """

    skeleton.at[index, 'link'] = min_index


def heal_skeleton(bodyId: int):

    """Link all the segments with no children to their closest neighbours.

    Arguments:
        bodyId (int): ID of the neuron to be healed.
    """
    
    skeleton = neuprint.fetch_skeleton(body=bodyId, format='pandas')
    skeleton.to_csv('skeleton.csv')
    no_link = skeleton[skeleton['link'] == -1]

    for index, segment in no_link.iterrows():
        min_index, _ = find_closest(segment, skeleton.drop(index))
        link_closest(skeleton, index, min_index)

    skeleton.to_csv('healed_skeleton.csv')
