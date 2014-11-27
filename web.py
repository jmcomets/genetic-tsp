import logging
from flask import Flask, jsonify, abort, request
from models import Position, City, CityMap, MappedCDF
from parsing import parse_dataset, DATASETS
import methods.genetic # FIXME

app = Flask(__name__, static_folder='static', static_url_path='')

def build_citymap(dataset):
    cities = list(City(name, Position(*position)) for name, position in
                  zip(dataset['name'], dataset['xy']))
    cdf = MappedCDF(dataset['name'], dataset['dist'])
    return CityMap(cities, cdf)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/config')
def api_config():
    return jsonify({
        'datasets': app.config['DATASETS'],
        'methods': list(app.config['TSP_METHODS'].keys()),
        })

@app.route('/api/methods', methods=['POST'])
def api_methods_post():
    """Run a TSP solver for a given dataset.

    Parameters:
    - starting_city: name of the city to start from
    - dataset: name of the dataset to use (see app.config['DATASETS'])
    - method: the TSP method to use (see app.config['TSP_METHODS'])

    Returns: a JSON object
    - path: a list of city names to follow
    """
    try:
        # solving method
        method_name = request.form['method']
        method = app.config['TSP_METHODS'][method_name]

        # dataset
        dataset_name = request.form['dataset']
        dataset = app.config['DATASETS'][dataset_name]
        citymap = build_citymap(dataset)

        # get starting city
        starting_city_name = request.form['starting_city']
        starting_city = next((c for c in citymap.cities
                              if c.name == starting_city_name), None)
        if starting_city is None:
            raise KeyError

        # run solver
        path = method.solve(citymap, starting_city)
        return jsonify({
            'path': [c.name for c in path],
            })
    except KeyError:
        return abort(400)

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    if app.debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # parse all available datasets
    parsed_datasets = {}
    for dataset in DATASETS:
        app.logger.info('parsing dataset %s' % dataset)
        parsed_datasets[dataset] = parse_dataset(dataset)
    app.config['DATASETS'] = parsed_datasets

    # setup tsp algorithms
    app.config['TSP_METHODS'] = {
            'genetic': methods.genetic,
            }

if __name__ == '__main__':
    import sys
    app.run(debug='--debug' in sys.argv)
