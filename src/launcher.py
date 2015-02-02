import configuration
import logging
from engine import SchedulingEngine

if __name__ == '__main__':
	logging.basicConfig(filename='keynotifier.log',level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
	# Init scheduling engine
	notifierEngine = SchedulingEngine()

	# Create notifier & datasource
	configuration.configure(notifierEngine)

	# Start notifier process
	notifierEngine.startScheduling()
