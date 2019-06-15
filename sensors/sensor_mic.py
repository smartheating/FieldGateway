from module import Sensor
from grovepi import pinMode, analogRead
import time
from statistics import mean
import logging

class SensorMic(Sensor):
    port = None

    def set_params(self, params):
        self.port = params['port']
        pinMode(self.port, 'INPUT')

    def get_data(self):
        reads = []
        n = self.get_number_of_reads_per_send_interval()
        for _ in range(n):
            reads.append(analogRead(self.port))
            time.sleep(float(self.send_interval) / n)
        val = mean(reads)
        logging.info('{}: read values: {}'.format(self.module_name, reads))
        return {self.tags[0]: val}
