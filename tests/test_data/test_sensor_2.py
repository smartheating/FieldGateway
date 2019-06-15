from module import Sensor


class SensorDummy1(Sensor):
    param_a = None
    param_b = None

    def set_params(self, params):
        self.param_a = params['param_a']
        self.param_b = params['param_b']

    def get_data(self) -> dict:
        print('get data was called')
        return {'tag_1': 1.23, 'tag_2': 4.56}
