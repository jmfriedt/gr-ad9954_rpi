# Datashet AD9954 p.23: SPI CK rest state=0, change on falling edge => mode 0
# GPIO12 -> 47
# GPIO23 -> IO_UPDATE
import time
import spidev
import pigpio

bus = 0       # SPI0
device = 0    # CS#
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 1000000
spi.mode = 0

pi=pigpio.pi()
pi.set_mode(12,pigpio.OUTPUT)
pi.write(12, 0)  # PS0 low

pi.set_mode(23,pigpio.OUTPUT)
pi.write(23, 0)  # IO_UPDATE low

pi.set_mode( 7,pigpio.OUTPUT)
pi.write( 7, 0)  # reset low
time.sleep(0.01)
pi.write( 7, 1)  # reset hi
time.sleep(0.01)
pi.write( 7, 0)  # reset low

CFR1=[0x00, 0x00, 0x00, 0x00, 0x40]; # CFR1 disable comparator
CFR2=[0x01, 0xC4, 0x02, 0x94];       # CFR2 REFCLK Multiplier 0xA0=x20 => 400 MHz bits 3-7, 02 for VCO = 400 MHz
                                     #                        0x90=x18 => 360 MHz
ASF =[0x02, 0x04, 0x55];             # Auto Ramp Rate Speed control=11 (ASF: Amplitude Scale Factor)
ARR =[0x03, 0xff];                   # ARR      Amplitude Ramp Rate register
POW0=[0x05, 0x00, 0x00];             # POW0 PHASE Offset World <13:0>  Not Used= 00
FTW1=[0x06, 0x2C, 0x8B, 0x43, 0x95]; # FTW1  Frequency Tuning Word
# FTW0=[0x04, 0x17, 0x77, 0x77, 0x77]; # FTW0 Frequency tuning World dec2hex(floor(33/360*2^32))
FTW0=[0x04, 0x18, 0x2d, 0x82, 0xd8]; # FTW0 Frequency tuning World dec2hex(floor(34/360*2^32))

spi.xfer2(CFR1)
spi.xfer2(CFR2)
spi.xfer2(ASF)
spi.xfer2(ARR)
spi.xfer2(POW0)
spi.xfer2(FTW1)
spi.xfer2(FTW0)
pi.write(23, 1)  # IO_UPDATE
time.sleep(0.01)
pi.write(23, 0)
