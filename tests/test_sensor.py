from test_data.test_sensor_1 import SensorDummy1
from threading import Thread
import json
import time
from flask import Flask, request

cloud_gateway_ip = 'localhost'
cloud_gateway_port = 5000


class TestSensor:

    @staticmethod
    def _get_dummy_sensor():
        sensor = SensorDummy1()
        sensor.set_module_id(1)
        sensor.set_send_interval(0.5)
        sensor.set_reads_per_minute(480)
        sensor.set_module_name('test_get_sensor')
        sensor.set_cloud_gateway_ip(cloud_gateway_ip)
        sensor.set_cloud_gateway_port(cloud_gateway_port)
        return sensor

    @staticmethod
    def _get_test_api(host, port, route):
        app = Flask('test_api')
        messages = []
        @app.route(route, methods=['POST'])
        def receive_device_registration():
            messages.append(request.get_data())
            return json.dumps({'success': True, 'id': 0}), 200, {'ContentType': 'application/json'},
        return Thread(target=app.run, kwargs={'host': host, 'port': port}, daemon=True), messages

    def test_int_message(self):
        """
        test value of type int
        """
        sensor = self._get_dummy_sensor()
        list_msg = sensor.create_event_messages({'test': 23})
        msg = json.loads(list_msg[0])
        assert len(list_msg) == 1
        assert msg['module_name'] == 'test_get_sensor'
        assert msg['value_type'] == 'int'
        assert msg['tag'] == 'test'
        assert msg['value'] == '23'

    def test_float_message(self):
        """
        test value of type float
        """
        sensor = self._get_dummy_sensor()
        msg_list = sensor.create_event_messages({'test': 23.3})
        msg = json.loads(msg_list[0])
        assert msg['value_type'] == 'float'
        assert msg['value'] == '23.3'

    def test_str_message(self):
        """
        test value of type str
        """
        sensor = self._get_dummy_sensor()
        msg_list = sensor.create_event_messages({'test': 'asdf'})
        msg = json.loads(msg_list[0])
        assert msg['value_type'] == 'str'
        assert msg['value'] == 'asdf'

    def test_list_message(self):
        """
        test value of type list
        """
        sensor = self._get_dummy_sensor()
        msg_list = sensor.create_event_messages({'test_1': 23.3, 'test_2': 'wat'})
        msg_0 = json.loads(msg_list[0])
        msg_1 = json.loads(msg_list[1])
        assert msg_0['value_type'] == 'float'
        assert msg_0['value'] == '23.3'
        assert msg_1['value_type'] == 'str'
        assert msg_1['value'] == 'wat'

    def test_device_registration(self):
        """
        Tests if the sensor module actually sends a registration message via http
        """
        sensor = self._get_dummy_sensor()
        sensor.set_cloud_gateway_port(5001)
        test_api, messages = self._get_test_api(
            sensor.cloud_gateway_ip, sensor.cloud_gateway_port, '/repository/devices')
        test_api.start()
        time.sleep(1)
        sensor.register()
        time.sleep(1)
        for msg in messages:
            print(json.loads(msg.decode()))
        assert len(messages) > 0
        assert json.loads(messages[0].decode())['module_name'] == 'test_get_sensor'
        sensor.stopped.set()
        test_api.join(timeout=1)

    def test_event_sending(self):
        """
        Tests if the sensor module actually sends the values from get_data and sends them via http
        """
        sensor = self._get_dummy_sensor()
        sensor.set_cloud_gateway_port(5002)
        test_api, messages = self._get_test_api(
            sensor.cloud_gateway_ip, sensor.cloud_gateway_port, '/repository/events')
        test_api.start()
        time.sleep(1)
        sensor.start()
        time.sleep(1)
        for msg in messages:
            print(json.loads(msg.decode()))
        assert len(messages) > 0
        assert json.loads(messages[0].decode())['module_name'] == 'test_get_sensor'
        sensor.stopped.set()
        test_api.join(timeout=1)
