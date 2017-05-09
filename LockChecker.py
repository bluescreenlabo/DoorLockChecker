#!/usr/bin/env python
#coding: utf-8

import RPi.GPIO as GPIO
import threading
import time
import gmail
import ifttt
import checkTiming

switchPin = 18		# input pin number

#----------------------------------------------------------------------*/
# @brief	Check Edge
#----------------------------------------------------------------------*/
def checkMail():
	orderMail = gmail.check()
	if (orderMail[0] != 'none'):
		print("Mail Command: %s" % orderMail[0])
		switchNew = GPIO.input(switchPin)
	
	if (orderMail[0] == 'check'):
		if (switchNew == 0):
			ifttt.sendTrigger("Lock")
		else:
			ifttt.sendTrigger("Unlock")
	
	elif (orderMail[0] == 'unlockcheck'):
		if (switchNew == 1):
			ifttt.sendTrigger("Unlock")
	
	tm = threading.Timer(15, checkMail)
	tm.start()


#----------------------------------------------------------------------*/
# @brief	Check Edge
#----------------------------------------------------------------------*/
def checkMain():
	tc = threading.Timer(1, checkMain)
	tc.start()
	
	switchNew = GPIO.input(switchPin)
	
	if (c.isEdge(switchNew) == 1):
		if (switchNew == 0):
			ifttt.sendTrigger("Locked")
		else:
			ifttt.sendTrigger("Unlocked")
		
	else:
		if (c.isOpen(switchNew) == 1):
			ifttt.sendTrigger("Unlock")


#----------------------------------------------------------------------*/
# @brief	èâä˙âª
#----------------------------------------------------------------------*/
if __name__=='__main__':
	GPIO.setmode(GPIO.BCM)			# GPIO.BCM:GPIO number select / GPIO.BOARD:Board pin number select
	GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # set to input
	
	c = checkTiming.checkTiming(3000)
	tc = threading.Thread(target=checkMain)
	tc.start()
	
	time.sleep(0.5)
	
	tm = threading.Thread(target=checkMail)
	tm.start()

