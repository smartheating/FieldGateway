from module import Sensor

class SensorDHT(Sensor):
    port = None
    dht_type = None

    def set_params(self, params):
        self.port = params['port']
        self.dht_type = params['dht_type']

    def thread_init(self):
        from grovepi import pinMode, dht
        pinMode(self.port, 'INPUT')

    def get_data(self) -> dict:
        reads = []
        val = dht(self.port, self.dht_type)
        return {self.tags[0]: val[0], self.tags[1]: val[1]}
