from datetime import datetime, date, time
from unittest import TestCase
from unittest.mock import patch
from datasource import RawDataSource
from datasource.TimeFilter import HourFilter, DayFilter, MONDAY, SATURDAY

class TimeFilterTest(TestCase):
	def test_hourFilter_filterInside_timeOutside(self):
		# try mock datetime
		with patch('datasource.TimeFilter.datetime') as mock_datetime:
			mock_datetime.today.return_value = datetime(2014, 9, 8, 12, 00)
			mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

			# Test can start here
			ds = RawDataSource('ds_id')
			filter = HourFilter(ds, start=time(15, 0),
				end=time(18, 0), filteredOutside=False)
			self.assertFalse(filter.filter(ds))

	def test_hourFilter_filterInside_timeInside(self):
		# try mock datetime
		with patch('datasource.TimeFilter.datetime') as mock_datetime:
			mock_datetime.today.return_value = datetime(2014, 9, 8, 15, 30)
			mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

			# Test can start here
			ds = RawDataSource('ds_id')
			filter = HourFilter(ds, start=time(15, 0),
				end=time(18, 0), filteredOutside=False)
			self.assertTrue(filter.filter(ds))

	def test_hourFilter_filterOutside_timeOutside(self):
		# try mock datetime
		with patch('datasource.TimeFilter.datetime') as mock_datetime:
			mock_datetime.today.return_value = datetime(2014, 9, 8, 15, 30)
			mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

			# Test can start here
			ds = RawDataSource('ds_id')
			filter = HourFilter(ds, start=time(15, 0),
				end=time(16, 0), filteredOutside=True)
			self.assertFalse(filter.filter(ds))

	def test_hourFilter_filterOutside_timeInside(self):
		# try mock datetime
		with patch('datasource.TimeFilter.datetime') as mock_datetime:
			mock_datetime.today.return_value = datetime(2014, 9, 8, 11, 30)
			mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

			# Test can start here
			ds = RawDataSource('ds_id')
			filter = HourFilter(ds, start=time(15, 0),
				end=time(16, 0), filteredOutside=True)
			self.assertTrue(filter.filter(ds))


	def test_DayFilter_basicFilterWeekEnd(self):
		with patch('datasource.TimeFilter.date') as mock_date:
			mock_date.side_effect = lambda *args, **kw: datetime(*args, **kw)

			ds = RawDataSource('ds_id')
			filter = DayFilter(ds)
			# work day
			mock_date.today.return_value = date(2014, 9, 8)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 9)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 10)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 11)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 12)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 14)
			self.assertTrue(filter.filter(ds))

	def test_DayFilter_customFilter(self):
		with patch('datasource.TimeFilter.date') as mock_date:
			mock_date.side_effect = lambda *args, **kw: datetime(*args, **kw)

			ds = RawDataSource('ds_id')
			filter = DayFilter(ds, [ MONDAY, SATURDAY ])
			# work day
			mock_date.today.return_value = date(2014, 9, 8)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 13)
			self.assertFalse(filter.filter(ds))
			mock_date.today.return_value = date(2014, 9, 14)
			self.assertTrue(filter.filter(ds))

if __name__ == '__main__':
  unittest.main()
