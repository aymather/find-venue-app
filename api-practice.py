import httplib2
import json

def getGeocodeLocation(queryString):
	api_key = 'AIzaSyBmiXsVShDivS354XN3fPJyCFIWsuY_csc'
	location = queryString.replace(' ', '+')
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(location,api_key)
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result = json.loads(response)
	return result