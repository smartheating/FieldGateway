from pathlib import Path


def read_yaml(path):
    import yaml
    with open(path, 'r') as f:
        result = yaml.safe_load(f)
    return result


def get_project_root() -> Path:
    import inspect, os
    return Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) / '..'


