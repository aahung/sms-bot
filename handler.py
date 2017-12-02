# import services here
import sys
sys.path = ['lib'] + sys.path


from services import weather

def parser(sms):
	service = ''
	params = []
	return service, params


def test_weather():
	print(weather.handler(['today']))
	print(weather.handler(['now']))
	print(weather.handler(['tmr']))
	print(weather.handler(['tomorrow']))
	print(weather.handler([]))