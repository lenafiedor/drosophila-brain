import bokeh.plotting
import neuprint
import numpy as np
import pandas as pd

import bokeh
import hvplot.pandas
import holoviews as hv


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImxlbmFmaWVkb3IwMkBnbWFpbC5jb20iLCJsZXZlbCI6Im5vYXV0aCIsImltYWdlLXVybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lNN3drbnQwYmtuTHpKXzhtQ3g2LTZ3Q1l3WDdBRG9qUDVKNWxLSEk3VGJvQT1zOTYtYz9zej01MD9zej01MCIsImV4cCI6MTg4MDY0NDM2OX0.MKNdbzhz7uOgWZiu1zTcu9sSDz6zJeRGpg8RjjvaEOw"
c = neuprint.Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token=TOKEN)
neuprint.set_default_client(c)


# fetch neurons using API; creates the same output
neuron_criteria = neuprint.NeuronCriteria(bodyId=5813087532)
neuron_df, _ = neuprint.fetch_neurons(neuron_criteria)
print(neuron_df[['bodyId', 'type', 'instance', 'pre', 'post', 'size']])

# fetch TBars and PSDs for the selected neuron
tbar_criteria = neuprint.SynapseCriteria(type='pre')
tbars = neuprint.fetch_synapses(neuron_criteria, tbar_criteria)
psd_criteria = neuprint.SynapseCriteria(type='post')
psds = neuprint.fetch_synapses(neuron_criteria, psd_criteria)

# plot the TBars positions
# p = bokeh.plotting.figure()
# p.scatter(tbars['x'], tbars['y'])
# p.y_range.flipped = True
# bokeh.plotting.show(p)

syn_criteria = neuprint.SynapseCriteria(primary_only=True)
conns = neuprint.fetch_synapse_connections(neuron_criteria, None, syn_criteria)

# search for synapses with no postsynaptic neuron (???)
posts, _ = neuprint.fetch_neurons(conns['bodyId_post'])
no_post = conns[conns['bodyId_post'].isna()]
