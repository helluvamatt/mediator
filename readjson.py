import json

def read_json(read_file):

    from pprint import pprint

    json_data = open(read_file)
    data = json.load(json_data)
    json_data.close()

    return data