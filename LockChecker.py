#!/usr/bin/env python
#coding: utf-8

import RPi.GPIO as GPIO
import threading
import gmail
import ifttt
import checkTiming

switchPin = 18		# input pin number

#----------------------------------------------------------------------*/
# @brief	ÉÅÉCÉìèàóù
#----------------------------------------------------------------------*/
def checkMain():
	t = threading.Timer(1, checkMain)
	t.start()
	
	switchNew = GPIO.input(switchPin)
	
	if (c.checkMail() == 1):
		orderMail = gmail.check()
		if (orderMail[0] == 'check'):
			print("Mail Command: %s" % orderMail[0])
			if (switchNew == 0):
				ifttt.sendTrigger("Lock")
			else:
				ifttt.sendTrigger("Unlock")
		
		if (orderMail[0] == 'unlockcheck'):
			print("Mail Command: %s" % orderMail[0])
			if (switchNew == 1):
				ifttt.sendTrigger("Unlock")
	
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
	
	c = checkTiming.checkTiming(15, 3000)
	t = threading.Thread(target=checkMain)
	t.start()

