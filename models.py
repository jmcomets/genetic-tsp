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
    def __init__(self, cities, distances):
        self.cities = cities
        self.distances = distances

def build_citymap(dataset):
    cities = list(City(name, Position(*position)) for name, position in
                  zip(dataset['name'], dataset['xy']))
    return CityMap(cities, dataset['dist'])

if __name__ == '__main__':
    from parsing import DATASETS
    dataset = parse_dataset(DATASETS[0])
    citymap = build_citymap(dataset)
    print('Cities:')
    for city in citymap.cities:
        print(city.name, '->', city.position)
    print(citymap.distances)
