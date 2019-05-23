from os import environ
import yaml
from module_factory import ModuleFactory
from threading import Event

if __name__ == '__main__':

    'read the environment variables'
    env_config = environ.get('CONFIG', '../config.yaml')

    'load the config file'
    with open(env_config, 'r') as f:
        conf = yaml.load(f)

    'load the sensor modules'
    module_factory = ModuleFactory(conf)
    sensors = module_factory.get_sensors()
    for sensor in sensors:
        sensor.start()
    try:
        Event().wait()
    except KeyboardInterrupt:
        for sensor in sensors:
            sensor.stopped.set()





