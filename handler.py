# import services here

import sys
sys.path = ['lib'] + sys.path

import re
from services import weather

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

    args = re.split('\s', sms.lower())

    if len(args) == 0:
        exit('gg')

    service = args[0]
    if len(args) == 1:
        return service, params

    if service == 'weather':
        if len(args) == 2:
            if args[1] in ['now', 'today', 'tomorrow', 'tml']:
                params = args[1:]
        elif len(args) == 3:
            if args[1] == 'vancouver':
                params.append(args[1])
            else:
                # FIXME: HACK: if location unsupported, always use vancouver
                params.append('vancouver')
            if args[2] in ['now', 'today', 'tomorrow', 'tml']:
                params.append(args[2])
            else:
                # Agreed that time is now if not specified
                params.append('now')
            
    return service, params

def main(sms):
    service, params = parser(sms)
    if service == 'weather':
        weather.handler(params)

def test_weather():
	print(weather.handler(['today']))
	print(weather.handler(['now']))
	print(weather.handler(['tmr']))
	print(weather.handler(['tomorrow']))
	print(weather.handler([]))
