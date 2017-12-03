# import services here

import os
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
usage.append('Github: https://github.com/Aahung/sms-bot')
usage = '\n'.join(usage)

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")

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
    
    populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)

    r = requests.post(populated_url, dict(
        From=TWILIO_NUMBER,
        To=to,
        Body=body), auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
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
