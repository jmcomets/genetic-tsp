from solving import solve
from models import parse_and_build_dataset
from parsing import DATASETS

for dataset in DATASETS:
    citymap = parse_and_build_dataset(dataset)
    for starting_city in citymap.cities:
        lines = list(solve(citymap, starting_city))
        with open('results/%s-%s.csv' % (dataset, starting_city.name), 'w') as fp:
            for i, distance in lines:
                fp.write('%s %s\n' % (i, distance))
