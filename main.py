import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import sys
import os

buttonStat=False

def init():
    GPIO.setmode(GPIO.BCM) # set board mode to Broadcom
    ##LED SETUP
    GPIO.setup(3,GPIO.OUT,initial=GPIO.LOW) # set up pin 18
    GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(4,GPIO.RISING)
    service('OFF')

def my_gpioCallback(channel):
    global buttonStat
    start_time = time.time()
    buttonTime=0
    while GPIO.input(channel):
        if (buttonTime<=2):
            buttonTime=time.time()-start_time
        else:
            print(buttonTime)
            buttonStat=not(buttonStat and buttonStat)
            return;


def service(status):
    if status=='ON':
        print('ON')
        GPIO.output(3,1)
        os.system('sudo ifup usb0')
        os.system('sudo samba')
        GPIO.output(3,0)
        os.system('sudo ifconfig wlan0 up')
        GPIO.output(3,1)
        os.system('sudo systemctl start hostapd')
        GPIO.output(3,0)
        os.system('sudo iptables -t nat -I POSTROUTING -o usb0 -s 192.168.0.0/24 -j MASQUERADE')
        GPIO.output(3,1)

    elif status=='OFF':
        print('OFF')
        GPIO.output(3,1)
        os.system('sudo ifdown usb0')
        GPIO.output(3,0)
        os.system('sudo systemctl stop hostapd')
        GPIO.output(3,1)
        #os.system('sudo ifconfig wlan0 down')
        GPIO.output(3,0)

if __name__=="__main__":
    init()
    GPIO.add_event_callback(4,my_gpioCallback)
    temp = buttonStat
    while True:    
        if(temp!=buttonStat):
            if buttonStat==False:
                buttonStat=False
                service('OFF')
            else:
                buttonStat=True
                service('ON')
            temp=buttonStat



