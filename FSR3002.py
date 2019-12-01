import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz=1000000
spi.bits_per_word=8

dummy = 0xff
start = 0x47
sgl = 0x20
ch0 = 0x00
msbf = 0x08

def measure(ch):
    ad = spi.xfer2( [ (start + sgl + ch + msbf), dummy ] )
    
    #merge 2bit and 8bit to 10bit data
    val = ( ( ( (ad[0] & 0x03) << 8) + ad[1] ) * 3.3) / 1023
    return val
