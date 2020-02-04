# ADXL345-SPI
SPI python example for handling multiple ADXL345s on the Raspberry Pi. This code is designed to operate a maximum of 3200 Hz data sampling rate, and a minimum of 0.1 Hz. The user can designate the data acquisition rate, the g-gorce acceleration sensitivity, and also whether or not the user wants to output the data into a csv or some other delimited file. Excel compatability will be created soon. C++ code will be uploaded eventually. 
This library requires the following modules to pe installed: 

* spidev
* RPi.GPIO
* datetime

To install spidev, simply type ```pip install spidev``` in pip. To install datetime, do the same thing: ```pip install datetime```
