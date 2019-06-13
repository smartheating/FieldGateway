from module import Sensor
from statistics import mean
from random import random


class SensorDummy1(Sensor):
    param_1 = None
    param_2 = None
    count = 0

    def set_params(self, params):
        self.param_1 = params['param_1']
        self.param_2 = params['param_2']

    def get_data(self) -> list:
        self.count += 1
        print('get data was called {} times'.format(self.count))
        val1 = []
        val2 = []
        for _ in range(self.get_number_of_reads_per_send_interval()):
            val1.append(random() * 40)
            val2.append(100 + (random() * 20))
        return [mean(val1), mean(val2)]
