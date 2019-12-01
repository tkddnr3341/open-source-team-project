import RPi.GPIO as GPIO
import time
#import FSR3002
#import servo_motor
import spidev

GPIO.setmode(GPIO.BOARD)

SW = 7#switch
SRV = 12#servo_motor

GPIO.setup(SW, GPIO.IN)
GPIO.setup(SRV,GPIO.OUT)

#FSR3002
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
spi.bits_per_word=8
dummy = 0xff
start = 0x47
sgl = 0x20
ch0 = 0x00
msbf = 0x08
#servo_motor
freq = 100.0 #frequence
deg_min = 0.0 #degree
deg_max = 180.0
dc_min = 5.0 #PWM duty
dc_max = 22.0

def convert_dc(deg):
    return((deg-deg_min) * (dc_max - dc_min) / (deg_max - deg_min) + dc_min)
def measure(ch):
    ad = spi.xfer2( [ (start + sgl + ch + msbf), dummy ] )
    #merge 2bit and 8bit to 10bit data
    val = ( ( ( (ad[0] & 0x03) << 8) + ad[1] ) * 3.3) / 1023
    return val
#output_pin:SRV, frequence:freq
p = GPIO.PWM(SRV, freq)
p.start(0)
try:
    #set arm to book
    for deg in range(90, -1, -10):
        dc = convert_dc(float(deg))
        p.ChangeDutyCycle(dc)
        fsr = measure(ch0)
        if fsr > 1:
            break
        time.sleep(0.1)
#    p.stop()
    
    while 1:
        key_in = GPIO.input(SW)
        time.sleep(0.5)
        
        if key_in==0:#check switch
            fsr = measure(ch0)
#            p = GPIO.PWM(SRV, freq)
#            p.start(0)
            while not(fsr > 1 and fsr < 2):
                fsr = measure(ch0)
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
#            p.stop()#because vibes of motor

except KeyboardInterrupt:
    pass

p.stop()

GPIO.cleanup()