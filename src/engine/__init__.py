import sched
import logging
import sys

def execute_single_update(schedulingEngine, datasource):
	""" Execute datasource update and listener """
	logging.info('execute update of %s', datasource.id)
	# Re schedule datasource
	schedulingEngine.getScheduler().enter(datasource.getSchedulePeriod(),
		1, execute_single_update, kwargs = {
			'schedulingEngine': schedulingEngine,
			'datasource': datasource
		})

	# Call update and then notify if needed
	try:
		if datasource.update():
			datasource.notify()
	except:
		logging.exception('Unexpected error in datasource')


# Use python scheduler for scheduling datasource
class SchedulingEngine(object):
	""" Schedule datasource for execution """

	def __init__(self):
		self.scheduler = sched.scheduler()

	def scheduleDataSource(self, datasource, period):
		""" Schedule a data source update every period, where
			period is in seconds, first exec is immediate """
		datasource.setSchedulePeriod(period)
		execute_single_update(self, datasource)

	def getScheduler(self):
		return self.scheduler

	def startScheduling(self):
		""" Create a thread that run scheduler until no more stuff to do """
		#TODO create sub class of threading that run scheduler.run() if not it take control of central thread ...
		self.scheduler.run()
