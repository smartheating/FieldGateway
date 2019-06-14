from test_data.test_sensor_1 import SensorDummy1
import json
import time

cloud_gateway_ip = '54.165.131.127'
cloud_gateway_port = 9001
wait_seconds = 3


class TestSensorAWS:

    @staticmethod
    def _get_dummy_sensor():
        sensor = SensorDummy1()
        sensor.set_module_name('test_get_sensor')
        sensor.set_send_interval(1)
        sensor.set_reads_per_minute(480)
        sensor.set_script_path('/dummy/path/to/script')
        sensor.set_cloud_gateway_ip(cloud_gateway_ip)
        sensor.set_cloud_gateway_port(cloud_gateway_port)
        return sensor

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
            print(json.loads(response.content.decode()))
        assert len(responses) > 0
        assert json.loads(responses[0].content.decode())['module_name'] == 'test_get_sensor'
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
            print(json.loads(msg.content.decode()))
        assert len(responses) > 0
        assert json.loads(responses[0].content.decode())['value_type'] == 'float'
        sensor.stopped.set()
