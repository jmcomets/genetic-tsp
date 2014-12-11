import logging
from flask import Flask, jsonify, abort, request
from models import parse_and_build_dataset
from parsing import DATASETS
import solving

app = Flask(__name__, static_folder='public', static_url_path='')

def citymap_to_dict(citymap):
    return [{'name': city.name,
             'position': {
                 'x': city.position.x,
                 'y': city.position.y,
                 }} for city in citymap.cities]

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/config')
def api_config():
    return jsonify({
        'citymaps': {dataset : citymap_to_dict(citymap)
                     for dataset, citymap in app.config['CITYMAPS'].items()},
        })

@app.route('/api/solution', methods=['POST'])
def api_solution_post():
    """Run a TSP solver for a given dataset.

    Parameters:
    - starting_city: name of the city to start from
    - dataset: name of the dataset to use (see app.config['DATASETS'])

    Returns: a JSON object
    - path: a list of city names to follow
    """
    params = request.get_json()
    try:
        # dataset
        dataset_name = params['dataset']
        citymap = app.config['CITYMAPS'][dataset_name]

        # get starting city
        starting_city_name = params['starting_city']
        starting_city = next((c for c in citymap.cities
                              if c.name == starting_city_name), None)
        if starting_city is None:
            raise KeyError

        # run solver
        path = solving.solve(citymap, starting_city)
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
    citymaps = {}
    for dataset_name in DATASETS:
        app.logger.info('parsing dataset %s' % dataset_name)
        citymaps[dataset_name] = parse_and_build_dataset(dataset_name)
    app.config['CITYMAPS'] = citymaps

if __name__ == '__main__':
    import sys
    app.run(debug='--debug' in sys.argv)
