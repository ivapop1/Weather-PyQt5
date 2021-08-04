# weather v 1.0
import requests
import geocoder
import datetime

API_KEY = 'cf64041397ba4128f1a2426cd3e11397'
HOST  = 'https://api.openweathermap.org/data/2.5/'
DAYS = 	[
		{'num': 0 , 'title':'понедельник', 'active': False , 'color' : '#2d5664', 'order': [0,1,2,3,4,5,6], 'temp': 0, 'type': '-'},
		{'num': 1 , 'title':'вторник',     'active': False , 'color' : '#2d5664', 'order': [1,2,3,4,5,6,0], 'temp': 0, 'type': '-'},
		{'num': 2 , 'title':'среда',       'active': False , 'color' : '#2d5664', 'order': [2,3,4,5,6,0,1], 'temp': 0, 'type': '-'},
		{'num': 3 , 'title':'четверг',     'active': False , 'color' : '#2d5664', 'order': [3,4,5,6,0,1,2], 'temp': 0, 'type': '-'},
		{'num': 4 , 'title':'пятница',     'active': False , 'color' : '#2d5664', 'order': [4,5,6,0,1,2,3], 'temp': 0, 'type': '-'},
		{'num': 5 , 'title':'суббота',     'active': False , 'color' : '#d0130d', 'order': [5,6,0,1,2,3,4], 'temp': 0, 'type': '-'},
		{'num': 6 , 'title':'воскресенье', 'active': False , 'color' : '#d0130d', 'order': [6,0,1,2,3,4,5], 'temp': 0, 'type': '-'},
]

def today():
	g = geocoder.ip('me')
	city = g.city
	lat = g.lat
	lon = g.lng
	req = requests.get(f'{HOST}weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ru').json()
	res={
		'city' : req['name'],
		'dis'  : req['weather'][0]['description'],
		'temp' : int(round(req['main']['temp'])),
		'feels': str(round(req['main']['feels_like']))+ '°С',
		'pressure': str(round(req['main']['pressure'] / 1000 * 750 , 2)),
		'wind' : req['wind'],
	}
	return res
	

def week():
	today = datetime.datetime.today()
	DAYS[today.weekday()]['active'] = True
	

	for i in DAYS:
		if DAYS[today.weekday()]['active']:
			order = DAYS[today.weekday()]['order']
		g = geocoder.ip('me')
		city = g.city
		lat  = g.lat
		lon  = g.lng

		req = requests.get(f'{HOST}onecall?/exclude=daily&lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ru').json()
		res = [DAYS[i] for i in order]

		for i in req['daily']:
			index = req['daily'].index(i)
			if index ==7:
				break
			res[index]['temp'] = round(i['temp']['day'])
			res[index]['type'] = i['weather'][0]['description']

		return res



