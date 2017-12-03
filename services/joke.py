import requests

usage = 'tell me a joke'

def parse(args):
    return []

def handler(params):
    r = requests.get('http://api.icndb.com/jokes/random')
    return r.json()['value']['joke']