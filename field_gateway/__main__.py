from os import environ
from commons import read_device_ids, get_project_root, prepare_logging
import yaml
from commons import store_device_ids, log_modules
from module_factory import ModuleFactory
from threading import Event
import logging


if __name__ == '__main__':

    prepare_logging()
    # read the environment variables
    env_config = environ.get('CONFIG', 'config.yaml')

    # load the config file
    with open(env_config, 'r') as f:
        conf = yaml.safe_load(f)

    # load the device ids
    device_ids = read_device_ids()

    # load the sensor modules'
    module_factory = ModuleFactory(conf, device_ids)
    sensors = module_factory.get_sensors()
    log_modules(sensors)
    # store updated device ids
    logging.info('Store device ids: {}'.format(device_ids))
    store_device_ids(module_factory.device_ids)

    for sensor in sensors:
        # Test every sensor
        if environ.get('TESTING', 'no') != 'no':
            logging.info('{} testing with parameters'.format(sensor.module_name))
            try:
                logging.info('{} test result: {}'.format(sensor.module_name, sensor.get_data()))
            except IndexError as e:
                logging.error(e)
                logging.error('Hint: You might have forgotten to set the tags in config.yaml')
                raise e

        logging.info('{} starting'.format(sensor.module_name))
        sensor.start()
    try:
        Event().wait()
    except Exception:
        logging.info('Application stopped')
        for sensor in sensors:
            sensor.stopped.set()





