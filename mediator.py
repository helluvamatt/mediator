#!/usr/bin/env python

import os
from log import Log

settings = "settings.json"

def inspect_media_type():
	pass

def main():
	mylog = Log(settings)

	todo, history, delta = mylog.scan_logs()
	mylog.print_logs()

if __name__ == "__main__":
	main()