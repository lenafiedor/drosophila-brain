from heal_skeleton import heal_skeleton
import link_synapses
import neuprint
import sys


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImxlbmFmaWVkb3IwMkBnbWFpbC5jb20iLCJsZXZlbCI6Im5vYXV0aCIsImltYWdlLXVybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lNN3drbnQwYmtuTHpKXzhtQ3g2LTZ3Q1l3WDdBRG9qUDVKNWxLSEk3VGJvQT1zOTYtYz9zej01MD9zej01MCIsImV4cCI6MTg4MDY0NDM2OX0.MKNdbzhz7uOgWZiu1zTcu9sSDz6zJeRGpg8RjjvaEOw"
c = neuprint.Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token=TOKEN)
neuprint.set_default_client(c)


# a default value for bodyId of the neuron, can also be passed as a command line argument
bodyId = 5813087532

try:
    bodyId = int(sys.argv[1])
except IndexError:
    print('No bodyId passed, calculating the default one')

healed_skeleton = heal_skeleton(bodyId)
# plot_neuron(bodyId)
link_synapses.heal_synapses(bodyId, healed_skeleton)