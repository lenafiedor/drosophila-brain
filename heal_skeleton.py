import neuprint
from link_closest import find_closest, link_closest


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImxlbmFmaWVkb3IwMkBnbWFpbC5jb20iLCJsZXZlbCI6Im5vYXV0aCIsImltYWdlLXVybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lNN3drbnQwYmtuTHpKXzhtQ3g2LTZ3Q1l3WDdBRG9qUDVKNWxLSEk3VGJvQT1zOTYtYz9zej01MD9zej01MCIsImV4cCI6MTg4MDY0NDM2OX0.MKNdbzhz7uOgWZiu1zTcu9sSDz6zJeRGpg8RjjvaEOw"
c = neuprint.Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token=TOKEN)
neuprint.set_default_client(c)


# fetch skeleton for the neuron of interest
bodyId = 5813087532
skeleton = neuprint.fetch_skeleton(body=bodyId, format='pandas')
skeleton.to_csv('skeleton.csv')
no_link = skeleton[skeleton['link'] == -1]

for index, segment in no_link.iterrows():
    min_index, min_dist = find_closest(segment, skeleton.drop(index))
    link_closest(skeleton, index, min_index)

skeleton.to_csv('healed_skeleton.csv')