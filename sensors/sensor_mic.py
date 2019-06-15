from module import Sensor
from grovepi import pinMode, analogRead
import time
from statistics import mean


class SensorMic(Sensor):
    port = None

    def set_params(self, params):
        self.port = params['port']
        pinMode(self.port, 'INPUT')

    def get_data(self):
        reads = []
        if self.send_interval > 1:
            # reads for times per second
            for _ in range(self.send_interval * 4):
                reads.append(analogRead(self.port))
                time.sleep(1/4)
        val = mean(reads)
        print(val)
        return val
