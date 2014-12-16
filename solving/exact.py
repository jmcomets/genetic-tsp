from itertools import permutations

__all__ = ('solve',)

def solve(citymap, starting_city):
    return min(permutations((c for c in citymap.cities
                             if c is not starting_city)),
               key=citymap.total_path_distance)
