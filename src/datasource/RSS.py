from datasource import RawDataSource
import urllib.request
import logging
from xml.dom import minidom, Node

class RSSNumberOfItemDataSource(RawDataSource):
	""" Simple RSS Datasource that request a rss channel and count
	the number of items. Notify only when count change """

	def __init__(self, id, url):
		""" url: URL of rss stream """
		super(RSSNumberOfItemDataSource, self).__init__(id)
		self.url = url
		self.count = None

	def getRssCount(self):
		""" Request rss stream and return count of items """
		nodeCount = None
		try:
			rssStream = urllib.request.urlopen(self.url)
			xmldoc = minidom.parse(rssStream)
			items = xmldoc.getElementsByTagName('item')
			nodeCount = len(items)
		except Exception as exp:
			logging.exception('RSS datasource update failure')

		return nodeCount

	def update(self):
		nodeCount = self.getRssCount()
		if nodeCount == None:
			return False
		result = nodeCount != self.count
		self.count = nodeCount
		return result

	def getCount(self):
		return self.count

	def getValue(self):
		return str(self.count)
