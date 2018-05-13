import yaml


def load_yaml(filename):
    return yaml.load(open(filename))