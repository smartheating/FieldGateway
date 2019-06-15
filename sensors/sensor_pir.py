from module import Sensor
from grovepi import pinMode, digitalRead


class SensorPIR(Sensor):
    port = None

    def set_params(self, params):
        self.port = params['port']
        pinMode(self.port, 'INPUT')

    def get_data(self):
        val = digitalRead(self.port)
        print(val)
        return val
