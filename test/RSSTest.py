from unittest import TestCase
from unittest.mock import patch, MagicMock
from datasource.RSS import RSSNumberOfItemDataSource

class RSSTest(TestCase):

	def test_updateFalse_if_noResult(self):
		ds = RSSNumberOfItemDataSource('ds_id', 'nowhere_url')
		ds.getRssCount = MagicMock(return_value=None)
		self.assertFalse(ds.update())

	def test_updateFalse_if_samecount(self):
		ds = RSSNumberOfItemDataSource('ds_id', 'nowhere_url')
		ds.getRssCount = MagicMock(return_value=5)
		# Set value to 5
		ds.update()
		# Check false on same value
		self.assertFalse(ds.update())

	def test_updateTrue_if_numberChange(self):
		ds = RSSNumberOfItemDataSource('ds_id', 'nowhere_url')
		ds.getRssCount = MagicMock(return_value=5)
		ds.update()
		ds.getRssCount = MagicMock(return_value=3)
		self.assertTrue(ds.update())
