from commons import get_project_root
from module_factory import ModuleFactory
import os
import yaml


root_path = get_project_root()
os.chdir(root_path)


class TestModuleFactory:

    def test_sensor(self):
        with open(root_path / 'tests' / 'test_data' / 'test_config_1.yaml', 'r') as f:
            conf = yaml.load(f)
        factory = ModuleFactory(conf)
        sensors = factory.get_sensors()

        # There should be two sensors..
        assert len(sensors) == 2
        sensor_1 = sensors[0]
        sensor_2 = sensors[1]

        # Tests if the factory sets the default module parameters
        assert sensor_1.module_type == 'sensor'
        assert sensor_1.module_id == 0
        assert sensor_1.module_ip == '0.0.0.0'
        assert sensor_1.module_port == '12345'
        assert sensor_1.module_name == 'Test Sensor 1'
        assert sensor_1.script_path == 'tests/test_data/test_sensor_1.py'
        assert sensor_1.value_type == ''

        # Tests if the factory sets the sensor parameters
        assert sensor_1.send_interval == 1.5
        assert sensor_1.reads_per_minute == 120

        # Tests if the factory sets the user defined parameters
        assert sensor_1.param_1 == 42
        assert sensor_2.param_b == 'some arbitrary param'


