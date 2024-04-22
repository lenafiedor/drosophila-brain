import neuprint
import math

from bokeh.plotting import figure
from bokeh.io import export_png


def plot_neuron(bodyId):

    n = neuprint.fetch_skeleton(bodyId)
    plot = figure()
    plot.scatter(n['x'], n['z'])
    export_png(plot, filename=f'../images/skeleton_{bodyId}.png')


def get_euclidean_distance(coords_first: tuple, coords_second:tuple) -> float:

    """Calculate the distance between two points in the Euclidean space.
    
    Args:
        coords_selected (tuple): Euclidean coordinates of the first segment (x, y, z).
        coords_second (tuple): Euclidean coordinates of the second segment (x, y, z).

    Returns:
        float: The Euclidean distance between the two points.
    """

    return math.sqrt((coords_first[0]-coords_second[0])**2 + (coords_first[1]-coords_second[1])**2 + (coords_first[2]-coords_second[2])**2)
