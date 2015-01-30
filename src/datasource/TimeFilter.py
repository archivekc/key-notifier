from datasource import FilterDataSource
from datetime import datetime, date, time

class HourFilter(FilterDataSource):
	""" Filter Datasource when it is not inside or outside specific time period """

	def __init__(self, dataSource, start, end, filteredOutside=True):
		""" start and end are time from datetime.time  (time(17, 30) -> 17h30)
			if filteredOutside = True -> [start, end] define not filter period
			if filteredOutside = False -> [start, end] define filter period """
		super (HourFilter, self).__init__(dataSource)
		self.filteredOutside = filteredOutside
		self.start = start
		self.end = end

	def filter(self, dataSource):
		local_hour = datetime.today().time()
		if local_hour >= self.start and local_hour <= self.end:
			# inside define period, if inside True we do not filter means result is !inside
			return not self.filteredOutside
		else:
			return self.filteredOutside

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7
WORKDAY = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]

class DayFilter(FilterDataSource):
	""" Filter Datasource when it is not during specific weekday """

	def __init__(self, dataSource, authorizeDay=WORKDAY):
		""" start and end are time from datetime.time  (time(17, 30) -> 17h30)
			if inside = True -> [start, end] define not filter period
			if inside = False -> [start, end] define filter period """
		super (DayFilter, self).__init__(dataSource)
		self.authorizeDay = authorizeDay

	def filter(self, dataSource):
		current_day = date.today().isoweekday()
		if current_day in self.authorizeDay:
			return False
		else:
			return True
