from models import Position, City, CityMap, MappedCDF
from parsing import parse_dataset

def build_citymap(dataset, cdf_cls=MappedCDF):
    cities = list(City(name, Position(*position)) for name, position in
                  zip(dataset['name'], dataset['xy']))
    cdf = cdf_cls(dataset['name'], dataset['dist'])
    return CityMap(cities, cdf)

if __name__ == '__main__':
    from parsing import DATASETS
    dataset = parse_dataset(DATASETS[0])
    citymap = build_citymap(dataset)
