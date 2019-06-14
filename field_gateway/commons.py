from pathlib import Path


def read_yaml(path):
    import yaml
    with open(path, 'r') as f:
        result = yaml.safe_load(f)
    return result


def read_device_ids():
    import json
    device_ids = None
    try:
        with open(str(get_project_root() / 'device_ids.json'), 'r') as f:
            device_ids = json.load(f)
    except:
        pass
    if not isinstance(device_ids, dict):
        device_ids = {}
    return device_ids


def store_device_ids(device_ids):
    import json
    with open(str(get_project_root() / 'device_ids.json'), 'r') as f:
        json.dump(device_ids, f)


def get_project_root() -> Path:
    import inspect, os
    return Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) / '..'


