import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

def sensores():
	values = [0]*4

	for i in range(4):
		values[i] = adc.read_adc(i, gain=GAIN)
	time.sleep(0.1)
	return values

sensores()
