from module import Sensor, Actuator, Module
from importlib import invalidate_caches
from logging import info


class ModuleFactory:
    def __init__(self, conf: dict, device_ids: dict):
        self.conf = conf
        self.device_ids = device_ids

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

    def _add_module_conf(self, module: Module, conf: dict):
        module.set_module_type('sensor' if issubclass(module.__class__, Sensor) else 'actuator')
        module.set_module_ip(conf.get('module_ip', ''))
        module.set_module_name(conf.get('module_name', ''))
        module.set_module_port(conf.get('module_port', 9001))
        module.set_reads_per_minute(conf.get('reads_per_minute', 60))
        module.set_script_path(conf.get('script_path', ''))
        module.set_send_interval(conf.get('send_interval', 10))
        module.set_value_type(conf.get('value_type', ''))
        module.set_cloud_gateway_ip(self.conf.get('cloud_gateway_ip', ''))
        module.set_cloud_gateway_port(self.conf.get('cloud_gateway_port', ''))
        module.set_params(conf.get('params', ''))
        module.set_tags(conf.get('tags', []))

    def _set_module_name_and_eventually_register(self, module):
        if module.module_name in self.device_ids.keys():
            module_id = self.device_ids.get(module.module_name)
            info('Found module {} in cache. Id: {}'.format(module.module_name, module_id))
        else:
            module_id = module.register()
            info("Didn't find module {} in cache. Got module_id {} from backend".format(module.module_name, module_id))
        self.device_ids[module.module_name] = module_id
        module.set_module_id(module_id)

    def get_actuators(self) -> [Actuator]:
        act_conf = self._get_element_from_path(self.conf, ['actuators'])
        acts = []

    def get_sensors(self) -> [Sensor]:
        sensor_conf = self._get_element_from_path(self.conf, ['sensors'])
        sensors = []
        for s_conf in sensor_conf:
            with open(s_conf['script_path'], 'r') as f:
                script = f.read()
            sensor = self._load_module(script)()
            self._add_module_conf(sensor, s_conf)
            self._set_module_name_and_eventually_register(sensor)

            sensors.append(sensor)
        return sensors




