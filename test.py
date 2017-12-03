import unittest

from handler import *

class TestCase(unittest.TestCase):
    def test_weather(self):
        self.assertTrue(parse('weather')[0] == services['weather'])
        self.assertTrue(parse('weather   ')[0] == services['weather'])
        self.assertTrue(parse('  weather   ')[0] == services['weather'])

        self.assertTrue('C' in weather.handler(['today']))
        self.assertTrue('C' in weather.handler(['now']))
        self.assertTrue('C' in weather.handler(['tmr']))
        self.assertTrue('C' in weather.handler(['tomorrow']))
        self.assertTrue('Usage' in weather.handler([]))

    def test_stock(self):
        self.assertTrue('Apple Inc.' in stock.handler(['aapl']))
        self.assertTrue('Facebook Inc.' in stock.handler(['fb']))
        self.assertTrue('Microsoft' in stock.handler(['msft']))
        self.assertTrue('Usage' in stock.handler([]))

    def test_ubc_exam(self):
        self.assertTrue(parse('ubc exam')[0] == services['ubc']['exam'])
        self.assertTrue('CPSC304' in ubc_exam.handler(['CPsC', '304']))
        self.assertTrue('CPSC310' in ubc_exam.handler(['cPsC', '310']))
        self.assertTrue('CPSC310' in ubc_exam.handler(ubc_exam.parse(['ubc', 'exam', 'cPsC', '310'])))
        self.assertTrue('Usage' in ubc_exam.handler(['asdg']))
        self.assertTrue('Usage' in ubc_exam.handler([]))

    def test_parse(self):
        try:
            parse('asdhaksljd')
            self.fail()
        except Exception as e:
            self.assertTrue(usage == str(e))

    def test_exchange(self):
        self.assertTrue(parse('exchange')[0] == services['exchange'])
        self.assertTrue(len(exchange.parse(['exchange', 'CAD']).keys()) == 3)
        self.assertTrue(len(exchange.parse(['exchange', '1.5', 'USD']).keys()) == 3)
        self.assertTrue(exchange.parse(['exchange', '1.5', 'USD'])['target'] == 'USD')
        self.assertTrue(exchange.parse(['exchange', 'USD'])['target'] == 'USD')
        self.assertTrue(exchange.parse(['exchange', '1.5', 'USD', 'to', 'CAD'])['target'] == 'CAD')
        self.assertTrue('Usage' in exchange.handler({'error': ''}))
        self.assertTrue(' = ' in exchange.handler(exchange.parse(['exchange', 'USD'])))

    def test_ubc_prof(self):
        self.assertTrue(parse('ubc prof')[0] == services['ubc']['prof'])
        self.assertTrue('Reid Hol' in ubc_prof.handler(ubc_prof.parse(['ubc', 'prof', 'reid', 'ho'])))
        self.assertTrue('phone' in ubc_prof.handler(ubc_prof.parse(['ubc', 'prof', 'reid', 'ho'])))
        self.assertTrue('phone' in ubc_prof.handler(ubc_prof.parse(['ubc', 'prof', 'carol', 'jaeger'])))
        self.assertTrue('narrow' in ubc_prof.handler(ubc_prof.parse(['ubc', 'prof', 'reid'])))

    def test_joke(self):
        self.assertTrue(parse('tell me a joke')[0] == joke)
        self.assertTrue(parse('jokes?')[0] == joke)
        self.assertTrue(parse('any jokes?')[0] == joke)


if __name__ == '__main__':
    unittest.main()