#!/usr/bin/env python
#coding: utf-8

import RPi.GPIO as GPIO
import time
import requests # http request lib
import gmail
import bme280
import Settings

def sendTrigger(triggerName):
    tempData = bme280.readData
    datalist = {"key1": tempData[0], "key2": tempData[1], "key3": tempData[2]}
    reqStr = "https://maker.ifttt.com/trigger/" + triggerName + "/with/key/" + IFTTT_KEY
    
    requests.post(reqStr, json=datalist)


switchPin = 18      # input
switchBackup = 0    # for detect edge
countWait = 0
countOpen = 0

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)          # GPIO.BCM:GPIO number select / GPIO.BOARD:Board pin number select
GPIO.setup(switchPin, GPIO.IN)  # set to input

while True:
    switchNew = 0
    switchNew1 = 1
    while (switchNew != switchNew1):
        switchNew = GPIO.input(switchPin)
        time.sleep(0.01)
        switchNew1 = GPIO.input(switchPin)
    
    countWait = countWait + 1
    
    if (countWait == 10):
        countWait = 0
        orderMail = gmail.check()
        
        if (orderMail[0] == 'check'):
            print ("Mail Command: checkdoor")
            if (switchNew == 0):
                sendTrigger("Lock")
            else:
                sendTrigger("Unlock")
        
        if (orderMail[0] == 'unlockcheck'):
            print ("Mail Command: isopen")
            if (switchNew == 0):
                sendTrigger("Unlock")
    
    if( switchNew != switchBackup ):
        if (switchNew == 0):
            print ("Locked.")
            sendTrigger("Locked")
            countOpen = 0
        else:
            print ("Unlocked.")
            sendTrigger("Unocked")
        
        switchBackup = switchNew
        
    else:
        if (switchNew == 1):
            if (countOpen < 3000):
                countOpen = countOpen + 1
                if (countOpen == 3000):
                    sendTrigger("Lock")
    
    time.sleep(1)

