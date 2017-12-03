import requests

usage = 'tell me a joke'

def parse(args):
    return []

def handler(params):
    r = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
    return r.json()['joke']