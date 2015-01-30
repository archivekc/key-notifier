from datasource import RawDataSource
import http.client
import xml.etree.ElementTree
import re

class SNCFDataSource(RawDataSource):
	""" Data source that request and store depart time for the next train.
		use the http://www.gares-en-mouvement.com/ website. """

	def __init__(self, id, station_id, destination):
		""" station_id: train station id, destination: train destination (tableau) """
		super(SNCFDataSource, self).__init__(id)
		self.station_id = station_id
		self.destination = destination
		self.host = 'www.gares-en-mouvement.com'
		self.webserviceurl = 'http://www.gares-en-mouvement.com/fr/%s/horaires-temps-reel/dep/'
		# information is a time of depart plus possible information
		self.result = None

	def getWaitTimeAndInfo(self):
		""" Request Tan webservice and return response as an object,
			if requesting failed return None. """
		conn = http.client.HTTPConnection(self.host)
		conn.request('GET', self.webserviceurl % self.station_id)
		response = conn.getresponse()
		if response.status == 200:
			text = response.read()
		if not response.closed:
			response.close()
		conn.close()
		match = re.findall('(<tbody>.*</tbody>)', text.decode(), re.DOTALL | re.U)
		if match:
			return self.extractFirstTime(match[0])
		return None

	def extractFirstTime(self, tbody):
		cur_hour = None
		cur_dest = None
		cur_info = None
		for line in tbody.split('\n'):
			if re.findall('(<tr)', line):
				cur_hour = None
				cur_dest = None
				cur_info = None
			match_hour = re.findall('td\s*class="tvs_td_heure"[^>]*>([^<]*)<abbr[^>]*>([^<]*)</abbr>([^<]*)</td>', line)
			if match_hour:
				cur_hour = match_hour[0][0] + match_hour[0][1] + match_hour[0][2]
			match_dest = re.findall('td\s*class="tvs_td_originedestination"[^>]*>(.*)</td>', line)
			if match_dest:
				cur_dest = match_dest[0]
			match_info = re.findall('td\s*class="tvs_td_situation"[^>]*>(.*)</td>', line)
			if match_info:
				match2 = re.findall('Retard\s*:\s*(\d+).*', match_info[0])
				if match2:
					cur_info = match2[0]
			if cur_hour and cur_dest and cur_dest in self.destination:
				return (cur_hour, cur_dest, cur_info)
			if re.findall('(</tr>)', line):
				cur_hour = None
				cur_dest = None
				cur_info = None
		return None

	def update(self):
		res = self.getWaitTimeAndInfo()
		if res and self.result != res:
			self.result = res
			return True
		return False

	def getValue(self):
		value = self.result[1][:4] + ": " + self.result[0]
		if self.result[2]:
			value = value + ' R: ' + self.result[2]
		return value
