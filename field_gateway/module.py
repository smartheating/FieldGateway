from abc import abstractmethod
import json
from threading import Thread, Event
import requests
import time


class Module:
    module_id = None
    module_name = None

    def set_module_id(self, module_id: int):
        self.module_id = module_id

    def set_module_name(self, name: str):
        self.module_name = name


class Sensor(Module, Thread):

    def __init__(self):
        Module.__init__(self)
        Thread.__init__(self)
        self.stopped = Event()
        self.send_interval = 10
        self.reads_per_minute = 60

    cloud_gateway_ip = None
    cloud_gateway_port = None

    @abstractmethod
    def set_params(self, params):
        raise NotImplementedError

    @abstractmethod
    def get_data(self):
        raise NotImplementedError

    def run(self) -> None:
        print('started {}'.format(self.module_name))
        while not self.stopped.wait(self.send_interval):
            self._read_and_send()

    def _read_and_send(self):
        list_msg = self.create_messages(
            self.get_data())
        for msg in list_msg:
            requests.post('http://{}:{}/sensor_reading'.format(self.cloud_gateway_ip, self.cloud_gateway_port),
                          data=msg)

    def set_send_interval(self, send_interval):
        self.send_interval = send_interval

    def set_reads_per_minute(self, reads_per_minute):
        self.reads_per_minute = reads_per_minute

    def set_cloud_gateway_ip(self, cloud_gateway_ip: str):
        self.cloud_gateway_ip = cloud_gateway_ip

    def set_cloud_gateway_port(self, cloud_gateway_port: int):
        self.cloud_gateway_port = cloud_gateway_port

    def create_messages(self, data):
        def _create(val):
            return json.dumps({
                'module_id': self.module_id,
                'module_name': self.module_name,
                'timestamp': time.time(),
                'type': type(val).__name__,
                'value': str(val)
            })
        if type(data) == list:
            msg_values = [_create(val) for val in data]
        elif type(data) in [int, float, str, bool]:
            msg_values = [_create(data)]
        else:
            raise ValueError('The function "get_data" function must return one of the following datatypes: '
                             'int, float, str, bool, list. If you use a list, make sure that it only contains '
                             'values of the following types: int, float, str, bool')
        return msg_values

    def get_number_of_reads_per_send_interval(self):
        return int(self.reads_per_minute / 60 * self.send_interval)


class Actuator(Module):
    pass
