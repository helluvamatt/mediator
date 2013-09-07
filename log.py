#!/usr/bin/env python

import os
from readjson import read_json

class Log:

	def __init__(self, logFile):

		self.logFile = logFile
		self.jsonDb = read_json(logFile)
		self.nTodo, self.nHistory, self.nDelta = -1, -1, -1

	def scanLogs(self):

		with open(self.jsonDb["todo-log"]) as todoLog:
			for self.nTodo, n in enumerate(todoLog):
				pass

		with open(self.jsonDb["history-log"]) as historyLog:
			for self.nHistory, n in enumerate(historyLog):
				pass

		with open(self.jsonDb["delta-log"]) as deltaLog:
			for self.nDelta, n in enumerate(deltaLog):
				pass
		return self.nTodo + 1, self.nHistory + 1, self.nDelta + 1

	def printLogs(self, all=True, todo=False, history=False, delta=False):
		"""Default behavior is to print all logs;
		raise flag to print one log explicitly"""

		self.scanLogs()

		# lower all flag if and only if one specific log flag is raised
		if todo ^ history ^ delta:
			all=False

		# print one or all
		if (self.nTodo > -1) and (todo or all):
			print("todo.log(%s):" % (self.nTodo + 1))
			with open(self.jsonDb["todo-log"]) as todoLog:
				for tName in todoLog:
					print tName.strip('\n')

		if (self.nHistory > -1) and (history or all):
			print("history.log(%s):" % (self.nHistory + 1))
			with open(self.jsonDb["history-log"]) as historyLog:
				for tName in historyLog:
					print tName.strip('\n')

		if (self.nDelta > -1) and (delta or all):
			print("delta.log(%s):" % (self.nDelta + 1))
			with open(self.jsonDb["delta-log"]) as deltaLog:
				for tName in deltaLog:
					print tName.strip('\n')

mylog = Log("settings.json")

todo, history, delta = mylog.scanLogs()
mylog.printLogs()