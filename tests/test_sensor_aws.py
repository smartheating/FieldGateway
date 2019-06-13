from test_data.test_sensor_1 import SensorDummy1
from threading import Thread
import json
import time
from flask import Flask, request

cloud_gateway_ip = '54.165.131.127'
cloud_gateway_port = 9001
wait_seconds = 3


class TestSensorAWS:

    @staticmethod
    def _get_dummy_sensor():
        sensor = SensorDummy1()
        sensor.set_module_id(1)
        sensor.set_send_interval(1)
        sensor.set_reads_per_minute(480)
        sensor.set_module_name('test_sensor')
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
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'},
        return Thread(target=app.run, kwargs={'host': host, 'port': port}), messages

    def test_device_registration(self):
        """
        Tests if the sensor module actually sends a registration message via http
        """
        sensor = self._get_dummy_sensor()
        responses = []
        sensor.set_response_callback(func=lambda response: responses.append(response))
        sensor.register()
        time.sleep(wait_seconds)
        for response in responses:
            print(json.loads(response.content))
        assert len(responses) > 0
        assert json.loads(responses[0].content)['module_name'] == 'test_sensor'
        sensor.stopped.set()

    def test_event_sending(self):
        """
        Tests if the sensor module actually sends the values from get_data and sends them via http
        """
        sensor = self._get_dummy_sensor()
        responses = []
        sensor.set_response_callback(func=lambda response: responses.append(response))
        sensor.start()
        time.sleep(wait_seconds)
        for msg in responses:
            print(json.loads(msg.content))
        assert len(responses) > 0
        assert json.loads(responses[0].content)['value_type'] == 'float'
        sensor.stopped.set()
