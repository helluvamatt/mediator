import json

def readJson(readFile):

	from pprint import pprint

	jsonData = open(readFile)
	data = json.load(jsonData)
	jsonData.close()

	return data