# params [location, time]
# time: now, today, tomorrow
from lib import pytz
from lib import requests
import datetime
import calendar

usage = 'stock [ticker]'

def parse(args):
    params = []
    if len(args) == 2:
        params = args[1:]
    
    return params

def handler(params):
    sms = []
    if len(params) != 1:
        # cannot continue without ticker
        # return usage
        sms.append('Usage: %s.' % usage)
        return ' '.join(sms)        
    
    try:
        symbol = params[0]
        iex_baseurl = 'https://api.iextrading.com/1.0/stock/{symbol}/quote'
        res = requests.get(iex_baseurl.format(symbol=symbol))
        res_json = res.json()

        sms = 'Lastest price for {company} is ${price} ({time})'.format(
            company=res_json['companyName'],
            time=res_json['latestTime'],
            price=res_json['latestPrice'])
    except Exception as e:
        return ' '.join(['Usage: {}.'.format(usage), 'Error: Invalid stock symbol.'])

    return sms