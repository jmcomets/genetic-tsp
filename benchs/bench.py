import sys; sys.path.append('.')
from solving import solve
from models import parse_and_build_dataset
from parsing import DATASETS

for dataset in DATASETS:
    citymap = parse_and_build_dataset(dataset)
    for starting_city in citymap.cities:
        lines, _ = solve(citymap, starting_city)
        with open('benchs/results/%s-%s.csv' % (dataset, starting_city.name), 'w') as fp:
            for i, _, distance in lines:
                fp.write('%s,%s\n' % (i, distance))
        break
    break
