from bluetooth import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time
import string

# 1
GPIO.setup( 26, GPIO.OUT )
# 2
GPIO.setup( 24, GPIO.OUT )
# 3
GPIO.setup( 23, GPIO.OUT )
# 4
GPIO.setup( 22, GPIO.OUT )
# 5
GPIO.setup( 21, GPIO.OUT )
# 6
GPIO.setup( 19, GPIO.OUT )
# 7
GPIO.setup( 18, GPIO.OUT )
# 8
GPIO.setup( 16, GPIO.OUT )
# 9
GPIO.setup( 15, GPIO.OUT )

leds = [ 26, 24, 23, 22, 21, 19, 18, 16, 15 ]
curled = 0

def onetonine():
	#1
	GPIO.output( 26, True )
	time.sleep(0.01)
	GPIO.output( 26, False)
	#2
	GPIO.output( 24, True )
	time.sleep(0.01)
	GPIO.output( 24, False)
	#3
	GPIO.output( 23, True )
	time.sleep(0.01)
	GPIO.output( 23, False)
	#4
	GPIO.output( 22, True )
	time.sleep(0.01)
	GPIO.output( 22, False)
	#5							
	GPIO.output( 21, True )
	time.sleep(0.01)
	GPIO.output( 21, False)
	#6
	GPIO.output( 19, True )
	time.sleep(0.01)
	GPIO.output( 19, False)
	#7
	GPIO.output( 18, True )
	time.sleep(0.01)
	GPIO.output( 18, False) 
	#8
	GPIO.output( 16, True )
	time.sleep(0.1)
	GPIO.output( 16, False)
	#9
	GPIO.output( 15, True )
	time.sleep(0.1)
	GPIO.output( 15, False)



while True: 
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]

	uuid = "00000003-0000-1000-8000-00805F9B34FB"

	advertise_service( server_sock, "SampleServer",
			service_id = uuid,
			service_classes = [ uuid, SERIAL_PORT_CLASS ],
			profiles = [ SERIAL_PORT_PROFILE ],
			  )

	print("Waiting for connection on RFCOMM channel %d" % port )

	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)

	

	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0: break

			#print("received [%s]" % data)
			arr = data.split("/")

			power = int(arr[0])
			# Don't ask, I don't know how this works
			# Max array size -1, casted to an int
			# I'm so sorry
			angle = int( arr[ len(arr) - 1 ] )

			print( arr[0], arr[len(arr)-1] )
			
			for led in leds:
				GPIO.output( led, False )

			if angle < 0:
				curled = curled + 1
				if curled == len(leds):
					curled = 0
				GPIO.output( leds[curled], True )

			elif angle > 0:
				curled = curled - 1
				if curled == -1:
					curled = len(leds)-1
				GPIO.output( leds[curled], True )
	except IOError:
		pass

	print("Disconnected")

	client_sock.close()
	server_sock.close()
	print("all done")
