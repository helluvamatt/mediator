import json

def read_json(readFile):

	from pprint import pprint

	jsonData = open(readFile)
	data = json.load(jsonData)
	jsonData.close()

	return data