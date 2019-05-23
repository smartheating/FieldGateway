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

        # Tests if the factory sets the default module parameters
        assert sensors[0].module_name == 'Test Sensor 1'
        assert sensors[1].module_id == 1

        # Tests if the factory sets the sensor parameters
        assert sensors[0].reads_per_minute == 120
        assert sensors[1].send_interval == 1.5

        # Tests if the factory sets the user defined parameters
        assert sensors[0].param_1 == 42
        assert sensors[1].param_b == 'some arbitrary param'


