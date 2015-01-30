from unittest import TestCase
from unittest.mock import patch, MagicMock
from datasource.bicloo import BiclooDataSource

inputTest = {'name': '00055-MAGELLAN', 'address': 'MAGELLAN - 11 RUE DE BELFORT', 'status': 'OPEN', 'banking': False, 'bonus': False, 'position': {'lat': 47.21078140655944,\
 'lng': -1.544298470945214}, 'available_bikes': 9, 'contract_name': 'Nantes', 'number': 55, 'available_bike_stands': 6, 'last_update': 1410348047000, 'bike_stan\
ds': 15}

class BiclooTest(TestCase):

	def test_updateFalse_if_noResult(self):
		ds = BiclooDataSource('ds_id', 'api_key', 55)
		ds.getStationFromWebService = MagicMock(return_value=None)
		self.assertFalse(ds.update())

	def test_updateTrue_if_result(self):
		ds = BiclooDataSource('ds_id', 'api_key', 55)
		ds.getStationFromWebService = MagicMock(return_value=inputTest)
		self.assertTrue(ds.update())
		self.assertEqual(9, ds.availableBikes)
		self.assertEqual(15, ds.maxStands)

	def test_result_kept_if_second_no_result(self):
		ds = BiclooDataSource('ds_id', 'api_key', 55)
		ds.getStationFromWebService = MagicMock(return_value=inputTest)
		self.assertTrue(ds.update())
		self.assertEqual(9, ds.availableBikes)
		self.assertEqual(15, ds.maxStands)
		ds.getStationFromWebService = MagicMock(return_value=None)
		self.assertFalse(ds.update())
		self.assertEqual(9, ds.availableBikes)
		self.assertEqual(15, ds.maxStands)
