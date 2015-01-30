import configuration
from engine import SchedulingEngine

if __name__ == '__main__':
	# Init scheduling engine
	notifierEngine = SchedulingEngine()

	# Create notifier & datasource
	configuration.configure(notifierEngine)

	# Start notifier process
	notifierEngine.startScheduling()
