import requests
from bs4 import BeautifulSoup

usage = 'ubc prof <keywords>'

def parse(args):
    args = args[2:]
    if len(args) == 0:
        return None
    return ' '.join(args)

def printString(aText, jump):
    for i in range(98, 124):
        aText = aText.replace(chr(i), chr(i - jump))
    return aText

def handler(params):
    sms = []

    if params is None:
        sms.append('Usage: %s.' % usage)

    HOST = 'https://directory.ubc.ca/'
    r = requests.get(HOST + 'index.cfm')
    soup = BeautifulSoup(r.content, 'html.parser')
    search_form = soup.find('form', { 'id': 'CFForm_1' })
    search_action = HOST + search_form.get('action')
    keyword = params
    r = requests.post(search_action, {
            'keywords': keyword,
            'andorexactkeywords': 'start',
            'building_name': '',
            'title': '',
            'description': '',
            'address': '',
            'location': '',
            'area': '',
            'switche': '',
            'number': '',
            'local': '',
            'email': '',
            'resultsperpagestaff': 10,
            'submitAnd': 'search using exact fields'
        })
    soup = BeautifulSoup(r.content, 'html.parser')
    trs = []
    try:
        trs = soup.find('div', { 'class': 'results' }) \
                  .find('table') \
                  .find_all('tr', { 'align': 'left' })
    except Exception as e:
        pass
    if len(trs) < 1:
        sms.append('Cannot find results.')
    elif len(trs) > 1:
        names = [' '.join([eval(f.strip().replace(';', '')) for f in tr.find('td').text.strip().split('\n')]) for tr in trs]
        if len(names) > 4:
            names = names[:4]
        sms.append('Found multiple professors: [%s ..]. Please narrow down the keywords' % ' | '.join(names))
    else:
        tr = trs[0]
        name = ' '.join([eval(f.strip().replace(';', '')) for f in tr.find('td').text.strip().split('\n')])
        phone = '-'.join(tr.find_all('td')[-1].text.strip().split('\xa0')[0].split())
        sms.append('%s\'s phone number is %s.' % (name, phone))

    return ' '.join(sms)
