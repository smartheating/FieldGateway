from module import Sensor
from grovepi import pinMode, dht


class SensorDHT(Sensor):
    port = None
    dht_type = None

    def set_params(self, params):
        self.port = params['port']
        self.dht_type = params['dht_type']
        pinMode(self.port, 'INPUT')

    def get_data(self) -> list:
        return dht(self.port, self.dht_type)