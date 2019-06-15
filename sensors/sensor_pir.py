from module import Sensor
<<<<<<< HEAD
from grovepi import pinMode, analogRead
import time
from statistics import mean
=======
from grovepi import pinMode, digitalRead
>>>>>>> eba8c1af4e5f9deb722186e9c4d36886cf2cd9fd


class SensorPIR(Sensor):
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
        return val
