from math import sqrt

def distance(coordinate, units):
    lowest_distance = 1000
    if units:
        for unit in units:
            a_distance = sqrt(
                 (coordinate[0] - unit.map_r)**2 +
                 (coordinate[1] - unit.map_c)**2
                 )
            if a_distance < lowest_distance:
                lowest_distance = a_distance
        return lowest_distance
    else:
        return 0