#servo moter
import RPi.GPIO as GPIO
import time
import FSR3002 as FSR

GPIO.setmode(GPIO.BOARD)

SRV = 12

GPIO.setup(SRV,GPIO.OUT)

freq = 100.0 #frequence
deg_min = 0.0 #degree
deg_max = 180.0
dc_min = 5.0 #PWM duty
dc_max = 22.0

p = GPIO.PWM(SRV, freq)
p.start(0)

def convert_dc(deg):
    return((deg-deg_min) * (dc_max - dc_min) / (deg_max - deg_min) + dc_min)

def init_arm(deg):
    #p.start(0)
    for deg in range(90, -1, -10):
        dc = convert_dc(float(deg))
        p.ChangeDutyCycle(dc)
        fsr = FSR.measure(FSR.ch0)
        if fsr > 1:
            break
        time.sleep(0.1)
    #p.stop()
        
def place_an_arm(deg):
    ch0 = FSR.ch0
    fsr = FSR.measure(ch0)
    #p = GPIO.PWM(SRV, freq)
    #p.start(0)
    while not(fsr > 1 and fsr < 2):
        fsr = FSR.measure(ch0)
        print("fsr = ",fsr)#
        if (fsr > 1 and fsr < 2):
            print("touched book")#
        elif fsr < 1:#did't contact
            print("deg = ",deg)
            if deg > 0:
                deg = deg - 1
                dc = convert_dc(float(deg))
                p.ChangeDutyCycle(dc)
        elif fsr > 2:#powerful contact
            print("deg = ",deg)
            if deg < 90:
                deg = deg + 1
                dc = convert_dc(float(deg))
                p.ChangeDutyCycle(dc)
        else:
            print("error #line 61")
        time.sleep(0.2)
        #p.stop()#because vibes of motor
    

    
