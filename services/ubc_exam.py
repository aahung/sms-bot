import requests
from bs4 import BeautifulSoup

usage = 'ubc exam <dept> <course#>'

def parse(args):
    params = []
    if len(args) == 4:
        params = args[2:]
    
    return params

def handler(params):
    sms = []
    if len(params) != 2:
        # cannot continue without ticker
        # return usage
        sms.append('Usage: %s.' % usage)
        return ' '.join(sms)

    if params[0].lower() != 'cpsc':
        return 'Error: Sorry we currently only support CPSC.'
    
    try:
        sms = []
        ubcexam_base_url = 'https://students.ubc.ca/enrolment/exams/exam-schedule?department=121'
        res = requests.get(ubcexam_base_url)

        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find_all('table')[0]
        table_body = table.find_all('tbody')[0]
        rows = table_body.findAll('tr')

        for tr in rows:
            cols = tr.findAll('td')

            course_code = cols[0].text.strip()[0:7]
            exam_time = cols[1].text.strip()
            location = cols[2].text.strip()
            alpha = cols[3].text.strip()
            notes = cols[4].text.strip()
            if (params[0] + params[1]).lower() == course_code.lower():
                sms.append('{} \ {} \ {} \ {} \ {}'.format(cols[0].text.strip(), 
                    exam_time, location, alpha if alpha else '(none)', notes if notes else '(none)'))
    except Exception as e:
        return ' '.join(
            ['Usage: {}.'.format(usage), 'Error: Something went wrong in your request.'])

    if len(sms) == 0:
        return 'Oops, we couldn\'t find the course you\'re looking for.'

    return '\n'.join(sms)
