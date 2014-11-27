import os

DATASETS_DIR = 'data'
COMMENT_CHAR = '#'
DATASETS = os.listdir(DATASETS_DIR)

def lines_without_comments(fp):
    for line in fp:
        line = line.split(COMMENT_CHAR, 1)[0].strip()
        if line:
            yield line

def parse_dataset(dataset_name):
    dataset = {}
    dataset_dir = os.path.join(DATASETS_DIR, dataset_name)
    dataset_files = os.listdir(dataset_dir)
    for name, pattern in patterns.items():
        filename = pattern % dataset_name
        if filename in dataset_files:
            full_filename = os.path.join(dataset_dir, filename)
            with open(full_filename, 'r') as fp:
                fp = lines_without_comments(fp)
                dataset[name] = parsers[name](fp)
    return dataset

def parse_dist(fp):
    return list(list(map(float, line.split())) for line in fp)

def parse_name(fp):
    return list(fp)

def parse_xy(fp):
    return list(list(map(float, line.split())) for line in fp)

parsers = {
        'dist'   : parse_dist,
        'name'   : parse_name,
        'xy'     : parse_xy,
        }

patterns = {x : ''.join(('%s_', x, '.txt'))
            for x in parsers.keys()}
