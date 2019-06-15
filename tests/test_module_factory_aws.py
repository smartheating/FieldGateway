from commons import get_project_root, store_device_ids, print_modules
from module_factory import ModuleFactory
from module import Module
from copy import deepcopy
import os
import yaml


cloud_gateway_ip = '54.165.131.127'
cloud_gateway_port = 9001
root_path = get_project_root()
os.chdir(str(root_path))


class TestModuleFactoryAWS:

    def test_sensor_aws(self):
        """
        In this test, the module names in the config file is different than in device_ids.
        In this case, the module factory should register new devices and update the device ids
        :return:
        """
        with open(str(root_path / 'tests' / 'test_data' / 'test_config_1.yaml'), 'r') as f:
            conf = yaml.safe_load(f)
        conf['cloud_gateway_ip'] = cloud_gateway_ip
        conf['cloud_gateway_port'] = cloud_gateway_port
        device_ids_orig= {'Test Sensor 1': 11}
        device_ids = deepcopy(device_ids_orig)
        factory = ModuleFactory(conf, device_ids)
        sensors = factory.get_sensors()
        print_modules(sensors)

        # There should be two sensors..
        assert len(sensors) == 2
        sensor_1 = sensors[0]
        sensor_2 = sensors[1]

        # Test that sensor_2 got new id from registration
        assert sensor_2.module_id != Module.module_id

        # Test that device_ids has changed during registration
        assert device_ids_orig != factory.device_ids

        # Test if the ids were set correctly
        assert sensor_1.module_id == device_ids[sensor_1.module_name]
        assert sensor_2.module_id == device_ids[sensor_2.module_name]

        store_device_ids(device_ids)

