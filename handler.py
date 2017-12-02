# import services here

import sys
sys.path = ['lib'] + sys.path

import re
from services import weather
import requests
import json
from urllib.parse import parse_qs

def parser(sms):
    """
    Weather Service Inputs:
        weather <location> [day]
        ex. weather vancouver now
            weather vancouver today
            weather vancouver tomorrow
    """

    service = ''
    params = []

    args = re.split('\s', sms.lower().strip())

    if len(args) == 0:
        exit('gg')

    service = args[0]
    if len(args) == 1:
        return service, params

    if service == 'weather':
        if len(args) == 2:
            if args[1] in ['now', 'today', 'tomorrow', 'tmr']:
                params = args[1:]
        elif len(args) == 3:
            if args[1] == 'vancouver':
                params.append(args[1])
            else:
                # FIXME: HACK: if location unsupported, always use vancouver
                params.append('vancouver')
            if args[2] in ['now', 'today', 'tomorrow', 'tmr']:
                params.append(args[2])
            else:
                # Agreed that time is now if not specified
                params.append('now')
            
    return service, params

def test_weather():
    print(weather.handler(['today']))
    print(weather.handler(['now']))
    print(weather.handler(['tmr']))
    print(weather.handler(['tomorrow']))
    print(weather.handler([]))

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

    service, params = parser(message)
    if service == 'weather':
        response = weather.handler(params)
        send_sms(from_number, response)