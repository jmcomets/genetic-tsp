from itertools import permutations

__all__ = ('solve',)

def solve(self, citymap, starting_city):
    return min(map(lambda p: citymap.total_path_distance(p),
                   permutations((c for c in citymap.cities
                                 if c is not starting_city))))[1]
