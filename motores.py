
import time
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

M1 = 0x01	#llanta 1
M2 = 0x02	#llanta 2
M3 = 0x03	#llanta 3
M4 = 0x04	#llanta 4

M5 = 0x08
M6 = 0x05
M7 = 0x06
M8 = 0x07
M9 = 0x09


ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate= 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


def wheelMode(ID):
	GPIO.output(12, GPIO.HIGH)
	onLed(ID,0x01)
	checksum =(0xff &~(ID+0x05+0x03+0x06+0x00+0x00))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x05))
        ser.write(chr(0x03))
        ser.write(chr(0x06))
        ser.write(chr(0x00))
        ser.write(chr(0x00))
        ser.write(chr(checksum))
        time.sleep(1)
	checksum =(0xff &~(ID+0x05+0x03+0x08+0x00+0x00))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x05))
        ser.write(chr(0x03))
        ser.write(chr(0x08))
        ser.write(chr(0x00))
        ser.write(chr(0x00))
        ser.write(chr(checksum))
        time.sleep(1)
	onLed(ID,0x00)
	GPIO.output(12, GPIO.LOW)

def joinMode(ID):
	GPIO.output(12, GPIO.HIGH)
        onLed(ID,0x01)
        checksum =(0xff &~(ID+0x05+0x03+0x06+0x00+0x00))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x05))
        ser.write(chr(0x03))
        ser.write(chr(0x06))
        ser.write(chr(0x00))
        ser.write(chr(0x00))
        ser.write(chr(checksum))
        time.sleep(1)
        checksum =(0xff &~(ID+0x05+0x03+0x08+0xff+0x03))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x05))
        ser.write(chr(0x03))
        ser.write(chr(0x08))
        ser.write(chr(0xff))
        ser.write(chr(0x03))
        ser.write(chr(checksum))
        time.sleep(1)
        onLed(ID,0x00)
	GPIO.output(12, GPIO.LOW)

def velocidad(ID,vel):
	GPIO.output(12, GPIO.HIGH)
        vel_H = vel >> 8
        vel_L = vel % 256
        checksum =(0xff &~(ID+0x05+0x03+0x20+vel_L+vel_H))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x05))
        ser.write(chr(0x03))
        ser.write(chr(0x20))
        ser.write(chr(vel_L))
        ser.write(chr(vel_H))
        ser.write(chr(checksum))
        time.sleep(0.01)
	GPIO.output(12, GPIO.LOW)



def mover(ID,position):
	grados = int((3.41*position)-102.13)
	GPIO.output(12, GPIO.HIGH)
        position_H = grados >> 8
        position_L = grados % 256
        checksum =(0xff &~(ID+0x05+0x03+0x1e+position_L+position_H))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x05))
        ser.write(chr(0x03))
        ser.write(chr(0x1e))
        ser.write(chr(position_L))
        ser.write(chr(position_H))
        ser.write(chr(checksum))
        time.sleep(0.01)
	velocidad(ID, 50)
	GPIO.output(12, GPIO.LOW)

def onLed(ID, state):
	GPIO.output(12, GPIO.HIGH)
        checksum =(0xff &~(ID+0x04+0x03+0x19+state))
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x04))
        ser.write(chr(0x03))
        ser.write(chr(0x19))
        ser.write(chr(state))
        ser.write(chr(checksum))
        time.sleep(0.01)
	GPIO.output(12, GPIO.LOW)

def signalTemp(ID):
	GPIO.output(12, GPIO.HIGH)
        checksum =(0xff &~(ID+0x04+0x02+0x2B+0x01))
	time.sleep(0.01)
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(ID))
        ser.write(chr(0x04))
        ser.write(chr(0x02))
        ser.write(chr(0x2B))
        ser.write(chr(0x01))
        ser.write(chr(checksum))
        time.sleep(0.01)
	GPIO.output(12, GPIO.LOW)

def leerTemp():
	print("Temperatura")
	time.sleep(0.02)
	while ser.inWaiting() > 0:
		cadena += ser.readline()
		print cadena.rstrip("\n")
		cadena = ""

def setID(ID):
	GPIO.output(12, GPIO.HIGH)
	onLed(0xfe, 0x01)
        checksum =(0xff &~(ID+0x04+0x03+0x3+0xfe))
        time.sleep(0.01)
        ser.write(chr(0xff))
        ser.write(chr(0xff))
        ser.write(chr(0xfe))
        ser.write(chr(0x04))
        ser.write(chr(0x03))
        ser.write(chr(0x03))
        ser.write(chr(ID))
        ser.write(chr(checksum))
        time.sleep(0.01)
	onLed(0xfe, 0x00)
        GPIO.output(12, GPIO.LOW)

mover(8, 90)
