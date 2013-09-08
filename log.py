from readjson import read_json

class Log:

	def __init__(self, logfile):

		self.logfile = logfile
		self.json_file = read_json(logfile)
		self.todo, self.history, self.delta = -1, -1, -1

	def scan_logs(self):

		with open(self.json_file["todo-log"]) as todo_items:
			for self.todo, n in enumerate(todo_items):
				pass

		with open(self.json_file["history-log"]) as history_items:
			for self.history, n in enumerate(history_items):
				pass

		with open(self.json_file["delta-log"]) as delta_items:
			for self.delta, n in enumerate(delta_items):
				pass
		return self.todo + 1, self.history + 1, self.delta + 1

	def print_logs(self, all=True, todo=False, history=False, delta=False):
		"""Default behavior is to print all logs;
		raise flag to print one log explicitly"""

		self.scan_logs()

		# lower all flag if and only if one specific log flag is raised
		if todo ^ history ^ delta:
			all=False

		# print one or all
		if (self.todo > -1) and (todo or all):
			print("todo.log(%s):" % (self.todo + 1))
			with open(self.json_file["todo-log"]) as todo_items:
				for torrent in todo_items:
					print torrent.strip('\n')

		if (self.history > -1) and (history or all):
			print("------\nhistory.log(%s):" % (self.history + 1))
			with open(self.json_file["history-log"]) as history_items:
				for torrent in history_items:
					print torrent.strip('\n')

		if (self.delta > -1) and (delta or all):
			print("-------\ndelta.log(%s):" % (self.delta + 1))
			with open(self.json_file["delta-log"]) as delta_items:
				for torrent in delta_items:
					print torrent.strip('\n')