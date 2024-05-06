import matplotlib.pyplot as plt

def line_equation_2D(point1, point2):

    """
    Calculate the equation of the line passing through two points in cartesian space.
    
    Args:
    - point1 (tuple): Coordinates of the first point (x1, y1)
    - point2 (tuple): Coordinates of the second point (x2, y2)
    
    Returns:
    - tuple: Coefficients (a, b) of the line equation: y = ax + b
    """

    x1, y1 = point1
    x2, y2 = point2

    # find a and b coefficients
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1

    return (slope, intercept)


def cross_point_2D(equation, point):

    """
    Calculate the coordinates of a cross point of a linear function and its perpendicular line passing through a given point.

    Args:
    - equation (tuple): Coefficients (a, b) of the line equation: y = ax + b
    - point (tuple): Coordinates of the point (px, py)

    Returns:
    - tuple: Coordinates of the cross point (x, y)
    """

    a1, b1 = equation
    px, py = point
    
    # find perpendicular coefficients
    a2 = -1 / a1
    b2 = py - a2 * px

    x = (b2 - b1) / (a1 - a2)
    y = (a1*b2 - b1*a2) / (a1 - a2)

    return (x, y)


def cross_point_3D(point1, point2, synapse):

    """
    Calculate the coordinates of a cross point of a linear function and its perpendicular line passing through a given point.
    
    Args:
    - point1 (tuple): Coordinates of the first point (x1, y1, z1)
    - point2 (tuple): Coordinates of the second point (x2, y2, z2)
    - point (tuple): Coordinates of the synapse (px, py, pz)
    
    Returns:
    - tuple: Coordinates of the cross point (x, y, z)
    """

    x1, y1, z1 = point1
    x2, y2, z2 = point2
    px, py, pz = synapse

    line_equation1 = line_equation_2D((x1, y1), (x2, y2))
    cross_point1 = cross_point_2D(line_equation1, (px, py))

    line_equation2 = line_equation_2D((x1, z1), (x2, z2))
    cross_point2 = cross_point_2D(line_equation2, (cross_point1[0], pz))

    line_equation3 = line_equation_2D((y1, z1), (y2, z2))
    cross_point3 = cross_point_2D(line_equation3, (py, cross_point2[1]))

    print(f'Cross point 1: {cross_point1}')
    print(f'Cross point 2: {cross_point2}')
    print(f'Cross point 3: {cross_point3}')

    x, y, z = cross_point1[0], cross_point3[0], cross_point3[1]

    print(f'xyz: {x, y, z}')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot([x1, x2], [y1, y2], [z1, z2])
    ax.scatter(px, py, pz, color='b', s=50)
    ax.scatter(cross_point1[0], cross_point1[1], 0, color='g', s=50)
    ax.scatter(cross_point2[0], 0, cross_point2[1], color='g', s=50)
    ax.scatter(0, cross_point3[0], cross_point3[1], color='g', s=50)
    ax.scatter(x, y, z, color='r', s=50)

    plt.gca().set_aspect('equal')
    plt.show()

    return (x, y, z)


point1 = (1, 2, 3)
point2 = (5, 10, 15)
synapse = (3, 2, 6)

cp = cross_point_3D(point1, point2, synapse)
