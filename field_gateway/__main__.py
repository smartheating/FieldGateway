from os import environ
from commons import read_device_ids
import yaml
from commons import get_project_root, store_device_ids
from module_factory import ModuleFactory
from threading import Event

if __name__ == '__main__':

    # read the environment variables
    env_config = environ.get('CONFIG', '../config.yaml')

    # load the config file
    with open(env_config, 'r') as f:
        conf = yaml.safe_load(f)

    # load the device ids
    device_ids = read_device_ids()

    # load the sensor modules'
    module_factory = ModuleFactory(conf, device_ids)
    sensors = module_factory.get_sensors()

    # store updated device ids
    store_device_ids(module_factory.device_ids)

    for sensor in sensors:
        sensor.start()
    try:
        Event().wait()
    except KeyboardInterrupt:
        for sensor in sensors:
            sensor.stopped.set()





