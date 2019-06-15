from module import Sensor
from grovepi import pinMode, dht
import time
from statistics import mean

class SensorDHT(Sensor):
    port = None
    dht_type = None

    def set_params(self, params):
        self.port = params['port']
        self.dht_type = params['dht_type']
        pinMode(self.port, 'INPUT')

    def get_data(self) -> list:
        reads = []
        n = self.get_number_of_reads_per_send_interval()
        for _ in range(n):
            reads.append(dht(self.port, self.dht_type))
            time.sleep(float(self.send_interval) / n)
        val = mean(reads)
        return val
