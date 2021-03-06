#!/usr/bin/env python
#coding: utf-8

class checkTiming:
	def __init__(self, checkOpen=3000):
		self.switchBackup = 0	# for detect edge
		self.countOpen = 0
		self.checkOpen = checkOpen
	
	def isEdge(self, new):
		ret = 0
		if (new != self.switchBackup):
			self.countOpen = 0
			ret = 1
			self.switchBackup = new
		return ret
	
	def isOpen(self, new):
		ret = 0
		if (new == 1):
			if (self.countOpen < self.checkOpen):
				self.countOpen = self.countOpen + 1
				if (self.countOpen == self.checkOpen):
					ret = 1
		return ret