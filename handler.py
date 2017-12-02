# import services here
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
            if args[1] == 'now' or args[1] == 'today' or args[1] == 'tomorrow' or args[1] == 'tml':
                params = args[1:]

    return service, params

def main(sms):
    service, params = parser(sms)
    if service == 'weather':
        weather.handler(params)
