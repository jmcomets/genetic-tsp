from collections import namedtuple
from parsing import parse_dataset

Position = namedtuple('Position', 'x y')

class City:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class CityDistanceFinder:
    def distance_between(self, city, other_city):
        raise NotImplementedError

class ManhattanCDF(CityDistanceFinder):
    def distance_between(self, city, other_city):
        pos, other_pos = city.position, other_city.position
        return abs(pos.x - other_pos.x) + abs(pos.y - other_pos.y)

class EuclideanCDF(CityDistanceFinder):
    def distance_between(self, city, other_city):
        pos, other_pos = city.position, other_city.position
        return ((pos.x - other_pos.x) ** 2 + (pos.y - other_pos.y) ** 2) ** 0.5

class MappedCDF(CityDistanceFinder):
    def __init__(self, cities, distances):
        self.distance_mapping = {}
        for i1, lines in enumerate(distances):
            c1 = cities[i1]
            self.distance_mapping.setdefault(c1, {})
            for i2, dist in enumerate(lines):
                c2 = cities[i2]
                self.distance_mapping.setdefault(c2, {})
                self.distance_mapping[c1][c2] = dist
                self.distance_mapping[c2][c1] = dist

    def distance_between(self, city, other_city):
        return self.distance_mapping[city][other_city]

class CityMap:
    def __init__(self, cities, cdf):
        self.cities = cities
        self.cdf = cdf

    def distance_between(self, city, other_city):
        return self.cdf.distance_between(city, other_city)
