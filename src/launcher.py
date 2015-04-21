import configuration
import logging
from engine import SchedulingEngine

if __name__ == '__main__':
	logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(filename='keynotifier.log', mode='a', maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
	# Init scheduling engine
	notifierEngine = SchedulingEngine()

	# Create notifier & datasource
	configuration.configure(notifierEngine)

	# Start notifier process
	notifierEngine.startScheduling()
