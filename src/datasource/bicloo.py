from datasource import RawDataSource
import http.client
import json

class BiclooDataSource(RawDataSource):
	""" Permet de lire le nombre de velo a une station de bicloo """
	def __init__(self, id, api_key, station_id):
		super(BiclooDataSource, self).__init__(id)
		self.host = 'api.jcdecaux.com'
		self.station_req = 'https://api.jcdecaux.com/vls/v1/stations/'
		self.api_key = api_key
		self.station_id = station_id
		self.maxStands = -1
		self.availableBikes = -1

	def getStationFromWebService(self, station_id):
		station = None
		conn = http.client.HTTPSConnection(self.host)
		conn.request('GET', '%s%i?apiKey=%s&contract=Nantes' % (self.station_req, station_id, self.api_key))
		response = conn.getresponse()
		if response.status == 200:
			text = response.read()
			station = json.loads(text.decode('ASCII'))
		if not response.closed:
			response.close()
		conn.close()
		return station

	def update(self):
		""" Return true only when data changed """
		station = self.getStationFromWebService(self.station_id)
		if not station:
			return False
		else:
			if station['bike_stands'] != self.maxStands \
					or station['available_bikes'] != self.availableBikes:
				result = True
				self.maxStands = station['bike_stands']
				self.availableBikes = station['available_bikes']
			return True

	def getValue(self):
		return str(self.availableBikes) + '/' + str(self.maxStands)
