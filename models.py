from collections import namedtuple
from parsing import parse_dataset

Position = namedtuple('Position', 'x y')

def manhattan_distance(pos, other_pos):
    return abs(pos.x - other_pos.x) + abs(pos.y - other_pos.y)

def euclidean_distance(pos, other_pos):
    return ((pos.x - other_pos.x) ** 2 + (pos.y - other_pos.y) ** 2) ** 0.5

class City:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class CityMap:
    MAPPING_MODE = 0
    EUCLIDEAN_MODE = 1
    MANHATTAN_MODE = 2

    def __init__(self, cities, distances, distance_mode=MAPPING_MODE):
        self.cities = cities
        if distance_mode == self.MAPPING_MODE:
            self.distance_mapping = self._build_distance_mapping(distances)
        elif distance_mode not in (self.EUCLIDEAN_MODE, self.MANHATTAN_MODE):
            raise ValueError('bad distance mode given')
        self.distance_mode = distance_mode

    def _build_distance_mapping(self, distances):
        distance_mapping = {}
        for i1, lines in enumerate(distances):
            c1 = self.cities[i1]
            distance_mapping.setdefault(c1.name, {})
            for i2, dist in enumerate(lines):
                c2 = self.cities[i2]
                distance_mapping.setdefault(c2.name, {})
                distance_mapping[c1.name][c2.name] = dist
                distance_mapping[c2.name][c1.name] = dist
        return distance_mapping

    def distance(self, city, other_city):
        if self.distance_mode == self.MAPPING_MODE:
            return citymap.distance_mapping[city.name][other_city.name]
        elif self.distance_mode == self.EUCLIDEAN_MODE:
            return euclidean_distance(city.position, other_city.position)
        elif self.distance_mode == self.MANHATTAN_MODE:
            return manhattan_distance(self.city.position, other_city.position)

def build_citymap(dataset, **kwargs):
    cities = list(City(name, Position(*position)) for name, position in
                  zip(dataset['name'], dataset['xy']))
    return CityMap(cities, dataset['dist'], **kwargs)

if __name__ == '__main__':
    import random
    from parsing import DATASETS
    dataset = parse_dataset(DATASETS[0])
    citymap = build_citymap(dataset, distance_mode=CityMap.MANHATTAN_MODE)
