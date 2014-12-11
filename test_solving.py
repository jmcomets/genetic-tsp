from solving import solve
from models import parse_and_build_dataset
from parsing import DATASETS
from functools import reduce

# problem specification
citymap = parse_and_build_dataset(DATASETS[0])
starting_city = citymap.cities[0]

# helpers
city_distance = lambda c1, c2: citymap.distance_between(c1, c2)
path_distance = lambda cs: sum(city_distance(cs[i], cs[i+1]) for i in range(len(cs)-1))

path = solve(citymap, starting_city)
#print(path, path_distance(path))
