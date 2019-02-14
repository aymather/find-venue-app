import json
import requests
import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

global google_api_key
global foursquare_client_id
global foursquare_client_secret

google_api_key = 'AIzaSyBmiXsVShDivS354XN3fPJyCFIWsuY_csc'
foursquare_client_id = 'NM35JXFOY3GKAXAW21EV5QGL5IZFN4WWXSHW4V44A5G5WFLN'
foursquare_client_secret = 'DVHR0KU2AHCVHBBUZITR5YGRRTWNIBBOUHJRNQYMH1OIHWMQ'


def getData(url,params):
	response = requests.get(url=url,params=params)
	data = json.loads(response.text)
	return data


def getGeocodeLocation(queryString):
	location = queryString.replace(' ', '+')
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(location,google_api_key)
	params = dict(address=location,key=google_api_key)
	result = getData(url, params)
	latitude = result['results'][0]['geometry']['location']['lat']
	longitude = result['results'][0]['geometry']['location']['lng']
	return latitude, longitude


def get4SquareVenue(lat, lon, venueType):

	# Construct url for 4square and make request
	url = 'https://api.foursquare.com/v2/venues/explore'
	params = dict(client_id = foursquare_client_id,
				  client_secret = foursquare_client_secret,
				  v = '20180323',
				  ll = '{},{}'.format(lat,lon),
				  query = venueType,
				  limit = 1)
	data = getData(url, params)

	# Extract data
	name = data['response']['groups'][0]['items'][0]['venue']['name'] # venue name
	address = data['response']['groups'][0]['items'][0]['venue']['location']['formattedAddress'][0] # venue address
	imagenum = data['response']['groups'][0]['items'][0]['venue']['photos']['count'] # number of venue photos
	loc_id = data['response']['groups'][0]['items'][0]['venue']['id'] # venue id

	# Construct url for venue photos and make request
	venue_url_img = 'https://api.foursquare.com/v2/venues/{}/photos'.format(loc_id)
	params = dict(client_id = foursquare_client_id, client_secret = foursquare_client_secret, v = 20150603)
	result = getData(venue_url_img, params)

	# Grab the first image
	if result['response']['photos']['items']:
		firstpic = result['response']['photos']['items'][0]
		prefix = firstpic['prefix']
		suffix = firstpic['suffix']
		imageURL = prefix + "300x300" + suffix
	else:
		#6.  if no image available, insert default image url
		imageURL = "https://picsum.photos/200/300"

	info = dict(name = name,
				address = address,
				imageURL = imageURL)

	print u"Why don't you try {}!".format(info['name'])
	print u"It's located at {}".format(info['address'])
	print u"Want a preview? Check them out with this link! {}".format(info['imageURL'])

	return info


def findARestaurant(obj):
	data = []
	for item in obj:
		lat, lng = getGeocodeLocation(item['Location'])
		info = get4SquareVenue(lat, lng, item['Food'])
		data.append(info)

	return data


if __name__ == '__main__':

	obj = [
			{'Location':'Tokyo, Japan',
			 'Food':'Pizza'},
		    {'Location':'Jakarta, Indonesia',
			 'Food':'Tacos'},
			{'Location':'Maputo, Mozambique',
			 'Food':'Tapas'},
			{'Location':'Cairo, Egypt',
			 'Food':'Falafel'},
			{'Location':'Cairo, New Delhi, India',
			 'Food':'Spaghetti'},
			{'Location':'Geneva, Switzerland',
			 'Food':'Cappuccino'},
			{'Location':'Los Angeles, California',
			 'Food':'Sushi'},
			{'Location':'La Paz, Bolivia',
			 'Food':'Steak'},
			{'Location':'Sydney, Australia',
			 'Food':'Gyros'},
		   ]

	data = findARestaurant(obj)