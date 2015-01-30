from datasource import RawDataSource
from base64 import b64encode
import http.client
import json

class JenkinsJobAggregateResultDataSource(RawDataSource):
	""" Class that fetch status of all jobs and aggregate result to OK (all ok) or KO (at least one KO).
		result is store in status variable None|True|False"""

	def __init__(self, id, host, url, username, password, jobsArray):
		""" jobsArray -> an iterable with jobs name as available on jenkins at
			http://host/jenkins/api/json?pretty=true
			url is the complete json url.
			Currently auth is used as HTTP_AUTH """
		super(JenkinsJobAggregateResultDataSource, self).__init__(id)
		self.jobs = jobsArray
		self.host = host
		self.url = url
		self.status = None
		if username and password:
			self.headers = { 'Authorization' : 'Basic %s' % b64encode(username.encode() + b':' + password.encode()).decode("ascii")}
		else:
			self.headers = None

	def getJsonData(self):
		""" request network data """
		conn = http.client.HTTPConnection(self.host)
		conn.request('GET', self.url, headers=self.headers)
		response = conn.getresponse()
		if response.status == 200:
			text = response.read()
			result = json.loads(text.decode('UTF-8'))
			if not response.closed:
					response.close()
			conn.close()
			return result
		else:
			return None

	def update(self):
		""" request jenkins and compute status """
		response = self.getJsonData()
		if not response:
			return False
		else:
			self.status = True
			for job in response['jobs']:
				if job['name'] in self.jobs and \
					not job['color'] == 'blue' and not job['color'] == 'blue_anime':
					# At least one job on the list is not blue (build success) or
					# currently being build after a build success (blue_anime)
					self.status = False
			return True

	def getValue(self):
		if self.status:
			return 'OK'
		else:
			return 'KO'
