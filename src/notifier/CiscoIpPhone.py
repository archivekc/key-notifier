from threading import Thread
from PIL import Image, ImageFont, ImageDraw
from http.server import BaseHTTPRequestHandler, HTTPServer
from datasource import FilterListener
import http.client
import urllib.request
import os
import logging
import random

# FIXME this not covered by Unit test
class CiscoIpPhoneBackgroundServer(BaseHTTPRequestHandler):
	""" Http handler that serve cisco phone with their background """

	BACKGROUND_DIR = '.'

	def __init__(self, request, client_address, server):
		super(CiscoIpPhoneBackgroundServer, self).__init__(request, client_address, server)

	def do_GET(self):
		logging.info('Receive get request')
		try:
			self.send_response(200)
			self.send_header("Content-type", "image/bmp")
			self.end_headers()
			clientId = self.path.split('/')[1]

			f = open(os.path.join(CiscoIpPhoneBackgroundServer.BACKGROUND_DIR, clientId), 'rb');
			self.wfile.write(f.read())
			f.close()
		except Exception as exp:
			logging.exception("Exception occured while serving client")
			self.send_error(404,'File Not Found')

def _startBackgroundServer(ip, port, backgroundDir):
	""" Start a background server that stay up for ever
		ip : ip the server listen
		port : port the server listen"""
	CiscoIpPhoneBackgroundServer.BACKGROUND_DIR = backgroundDir
	server = HTTPServer((ip, port), CiscoIpPhoneBackgroundServer)
	server.serve_forever()

def startBackgroundServer(ip, port, backgroundDir):
	""" To call before using any cisco notifier """
	threadHttpD = Thread(target = _startBackgroundServer,
		kwargs = {
			'ip': ip,
			'port': port,
			'backgroundDir': backgroundDir
		})
	threadHttpD.start()


class CiscoBackground:
	""" Cisco Ip phone compatible background """
	def __init__(self):
		self.image = Image.new("1", (128, 48), 1);
		self.draw = ImageDraw.Draw(self.image);
		self.font = ImageFont.truetype("resources/arial.ttf")

	def write(self, linenumber, text):
		self.draw.rectangle([0, linenumber * 10, 147, (linenumber + 1) * 10], 1, 1)
		self.draw.text((0, linenumber * 10), text, font=self.font)

	def save(self, filehandle):
		self.image.save(filehandle, "BMP")


class CiscoIpPhoneNotifier(FilterListener):
	""" Class that trigger change of Cisco Ip Phone background """

	def __init__(self, host, port, directory, notifierId):
		""" directory is path to bmp folder for client
			start http server that give background """
		self.backgroundDir = directory
		self.host = host
		self.port = port
		self.notifierId = notifierId
		self.background = CiscoBackground()
		self.lines = {}
		self.dsOutput = {}
		self.clients = []
		# Id use to make the url different every time or phone will not change background
		self.randomId = random.randint(0, 10000)

	def addClient(self, host, idUrl, idType, uri="/admin/bcisco.csc"):
		""" Add a phone to client
			uri : use /admin/bsipura.spa with old Linksys firmware """
		self.clients.append({
			'client': host,
			'idUrl': idUrl,
			'idType': idType,
			'uri': uri
		})

	def listen(self, datasourceId, lineScreen, prefix):
		""" Listen a specific datasourceId, result will be place on screen at
			line lineScreen with prefix if not null """
		self.dsOutput[datasourceId] = {
			'value': None,
			'prefix': prefix
		}
		if not lineScreen in self.lines.keys():
			self.lines[lineScreen] = []
		self.lines[lineScreen].append(datasourceId)

	# do Action on filter
	def doAction(self, rawDataSource, status):
		logging.info ('CiscoNotifier receive event from %s', rawDataSource.getId())
		change = False
		if rawDataSource.getId() in self.dsOutput:
			change = self.dsOutput[rawDataSource.getId()]['value'] != rawDataSource.getValue()
			self.dsOutput[rawDataSource.getId()]['value'] = rawDataSource.getValue()
		if change:
			self.notifyClient()

	def doFilter(self, rawDataSource, status):
		logging.info ('CiscoNotifier receive filter event on %s', rawDataSource.id)
		change = False
		if rawDataSource.getId() in self.dsOutput:
			change = self.dsOutput[rawDataSource.getId()]['value'] != None
			self.dsOutput[rawDataSource.getId()]['value'] = None
		if change:
			self.notifyClient()

	def notifyClient(self):
		""" Trigger update on all clients after creating image for all """
		# Create image
		for lineNumber in self.lines:
			dsIds = self.lines[lineNumber]
			line = ''
			for dsId in dsIds:
				dso = self.dsOutput[dsId]
				if dso['value'] != None:
					line = line + dso['prefix'] + dso['value'] + ' '
			self.background.write(lineNumber, line)
		self.background.save(os.path.join(self.backgroundDir, self.notifierId + '.bmp'))

		for distant in self.clients:
			queryPayload = urllib.parse.urlencode({
				distant['idUrl']: "http://" + self.host + ':' + str(self.port) + "/" + self.notifierId + ".bmp" + "/" + str(self.randomId),
				distant['idType']: "BMP Picture"
			})
			self.randomId = self.randomId + 1
			queryPayload = queryPayload.encode('utf-8')

			try:
				urllib.request.urlopen("http://" + distant['client'] + distant['uri'], queryPayload)
			except Exception as exp:
				logging.error("http://" + distant['client'] + distant['uri'])
				logging.exception('Exception while notify client')
