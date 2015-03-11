from datasource import RawDataSource
import http.client
import xml.etree.ElementTree
import re

class SytadinDataSource(RawDataSource):
	""" Data source that request Sytadin's barometer
		use the www.sytadin.fr website. """

	def __init__(self, id):
		super(SytadinDataSource, self).__init__(id)
		self.host = 'www.sytadin.fr'
		self.webserviceurl = 'http://www.sytadin.fr/sys/barometres_de_la_circulation.jsp.html'
		self.result = None

	def getBarometer(self):
		""" Retrieve the following values :
		  * Cumul de bouchon / Niveau
		  * Cumul de bouchon / Tendance
		  * Cumul de bouchon / Distance en km
		  * Vitesse moyenne / Niveau
		  * Vitesse moyenne / Tendance
		  * Vitesse moyenne / Vitesse en km/h
		  * Congestion / Niveau
		  * Congestion / Tendance
		  * Congestion / Indice """
		cumul = None
		vitesse = None
		congestion = None
		conn = http.client.HTTPConnection(self.host)
		conn.request('GET', self.webserviceurl)
		response = conn.getresponse()
		if response.status == 200:
			text = response.read()
		if not response.closed:
			response.close()
		conn.close()
		match = re.search('Cumul de bouchon(.*?)</div>', text.decode(), re.DOTALL)
		if match:
			cumul = self.extractTriplet(match.group(1))
		match = re.search('Vitesse moyenne(.*?)</div>', text.decode(), re.DOTALL)
		if match:
			vitesse = self.extractTriplet(match.group(1))
		match = re.search('Congestion(.*?)</div>', text.decode(), re.DOTALL)
		if match:
			congestion = self.extractTriplet(match.group(1))
		return (cumul, vitesse, congestion)

	def extractTriplet(self, body):
		cur_level = None
		cur_tendency = None
		cur_value = None
		match = re.search('Niveau :.*?alt="(.*?)"', body, re.DOTALL)
		if match:
			cur_level = match.group(1)
		match = re.search('Tendance :.*?alt="(.*?)"', body, re.DOTALL)
		if match:
			cur_tendency = match.group(1)
		match = re.search('Valeur :(.*?)</span>', body, re.DOTALL)
		if match:
			cur_value = match.group(1).strip()
		return (cur_level, cur_tendency, cur_value)

	def update(self):
		res = self.getBarometer()
		""" if res and self.result != res: """
		self.result = res
		return True
		return False

	def getValue(self):
		""" Return "Indice de congestion - Niveau de congestion (Cumul de bouchon)"
		Todo : make customizable output, since we retrieve others values """
		if self.result:
			value = self.result[2][2] + " - " + self.result[2][0] + " (" + self.result[0][2] + ")"
			return value
		else:
			return None
