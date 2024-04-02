import Freenove_DHT as DHT
import time

class DHT11:
    def __init__(self, pin):
        self.DHTPin = pin
        self.dht = DHT.DHT(pin)   

    def read_temperature(self):
        counts = 0  
        while True:
            counts += 1
            for i in range(0, 15):            
                chk = self.dht.readDHT11()     
                if chk == self.dht.DHTLIB_OK:  
                    break
                time.sleep(0.1)
            temperature = self.dht.temperature
            return temperature

    def read_humidity(self):
        counts = 0  
        while True:
            counts += 1
            for i in range(0, 15):            
                chk = self.dht.readDHT11()     
                if chk == self.dht.DHTLIB_OK:  
                    break
                time.sleep(0.1)
            humidity = self.dht.humidity
            return humidity

