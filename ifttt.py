#!/usr/bin/env python
#coding: utf-8

import requests # http request lib
import bme280
import Settings

def sendTrigger(triggerName):
	tempData = bme280.readData()
	datalist = {"value1": tempData[0], "value2": tempData[1], "value3": tempData[2]}
	reqStr = "https://maker.ifttt.com/trigger/" + triggerName + "/with/key/" + Settings.IFTTT_KEY
	requests.post(reqStr, json=datalist)
	print ('Send trigger : %s.' % triggerName)

#----------------------------------------------------------------------*/
# @brief	ƒƒCƒ“ˆ—
#----------------------------------------------------------------------*/
if __name__=='__main__':
	try:
		sendTrigger('test')
	except KeyboardInterrupt:
		pass

