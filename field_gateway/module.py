from abc import abstractmethod
import json
from threading import Thread, Event
import requests
import datetime
import logging


class Module:
    module_type = ''
    module_id = -1
    module_ip = ''
    module_name = ''
    module_port = 5000
    reads_per_minute = -1
    script_path = ''
    send_interval = -1
    value_type = ''
    tags = []
    cloud_gateway_ip = ''
    cloud_gateway_port = 9001
    response_callback = None

    def _create_register_message(self):
        return json.dumps({
            'device_type': self.module_type,
            'id': 0,
            'ip': self.module_ip,
            'module_name': self.module_name,
            'port': self.module_port,
            'reads_per_minute': self.reads_per_minute,
            'script_path': self.script_path,
            'send_interval': self.send_interval,
            'value_type': self.value_type
        })

    def register(self):
        response = requests.post(
            url='http://{}:{}/repository/devices'.format(self.cloud_gateway_ip, self.cloud_gateway_port),
            data=self._create_register_message(),
            headers={'content-type': 'application/json'})
        if self.response_callback is not None:
            try:
                self.response_callback(response)
            except:
                pass
        if response.ok:
            return json.loads(response.content.decode())['id']
        else:
            return None

    def set_response_callback(self, func):
        self.response_callback = func

    def set_module_type(self, module_type: str):
        self.module_type = module_type

    def set_module_id(self, module_id: int):
        self.module_id = module_id

    def set_module_ip(self, module_ip: str):
        self.module_ip = module_ip

    def set_module_name(self, name: str):
        self.module_name = name

    def set_module_port(self, module_port: int):
        self.module_port = module_port

    def set_reads_per_minute(self, reads_per_minute: int):
        self.reads_per_minute = reads_per_minute

    def set_script_path(self, script_path: str):
        self.script_path = script_path

    def set_send_interval(self, send_interval: float):
        self.send_interval = send_interval

    def set_value_type(self, value_type: str):
        self.value_type = value_type

    def set_tags(self, tags: list):
        self.tags = tags

    def set_cloud_gateway_ip(self, cloud_gateway_ip: str):
        self.cloud_gateway_ip = cloud_gateway_ip

    def set_cloud_gateway_port(self, cloud_gateway_port: int):
        self.cloud_gateway_port = cloud_gateway_port

    @abstractmethod
    def set_params(self, params):
        raise NotImplementedError

    def get_number_of_reads_per_send_interval(self):
        return int(self.reads_per_minute / 60 * self.send_interval)


class Sensor(Module, Thread):

    def __init__(self):
        Module.__init__(self)
        Thread.__init__(self)
        self.stopped = Event()
        self.send_interval = 10
        self.reads_per_minute = 60

    @abstractmethod
    def set_params(self, params):
        raise NotImplementedError

    @abstractmethod
    def get_data(self) -> dict:
        raise NotImplementedError

    def run(self) -> None:
        logging.info('started {}'.format(self.module_name))
        while not self.stopped.wait(self.send_interval):
            self._read_and_send()

    def _read_and_send(self):
        logging.debug('{} requesting data'.format(self.module_name))
        try:
            list_msg = self.create_event_messages(
                self.get_data())
        except IndexError as e:
            logging.error(e)
            logging.error('Hint: You might have forgotten to set the tags in config.yaml')
            raise e
        for msg in list_msg:
            logging.debug(msg)
            response = requests.post(
                url='http://{}:{}/repository/events'.format(self.cloud_gateway_ip, self.cloud_gateway_port),
                data=msg,
                headers={'content-type': 'application/json'})
            if self.response_callback is not None:
                try:
                    self.response_callback(response)
                except:
                    pass

    def create_event_messages(self, data):
        def _create(tag, val):
            return json.dumps({
                'module_id': self.module_id,
                'module_name': self.module_name,
                'timestamp': datetime.datetime.now().isoformat(),
                'tag': tag,
                'value_type': str(type(val).__name__),
                'value': str(val)
            })

        msg_values = [_create(tag, val) for tag, val in data.items()]
        return msg_values


class Actuator(Module):
    @abstractmethod
    def set_params(self, params):
        raise NotImplementedError

