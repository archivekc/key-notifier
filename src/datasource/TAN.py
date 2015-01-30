from datasource import RawDataSource
import http.client
import json

class TanDataSource(RawDataSource):
	""" Data source that request and store time for a specific station
		(Nantes public transportation system (France)),
	 	provide simple method to access specific line information. """

	def __init__(self, id, station_id):
		super(TanDataSource, self).__init__(id)
		self.station = station_id
		self.host = 'open.tan.fr'
		self.webserviceurl = 'https://open.tan.fr/ewp/tempsattente.json/'
		# lines is a dict with first level as line name/number, snd direction,
		# value is time to wait
		self.lines = dict()

	def getStationFromWebService(self):
		""" Request Tan webservice and return response as an object,
		 	if requesting failed return None. """
		station = None
		conn = http.client.HTTPSConnection(self.host)
		conn.request('GET', '%s/%s' % (self.webserviceurl, self.station))
		response = conn.getresponse()
		if response.status == 200:
			text = response.read()
			station = json.loads(text.decode('UTF-8'))
		if not response.closed:
			response.close()
		conn.close()
		return station

	def update(self):
		lines = dict()
		# Request remote
		result = self.getStationFromWebService()
		if not result:
			return False
		else:
			# Extract line, and next waiting time for each direction
			for l in result:
				timing = l['temps']
				if timing == 'Close':
					timing = 0
				elif l['temps'][-2:] == 'mn':
					timing = int(l['temps'].split('mn')[0])
				if l['ligne']['numLigne'] not in lines:
					lines[l['ligne']['numLigne']] = dict()
				if l['terminus'] not in lines[l['ligne']['numLigne']] \
					or (lines[l['ligne']['numLigne']][l['terminus']] == 0	\
					or (timing != 0 and lines[l['ligne']['numLigne']][l['terminus']] > timing)):
					lines[l['ligne']['numLigne']][l['terminus']] = timing

			self.lines = lines;
			return True

	def hasLine(self, lineName):
		return lineName in self.lines

	def hasDirection(self, lineName, direction):
			if self.hasLine(lineName):
				return direction in self.lines[lineName]
			else:
				return False

	def getWaitTime(self, lineName, direction):
		""" Return None if not available """
		if self.hasDirection(lineName, direction):
			return self.lines[lineName][direction]
		else:
			return None

	def getLines(self):
		return list(self.lines.keys())

	def getDirections(self, lineName):
		if self.hasLine(lineName):
			return list(self.lines[lineName].keys())
		else:
			return list()
