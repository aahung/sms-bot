import unittest

from handler import *

class TestCase(unittest.TestCase):
    def test_weather(self):
        self.assertTrue('C' in weather.handler(['today']))
        self.assertTrue('C' in weather.handler(['now']))
        self.assertTrue('C' in weather.handler(['tmr']))
        self.assertTrue('C' in weather.handler(['tomorrow']))
        self.assertTrue('Usage' in weather.handler([]))

    def test_stock(self):
        self.assertTrue('Apple Inc.' in stock.handler(['aapl']))
        self.assertTrue('Facebook Inc.' in stock.handler(['fb']))
        self.assertTrue('Microsoft' in stock.handler(['msfg']))
        self.assertTrue('Usage' in weather.handler([]))

    def test_parse(self):
        self.assertTrue(parse('weather')[0] == 'weather')
        self.assertTrue(parse('weather   ')[0] == 'weather')
        self.assertTrue(parse('  weather   ')[0] == 'weather')
        try:
            parse('asdhaksljd')
            self.fail()
        except Exception as e:
            self.assertTrue(usage == str(e))

if __name__ == '__main__':
    unittest.main()