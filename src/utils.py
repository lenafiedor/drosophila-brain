import os
import math
import pandas as pd
import neuprint
from bokeh.plotting import figure
from bokeh.io.export import export_png
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


current_dir = os.path.dirname(os.path.realpath(__file__))


def plot_neuron(filepath, bodyId):

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    
    if not filepath:
        n = neuprint.fetch_neuron(bodyId)
    else:
        n = pd.read_csv(filepath)
    
    plot = figure()
    no_child = n[n['link'] == -1]
    child = n[n['link'] != -1]
    plot.scatter(child['x'], child['z'], color='lightblue')
    plot.scatter(no_child['x'], no_child['z'], color='red')
    
    export_png(plot, filename=f'{current_dir}/../images/skeleton_{bodyId}.png', webdriver=driver)
    driver.quit()


def get_euclidean_distance(coords_first: tuple, coords_second:tuple) -> float:

    """Calculate the distance between two points in the Euclidean space.
    
    Args:
        coords_selected (tuple): Euclidean coordinates of the first segment (x, y, z).
        coords_second (tuple): Euclidean coordinates of the second segment (x, y, z).

    Returns:
        float: The Euclidean distance between the two points.
    """

    return math.sqrt((coords_first[0]-coords_second[0])**2 + (coords_first[1]-coords_second[1])**2 + (coords_first[2]-coords_second[2])**2)
