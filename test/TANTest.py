from unittest import TestCase
from unittest.mock import patch, MagicMock
from datasource.TAN import TanDataSource

testInput = [{'terminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '3 mn'}, \
{'terminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '4 mn'}, {\
'terminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '7 mn'}, {'\
terminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '8 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '11 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '13 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '16 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '18 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '21 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '23 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '26 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '28 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '31 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '33 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '36 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '38 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '41 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '46 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '43 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '48 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '51 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '53 mn'}, {'t\
erminus': 'Foch-Cathédrale', 'arret': {'codeArret': 'CDCO1'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 1, 'temps': '56 mn'}, {'t\
erminus': 'Porte de Vertou', 'arret': {'codeArret': 'CDCO2'}, 'ligne': {'numLigne': '4', 'typeLigne': 2}, 'infotrafic': False, 'sens': 2, 'temps': '58 mn'}]

class TANTest(TestCase):

	def test_updateFalse_if_noResult(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=None)
		self.assertFalse(ds.update())

	def test_updateTrue_if_webServiceResult(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=testInput)
		self.assertTrue(ds.update())

	def test_hasLine(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=testInput)
		ds.update()
		self.assertTrue(ds.hasLine('4'))
		self.assertFalse(ds.hasLine('2'))

	def test_hasDirection(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=testInput)
		ds.update()
		self.assertTrue(ds.hasDirection('4', 'Porte de Vertou'))
		self.assertFalse(ds.hasDirection('2', 'Foch-Cathédrale'))
		self.assertFalse(ds.hasDirection('4', 'Foch'))

	def test_getLines(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=testInput)
		ds.update()
		self.assertEqual(ds.getLines(), [ '4' ])

	def test_getDirections(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=testInput)
		ds.update()
		self.assertEqual(ds.getDirections('2'), [])
		self.assertEqual(sorted(ds.getDirections('4')), sorted(['Porte de Vertou', 'Foch-Cathédrale']))

	def test_getWaitTime(self):
		ds = TanDataSource('ds_id', 'CDCO')
		ds.getStationFromWebService = MagicMock(return_value=testInput)
		ds.update()

		self.assertEqual(ds.getWaitTime('2', 'Porte de Vertou'), None)
		self.assertEqual(ds.getWaitTime('4', 'Porte de Vertou'), 3)
		self.assertEqual(ds.getWaitTime('4', 'Foch-Cathédrale'), 4)
