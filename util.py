import json


def fetch_conceptarium():
    conceptarium = json.load(open('data/dummy.json'))
    return conceptarium