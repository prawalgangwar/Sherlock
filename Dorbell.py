import  RPi.GPIO as GPIO
from time import sleep
import picamera
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = picamera.PiCamera()

s = socket.socket()
host = socket.gethostname()
port = 1994


i=1
camera.start_preview()
print "welcome to pi cam"
try:
	while 1:
		while GPIO.input(17):
			pass
		print "button pressed!"
		imagename = "image" + str(i) + ".jpg"
		camera.capture(imagename)
		i = i+1
		s.connect((host, port))
		with open(imagename, 'rb') as f:
			l = f.read(1024)
			while (l):
				s.send(l)
				l = f.read(1024)

		print "image sent!"
		s.close()
		sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
	camera.stop_preview()
