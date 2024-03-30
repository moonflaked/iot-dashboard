import time
import Freenove_DHT as DHT

class DHT11:
    def __init__(self, pin):
        self.DHTPin = pin
        self.dht = DHT.DHT(pin)   # create a DHT class object

    def read_temperature_humidity(self):
        counts = 0  # Measurement counts
        while True:
            counts += 1
            for i in range(0, 15):            
                chk = self.dht.readDHT11()     # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                if chk == self.dht.DHTLIB_OK:  # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                    break
                time.sleep(0.1)
            humidity = self.dht.humidity
            temperature = self.dht.temperature
            print("Humidity : %.2f, \t Temperature : %.2f \n" % (humidity, temperature))
            return temperature, humidity


    
