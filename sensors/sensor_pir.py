from module import Sensor
import time
from statistics import mean
import logging

class SensorPIR(Sensor):
    port = None

    def set_params(self, params):
        self.port = params['port']

    def thread_init(self):
        from grovepi import pinMode, digitalRead
        pinMode(self.port, 'INPUT')

    def get_data(self):
        reads = []
        n = self.get_number_of_reads_per_send_interval()
        for _ in range(n):
            reads.append(digitalRead(self.port))
            time.sleep(float(self.send_interval) / n)
        val = mean(reads)
        logging.debug('{} read values: {}'.format(self.module_name, reads))
        return {self.tags[0]: val}
