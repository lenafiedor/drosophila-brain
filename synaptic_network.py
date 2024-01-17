import numpy as np
from itertools import product


def get_distance(p1: int, p2: int, xyz: np.ndarray) -> np.linalg.norm:
    "This function calculates the distance between two points in the Euclidean space."
    return np.linalg.norm(xyz[p1-1] - xyz[p2-1])

def find_closest(pos: list[int], gCCpos: list[int], xyz: np.ndarray) -> tuple:
    "This function finds two closest neural segments"
    min_distance = float('inf')
    closest_points = None

    for i, j, k in product(['child', 'parent'], ['child', 'parent'], [-1, 1]): # k = range(pos)???
        print(f'i, j, k: {i}, {j}, {k}')
        candidate = [
            x for x in sorted(
                range(len(xyz)),
                key = lambda x: get_distance(pos[k], x, xyz),
            ) if x in gCCpos and x != pos[k]
        ][:20]
        
        if candidate:
            print(f'candidate: {candidate}')
            candidate = candidate[0]
            distance = get_distance(pos[k], candidate, xyz)
            print(f'distance: {distance}, min_distance: {min_distance}')

            if distance < min_distance:
                print('changing distance')
                min_distance = distance
                closest_points = ((candidate, i), (pos[k], j), distance)

    return closest_points

def link_closest(data, find):
    if None in find:
        return None
    
    temp = [item for sublist in [data[find[0][0] - 1], data[find[1][0] - 1]] for item in sublist]
    print(f'temp: {temp}')

    if -1 in temp:
        if -1 in temp[0]:
            updated_index = find[0][0], 2
            replacement_index = find[1][0], 1 if find[1][1] == 'child' else 3
        else:
            updated_index = find[1][0], 2
            replacement_index = find[0][0], 1 if find[0][1] == 'child' else 3
    elif set(x[1] for x in find[0:2]) == {'parent'}:
        updated_index = find[0][0], 3
        replacement_index = find[1][0], 3
    else:
        return data

    data[updated_index[0]][updated_index[1]] = temp[replacement_index[1]]
    return data


positions = [387, 388, 389, 390, 391, 392, 393]
graph_connected_component = [387, 388, 389, 390, 391, 392, 393]
coordinates = np.array([
    [1.0, 2.0, 3.0],
    [1.0, 2.0, 4.0],
    [7.0, 8.0, 9.0],
    [10.0, 11.0, 12.0],
    [13.0, 14.0, 15.0],
    [16.0, 17.0, 18.0],
    [19.0, 20.0, 25.0]
])

find = find_closest(positions, graph_connected_component, coordinates)
print(find)

data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

link = link_closest(data, find)
print(link)