from lib import requests

usage = 'exchange [amount=1] <target-currency> | exchange [amount=1] [base-currency=CAD] to <target-currency>'

def parse(args):
    args = args[1:]
    amount = 1
    base_currency = 'CAD'
    target_currency = None
    # parse amount
    try:
        amount = float(args[0])
        args = args[1:]
    except Exception as e:
        pass

    if 'to' in args:
        try:
            target_currency = args[args.index('to') + 1]
        except Exception as e:
            pass
        try:
            base_currency = args[args.index('to') - 1]
        except Exception as e:
            pass
    else:
        try:
            target_currency = args[0]
        except Exception as e:
            pass
    if target_currency is None:
        return {
            'error': 'target currency missing'
        }
    return {
        'amount': amount,
        'base': base_currency.upper(),
        'target': target_currency.upper()
    }

def handler(params):
    sms = []
    if 'error' in params:
        # invalid, return instructions
        sms.append('Usage: %s\nError: %s.' % (usage, params['error']))
    else:
        r = requests.get('https://api.fixer.io/latest?base=%s&symbols=%s' % (params['base'], params['target']))
        original_j = r.json()
        if 'error' in original_j and 'Invalid base' in original_j['error']:
            sms.append('Usage: %s\nError: %s' % (usage, 'invalid base currency'))
        elif 'rates' not in original_j or params['target'] not in original_j['rates']:
            sms.append('Usage: %s\nError: %s' % (usage, 'invalid target currency'))
        else:
            rate = original_j['rates'][params['target']]
            sms.append('%.4f %s = %.4f %s.' % (params['amount'], params['base'], params['amount'] * rate, params['target']))

    return ' '.join(sms)