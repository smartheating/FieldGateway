import yaml
from module import Sensor
from importlib import invalidate_caches


class ModuleFactory:
    def __init__(self, conf):
        self.conf = conf

    @staticmethod
    def _get_element_from_path(dictionary, path_list):
        def recursion(d, l):
            key = l.pop(0)
            if len(l) > 0:
                return recursion(d[key], l)
            else:
                return d[key]
        try:
            element = recursion(dictionary, path_list)
        except TypeError:
            raise TypeError('Could not read the config file. Please see README.md for how to define a config file.')
        return element

    @staticmethod
    def _load_module(script):
        def _is_sensor_subclass(obj):
            return isinstance(obj, type) and issubclass(obj, Sensor) and obj.__name__ is not 'Sensor'
        locals_tmp = list(locals().keys()) + ['locals_tmp']
        exec(script)
        keys_new_objects = [k for k in locals().keys() if k not in locals_tmp]
        for k in keys_new_objects:
            globals()[k] = locals()[k]
        invalidate_caches()
        class_names = [k for k in keys_new_objects if _is_sensor_subclass(globals().get(k))]
        return globals().get(class_names[0])

    def get_sensors(self) -> [Sensor]:
        sensor_conf = self._get_element_from_path(self.conf, ['sensors'])
        sensors = []
        for s_conf in sensor_conf:
            with open(s_conf['script_path'], 'r') as f:
                script = f.read()
            sensor = self._load_module(script)()
            sensor.set_params(s_conf['params'])
            sensor.set_module_id(s_conf['module_id'])
            sensor.set_module_name(s_conf['module_name'])
            sensor.set_reads_per_minute(s_conf['reads_per_minute'])
            sensor.set_reads_per_minute(s_conf['reads_per_minute'])
            sensor.set_send_interval(s_conf['send_interval'])
            sensors.append(sensor)
        return sensors




