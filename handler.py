# import services here

import sys
sys.path = ['lib'] + sys.path

import re
import requests
import json

from urllib.parse import parse_qs

from services import weather
from services import exchange
from services import stock

services = {
    'weather': weather,
    'exchange': exchange,
    'stock': stock
}

usage = '''Possible commands:
%s''' % ('\n'.join([services[s].usage for s in services]),)

def parse(sms):
    """
    Weather Service Inputs:
        weather <location> [day]
        ex. weather vancouver now
            weather vancouver today
            weather vancouver tomorrow
    """

    service = None
    params = []

    args = re.split('\s', sms.lower().strip())

    if len(args) == 0:
        exit('gg')

    serviceName = args[0]

    if serviceName in services:
        service = services[serviceName]
        params = service.parse(args)
    else:
        raise Exception(usage)
            
    return service, params

def send_sms(to, body):
    with open('twilio-credential.json', 'r') as f:
        config = json.loads(f.read())
    r = requests.post(config['endpoint'], dict(
        From=config['number'],
        To=to,
        Body=body), auth=(config['key'], config['token']))

def lambda_handler(event, context):
    params = parse_qs(event['body'])
    from_number = params['From'][0]
    message = params['Body'][0]
    
    try:
        service, params = parse(message)
        response = service.handler(params)
        send_sms(from_number, response)
    except Exception as e:
        send_sms(from_number, str(e))
