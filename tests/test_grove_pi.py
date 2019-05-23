from grovepi import *
from time import sleep


sensor_dht = 7
sensor_pir = 8
sensor_mic = 0

for x in [sensor_dht, sensor_pir, sensor_mic]:
    pinMode(x, 'INPUT')


class TestGrovePi:

    def test_mic(self):
        print('start mic test')
        rec = []
        for _ in range(5):
            reading = analogRead(sensor_mic)
            assert reading is not None
            rec.append(reading)
            sleep(1)
        print(rec)
        assert True

    def test_pir(self):
        print('start pir test')
        rec = []
        for _ in range(5):
            reading = digitalRead(sensor_pir)
            assert reading is not None
            rec.append(reading)
            sleep(1)
        print(rec)
        assert True

    def test_dht(self):
        print('start dht test')
        rec = []
        for _ in range(5):
            reading = dht(sensor_dht, 0)
            assert reading is not None
            rec.append(reading)
            sleep(1)
        print(rec)
        assert True


def read_mic():
    while True:
        print(analogRead(sensor_mic))
        sleep(0.1)


def read_pir():
    while True:
        print(digitalRead(sensor_pir))
        sleep(0.1)


def read_dht():
    while True:
        print(dht(sensor_dht, 0))
        sleep(1)

if __name__ == '__main__':
    test = TestGrovePi()
    test.test_dht()
    test.test_mic()
    test.test_pir()


