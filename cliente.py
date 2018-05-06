import socket
import sys
import time
import motores
import threading
import RPi.GPIO as GPIO1
import RPi.GPIO as GPIO2
import RPi.GPIO as GPIO3
import Queue
import commands
#import sensores

GPIO1.setmode(GPIO1.BOARD)
GPIO1.setup(16, GPIO1.OUT)

GPIO2.setmode(GPIO2.BOARD)
GPIO2.setup(40, GPIO1.OUT)

GPIO3.setmode(GPIO3.BOARD)
GPIO3.setup(22, GPIO3.OUT)

ledEnable = Queue.Queue()
Y = Queue.Queue()
leftyPad = Queue.Queue()
rightyPad = Queue.Queue()
arrowsButtonUp = Queue.Queue()
arrowsButtonLt = Queue.Queue()
arrowsButtonRt = Queue.Queue()
arrowsButtonDo = Queue.Queue()
LT = Queue.Queue()
RT = Queue.Queue()
alertSignal = Queue.Queue()

def UDPServerConnect():
	print 'iniciar'
	UDP_IP = '190.217.101.29'
	UDP_PORT = 10000

	while True:
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		sock.settimeout(0.5)
		try:
			sock.bind((UDP_IP, UDP_PORT))
		except:
			continue
		while True:
			sensor = sensores.sensores()
			print sensor
			try:
				sock.sendto(sensor, (UDP_IP, UDP_PORT))
			except socket.timeout, e:
				break
		continue

def ServerConnect(ledEnable,leftyPad,rightyPad,arrowsButtonUp,arrowsButtonLt,arrowsButtonRt,arrowsButtonDo,RT,LT,Y,alertSignal):
	HOST = '190.217.101.29'
	PORT = 10000
	while True:
		alertSignal.put(True)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               	s.settimeout(0.5)
		try:
			s.connect((HOST, PORT))
		except:
#			alertSignal.put(True)
			continue
#		alertSignal.put(False)
		while True:
			alertSignal.put(False)
			try:
				data = s.recv(12)
			except socket.timeout, e:
				data = 'null'
			except:
				data= 'null'
			if data == 'null':
				break
			try:
				bina = bin(int(str(data[2:12])))
			except:
				bina = bina
               	        ledEnable.put(bina[28])
                       	leftyPad.put(bina[11:15])
	                rightyPad.put(bina[3:7])
                        RT.put(bina[21])
               	        LT.put(bina[22])
                       	arrowsButtonUp.put(bina[29])
	                arrowsButtonLt.put(bina[30])
                        arrowsButtonRt.put(bina[31])
               	        arrowsButtonDo.put(bina[32])
                       	Y.put(bina[27])

		ledEnable.put('0000')
                leftyPad.put('0111')
                rightyPad.put('0111')
                RT.put('0')
       	        LT.put('0')
               	arrowsButtonUp.put('0')
                arrowsButtonLt.put('0')
                arrowsButtonRt.put('0')
       	        arrowsButtonDo.put('0')
               	Y.put(0)
		continue


def alert(alertSignal):
	led = False
        while alertSignal.get():
               	led = ~led
               	time.sleep(0.5)
		GPIO1.output(16, led)

def panoramic(ledEnable):
	led = False
	while True:
		if ledEnable.get() == "1":
			led = ~led
			time.sleep(0.7)
		GPIO1.output(16, led)

def LeftWheels(leftyPad, rightyPad,Y):
	vel = 0
	motor = 0
	dat = 0
	mecanum = False
	v = [0,0,0,0]
	while True:
		
		if str(Y.get()) == '1':
			mecanum = ~mecanum
			if mecanum:
				print 'mecanum'
			else:	
				print 'normal'
			GPIO2.output(40, mecanum)
			time.sleep(0.7)		
		if mecanum:
			v=mecanumWheels(str(leftyPad.get()),str(rightyPad.get()))			
		else:
			v=llantaNormal(str(leftyPad.get()),str(rightyPad.get()))
		print v
		motores.velocidad(0x01, v[0])
		motores.velocidad(0x02, v[1])
		motores.velocidad(0x03, v[2])
		motores.velocidad(0x04, v[3])


def llantaNormal(vel1, vel2):
	v = [0,0,0,0]
	v = [0,0,0,0]
        motor = 0
        motor1 = 0
        if vel1[0] == "1":
                motor = 8
        if vel1[1] == "1":
                motor = motor + 4
        if vel1[2] == "1":
                motor = motor + 2
        if vel1[3] == "1":
                motor = motor + 1

        if vel2[0] == "1":
                motor1 = 8
	if vel2[1] == "1":
                motor1 = motor1 + 4
        if vel2[2] == "1":
                motor1 = motor1 + 2
        if vel2[3] == "1":
                motor1 = motor1 + 1

        vel1 = motor
        vel2 = motor1

        if vel1 > 7 and vel2 == 7:
                dat = (((float(vel1)*1.0/15.0))*2.0)-1.0
                v[0]=(int(1023.0+1023.0*dat))
		v[1]=(int(1023.0+1023.0*dat))
                v[2]=(int(1023.0*dat))
                v[3]=(int(1023.0*dat))
        elif vel1 < 7 and vel2 == 7:
                dat = 1.0-(((float(vel1)*1.0/15.0))*2.0)
                v[0]=(int(1023.0*dat))
                v[1]=(int(1023.0*dat))
                v[2]=(int(1023.0+1023.0*dat))
                v[3]=(int(1023.0+1023.0*dat))
        elif vel2 > 7 and vel1 == 7:
                dat = (((float(vel2)*1.0/15.0))*2.0)-1.0
		v[0]=(int(1023.0+1023.0*dat))
                v[1]=(int(1023.0+1023.0*dat))
                v[2]=(int(1023.0+1023.0*dat))
                v[3]=(int(1023.0+1023.0*dat))
        elif vel2 < 7 and vel1 == 7:
                dat = 1.0-(((float(vel2)*1.0/15.0))*2.0)
                v[0]=(int(1023.0*dat))
                v[1]=(int(1023.0*dat))
                v[2]=(int(1023.0*dat))
                v[3]=(int(1023.0*dat))
        else:
                dat = 0
                v[0]=0
                v[1]=0
		v[1]=0
                v[2]=0
                v[3]=0
	return v

def mecanumWheels(vel1,vel2):
	v = [0,0,0,0]
        motor = 0
	motor1 = 0
        if vel1[0] == "1":
                motor = 8
        if vel1[1] == "1":
                motor = motor + 4
        if vel1[2] == "1":
                motor = motor + 2
        if vel1[3] == "1":
                motor = motor + 1

	if vel2[0] == "1":
                motor1 = 8
        if vel2[1] == "1":
                motor1 = motor1 + 4
        if vel2[2] == "1":
                motor1 = motor1 + 2
        if vel2[3] == "1":
                motor1 = motor1 + 1

        vel1 = motor
	vel2 = motor1

        if vel1 > 7 and vel2 == 7:
                dat = (((float(vel1)*1.0/15.0))*2.0)-1.0
                v[0]=(int(1023.0+1023.0*dat))
                v[1]=(int(1023.0+1023.0*dat))
		v[2]=(int(1023.0*dat))
                v[3]=(int(1023.0*dat))
        elif vel1 < 7 and vel2 == 7:
                dat = 1.0-(((float(vel1)*1.0/15.0))*2.0)
                v[0]=(int(1023.0*dat))
                v[1]=(int(1023.0*dat))
		v[2]=(int(1023.0+1023.0*dat))
                v[3]=(int(1023.0+1023.0*dat))
	elif vel2 > 7 and vel1 == 7:
		dat = (((float(vel2)*1.0/15.0))*2.0)-1.0
                v[0]=(int(1023.0+1023.0*dat))
                v[1]=(int(1023.0*dat))
                v[2]=(int(1023.0*dat))
                v[3]=(int(1023.0+1023.0*dat))
	elif vel2 < 7 and vel1 == 7:
		dat = 1.0-(((float(vel2)*1.0/15.0))*2.0)
                v[0]=(int(1023.0*dat))
                v[1]=(int(1023.0+1023.0*dat))
                v[2]=(int(1023.0+1023.0*dat))
                v[3]=(int(1023.0*dat))
        else:
                dat = 0
                v[0]=0
                v[1]=0
		v[2]=0
		v[3]=0
	return v


def pinza(RT,LT):
	a=[90,	90, 	90,	90,	90,	270,	270,	270,	270,	270]
	b=[60,	80,	80,	80,	80,	300,	180,	180,	180,	180]
	c=[290,	155,	155,	155,	155,	55,	180,	180,	180,	180]
	d=[210,	143,	143,	143,	143,	225,	225,	210,	210,	210]
	e=[270,	270,	270,	270,	270,	270,	270,	270,	225,	225]
	f=[180,	180,	270,	229,	200,	200,	200,	200,	200,	229]
	s = 0
	motores.mover(8,180)
        motores.mover(7,180)
        motores.mover(6,180)
	time.sleep(0.5)
	while True:
		if RT.get() == "1":
			s = s + 1
			time.sleep(0.2)
			if s >= len(b):
				s = 0	
			GPIO3.output(22, True)
        		time.sleep(0.8) 
       		        GPIO3.output(22, False)
		if LT.get() == "1":
			s = s - 1
			time.sleep(0.2)
			if s < 0:
                                s = 3
			GPIO3.output(22, True)
        		time.sleep(0.8)
        		GPIO3.output(22, False)
		motores.mover(10,f[s])
		motores.mover(9,e[s])
		motores.mover(8,d[s])
		motores.mover(7,c[s])
		motores.mover(6,b[s])
		motores.mover(5,a[s])
		
			


hilo1 = threading.Thread(target=ServerConnect, args=(ledEnable,leftyPad,rightyPad,arrowsButtonUp,arrowsButtonLt,arrowsButtonRt,arrowsButtonDo,RT,LT,Y,alertSignal,))
hilo2 = threading.Thread(target=panoramic, args=(ledEnable,))
hilo3 = threading.Thread(target=LeftWheels, args=(leftyPad, rightyPad,Y,))
hilo5 = threading.Thread(target=pinza, args=(RT,LT,)) 
hilo6 = threading.Thread(target=alert, args=(alertSignal,))
#hilo7 = threading.Thread(target=UDPServerConnect)


hilo1.start()
hilo2.start()
hilo3.start()
hilo5.start()
hilo6.start()
#hilo7.start()

ledEnable.join()
leftyPad.join()
rightyPad.join()
arrowsButtonUp.join()
arrowsButtonLt.join()
arrowsButtonRt.join()
arrowsButtonDo.join()
RT.join()
LT.join()
Y.join()
alertSignal.join()

hilo1.join()
hilo2.join()
hilo3.join()
hilo5.join()
hilo6.join()
#hilo7.join()
