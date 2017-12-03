# params [location, time]
# time: now, today, tomorrow
import pytz
import requests
import datetime
import calendar

usage = 'weather [now|today|tomorrow]'

def parse(args):
    params = []
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
    return params

def handler(params):
    sms = []
    if len(params) == 0:
        # assuming get weather for 'now'
        # and return instructions
        params = ['now']
        sms.append('Usage: %s.' % usage)

    van_tz = pytz.timezone('America/Vancouver')

    dayinweek_num = datetime.datetime.now(van_tz).weekday()
    dayinweek = calendar.day_name[dayinweek_num]
    dayinweek_abbr = calendar.day_abbr[dayinweek_num]

    r = requests.get('https://www.theweathernetwork.com/api/data/cabc0308/cm')
    original_j = r.json()

    if params[0] in ['now', 'today']:
        assert('sterm' in original_j)
        j = original_j['sterm']
        assert('periods' in j)
        forecast_items = j['periods']

        item = forecast_items[0]
        assert('rain_value' in item) # : "5-10"
        assert('stperiodfortime' in item) # period of time: "Morning"
        assert('f' in item) # feel like: "5"
        sms.append('Now is %s, rain volume is %smm and you will feel %sC.' % (
            item['stperiodfortime'],
            item['rain_value'],
            item['f']))
    if params[0] == 'today':
        assert('sterm' in original_j)
        j = original_j['sterm']
        assert('periods' in j)
        forecast_items = j['periods']

        item = forecast_items[1]
        assert('rain_value' in item) # : "5-10"
        assert('stperiodfortime' in item) # period of time: "Morning"
        assert('f' in item) # feel like: "5"
        sms.append('Then is %s, rain volume is %smm and you will feel %sC.' % (
            item['stperiodfortime'],
            item['rain_value'],
            item['f']))
    if params[0] in ['tomorrow', 'tmr']:
        assert('sevendays' in original_j)
        j = original_j['sevendays']
        assert('periods' in j)
        forecast_items = j['periods']

        item = forecast_items[1]
        assert('metric_rain' in item) # : "5-10"
        assert('cdate' in item)
        assert('f' in item) # feel like: "5"
        sms.append('Tomorrow is %s, rain volume is %smm and you will feel %sC.' % (
            item['cdate'],
            item['metric_rain'],
            item['f']))
    return ' '.join(sms)