import RPi.GPIO as GPIO
import spidev
import time
import FSR3002 as FSR
import sensing_arm as SVM

GPIO.setmode(GPIO.BOARD)

SW = 7#switch
SRV = 12#servo_motor
GPIO.setup(SW, GPIO.IN)
GPIO.setup(SRV,GPIO.OUT)

try:
    deg = 0
    SVM.init_arm(deg)
    while 1:
        key_in = GPIO.input(SW)
        time.sleep(0.5)
        print(key_in)
        if key_in==0:#check switch
            SVM.place_an_arm(deg)
            

except KeyboardInterrupt:
    pass


GPIO.cleanup()
