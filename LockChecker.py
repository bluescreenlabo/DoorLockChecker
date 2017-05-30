#!/usr/bin/env python
#coding: utf-8

import RPi.GPIO as GPIO
import threading
import time
import gmail
import ifttt
import checkTiming
import Settings

switchPin = 18		# input pin number

#----------------------------------------------------------------------*/
# @brief	Check Edge
#----------------------------------------------------------------------*/
def checkMail():
	tm = threading.Timer(20, checkMail)
	tm.start()
	
	Gmail = gmail.GmailClient(Settings.LOGIN_USER, Settings.LOGIN_PASS)
	
	orderMail = Gmail.getMail()
	
	subject = orderMail['subject']
	if subject != Settings.REMOTE_SUBJECT:
		return
	
	lines = orderMail['body']
	while (True):
		try:
			lines.remove("")
		except:
			break
	
	if (len(lines) != 0):
		print("Mail Command: %s" % lines[0])
		switchNew = GPIO.input(switchPin)
	
	if (lines[0] == 'check'):
		if (switchNew == 0):
			ifttt.sendTrigger("Lock")
		else:
			ifttt.sendTrigger("Unlock")
	
	elif (lines[0] == 'unlockcheck'):
		if (switchNew == 1):
			ifttt.sendTrigger("Unlock")
	


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

