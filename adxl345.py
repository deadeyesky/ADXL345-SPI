from __future__ import division
import spidev, datetime, time
import RPi.GPIO as GPIO

# Setup SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 3

# Constants
accres, accrate = 16, 15
      

# Set GPIO pins
GPIO.setwarnings(False)
cs1, cs2 = 17, 22  
GPIO.setup(cs1, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(cs2, GPIO.OUT)
GPIO.setmode(GPIO.BCM)


# Initialize the ADXL345
def initadxl345():

    # Set data rate (accrate=15 -> 3200 Hz, 14=1600 Hz, 13=800 Hz, 12=400 Hz, 11=200 Hz, 10=100 Hz etc.)
    spi.xfer2([44, accrate])

    # Enable full range (10 bits resolution) and +/- 16g 4 LSB
    spi.xfer2([49, accres])

# Read the ADXL x-y-z axia
def readadxl345():
    rx = spi.xfer2([242, 0, 0, 0, 0, 0, 0])

    out = [rx[1] | (rx[2] << 8), rx[3] | (rx[4] << 8), rx[5] | (rx[6] << 8)]
    # Format x-axis
    if (out[0] & (1<<16 - 1 )):
        out[0] = out[0] - (1<<16)
    # Format y-axis
    if (out[1] & (1<<16 - 1 )):
        out[1] = out[1] - (1<<16)
    # Format z-axis
    if (out[2] & (1<<16 - 1 )):
        out[2] = out[2] - (1<<16)

    return out

# Initialize the ADXL345 accelerometer
initadxl345()

timeout = 0.0003125 / 2 # timeout=1/samplerate=>not sufficient measurements. Half the time is sufficient (don't know why!)

timetosend = 1

while(1):
   with open('/proc/uptime', 'r') as f: # get uptime
       uptime_start = float(f.readline().split()[0])
   uptime_last = uptime_start
   active_file_first = "10bit" + str(accres) + 'g' + '.csv'
   file = open('/var/log/sensor/' + active_file_first, 'w')
   while uptime_last < uptime_start + timetosend:

       time1 = str(datetime.datetime.now().strftime('%S.%f'))
       axia = readadxl345()

       file.write(str(axia[0])+','+str(axia[1])+','+str(axia[2])+','+time1+'\n')                   

       # Print data every "timeout" second
       elapsed = time.process_time()
       current = 0
       while(current < timeout):
       current = time.process_time() - elapsed

