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
from services import ubc_prof
from services import ubc_exam
from services import joke

services = {
    'weather': weather,
    'exchange': exchange,
    'stock': stock,
    'ubc': {
        'prof': ubc_prof,
        'exam': ubc_exam
    }
}

usage = ['Possible commands:']
for service in services:
    if 'handler' not in dir(services[service]):
        for sub_service in services[service]:
            usage.append('%s %s' % (service, sub_service))
    else:
        usage.append(service)
usage = '\n'.join(usage)

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

    try:
        service = services[serviceName]
        if 'handler' not in dir(service):
            service = service[args[1]]
        params = service.parse(args)
    except Exception as e:
        if 'joke' in ''.join(args):
            return joke, []
        raise Exception(usage)
            
    return service, params

def send_sms(to, body):
    with open('twilio-credential.json', 'r') as f:
        config = json.loads(f.read())
    r = requests.post(config['endpoint'], dict(
        From=config['number'],
        To=to,
        Body=body), auth=(config['key'], config['token']))
    return {
        'statusCode': '200',
        'body': {
            'to': to,
            'message': body
        },
        'headers': {
            'Content-Type': 'application/json',
        }
    }

def lambda_handler(event, context):
    params = parse_qs(event['body'])
    from_number = params['From'][0]
    message = params['Body'][0]
    

    try:
        service, params = parse(message)
        response = service.handler(params)
        return send_sms(from_number, response)
    except Exception as e:
        return send_sms(from_number, str(e))
