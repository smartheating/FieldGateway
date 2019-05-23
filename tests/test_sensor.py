from test_data.test_sensor_1 import SensorDummy1
from threading import Thread
import json
import time
from flask import Flask, request


sensor = SensorDummy1()
sensor.set_module_id(1)
sensor.set_send_interval(0.5)
sensor.set_reads_per_minute(480)
sensor.set_module_name('test_sensor')
sensor.set_cloud_gateway_ip('localhost')
sensor.set_cloud_gateway_port(5000)


class TestSensor:

    def test_int_message(self):
        """
        test value of type int
        """
        list_msg = sensor.create_messages(23)
        msg = json.loads(list_msg[0])
        assert len(list_msg) == 1
        assert msg['module_name'] == 'test_sensor'
        assert msg['type'] == 'int'
        assert msg['value'] == 23

    def test_float_message(self):
        """
        test value of type float
        """
        msg_list = sensor.create_messages(23.3)
        msg = json.loads(msg_list[0])
        assert msg['type'] == 'float'
        assert msg['value'] == 23.3

    def test_str_message(self):
        """
        test value of type str
        """
        msg_list = sensor.create_messages('asdf')
        msg = json.loads(msg_list[0])
        assert msg['type'] == 'str'
        assert msg['value'] == 'asdf'

    def test_list_message(self):
        """
        test value of type list
        """
        msg_list = sensor.create_messages([23.3, 'wat'])
        msg_0 = json.loads(msg_list[0])
        msg_1 = json.loads(msg_list[1])
        assert msg_0['type'] == 'float'
        assert msg_0['value'] == 23.3
        assert msg_1['type'] == 'str'
        assert msg_1['value'] == 'wat'

    def test_scheduling(self):
        """
        Tests if the sensor module actually sends the values from get_data and sends them via http
        """
        messages = []
        app = Flask('test_api')
        @app.route('/sensor_reading', methods=['POST'])
        def sensor_reading():
            messages.append(request.get_data())
        test_api = Thread(target=app.run, kwargs={'host': sensor.cloud_gateway_ip, 'port': sensor.cloud_gateway_port})
        test_api.start()
        sensor.start()
        time.sleep(2)
        sensor.stopped.set()
        for msg in messages:
            print(json.loads(msg))
        assert len(messages) > 0
        assert json.loads(messages[2])['module_name'] == 'test_sensor'
