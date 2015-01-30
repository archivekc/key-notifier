class Listener(object):
  """ Datasource Listener, doAction is called after every successful
      datasource update
  """

  def doAction(self, rawDataSource):
    """ Called every time a datasource that have this listener succeed
      a update call """
    pass

class FilterListener(Listener):
  """ Listener on filtering, doFilter is called when dataSource result is
    filtered
  """

  def doFilter(self, rawDataSource):
    pass

class DataSource(object):
  """ Data source are data provider that notify listener.
  """

  def __init__(self):
    self.listeners = list()

  def register(self, listener):
    """ Register a listener, will be called every time update return True. """
    self.listeners.append(listener);

  def notify(self):
    """ Notify all listener """
    for listener in self.listeners:
      listener.doAction(self)



class RawDataSource(DataSource):
  """ Raw datasource are used for fetching data from remote services.
        They automatically hooks them to ThreadExecutor that will run the update
      method in a specific thread. After update, if it returns True, notify is
      called. It will called doAction(RawDataSource) on all listener.
  """

  def __init__(self, id):
    super(RawDataSource, self).__init__();
    self.schedulePeriod = 60
    self.id = id

  def setSchedulePeriod(self, schedulePeriodSeconds):
    """ Allow to change schedule period time for datasource,
      this method is at least call once when you schedule a RawDataSource,
      in ScheduleEngine. Can be use to change it afterwards """
    self.schedulePeriod = schedulePeriodSeconds

  def getSchedulePeriod(self):
    return self.schedulePeriod

  def update(self):
    """ Called by Thread executor, if it returns True, listener are called. """
    return False

  def getId(self):
    return self.id

  def getValue(self):
    """ Generic get value, use by datasource to communicate simple value,
      use by some notifier """
    return None

class FilterDataSource(DataSource, FilterListener):
  """ Filter dataSource are specific data source that do not request remote
    service but instead register as listener of raw data source in order to
    filter times that you want to be notify. For exemple, will filter all
    success update on Sunday
  """

  def __init__(self, filteredDataSource):
    super(FilterDataSource, self).__init__()
    filteredDataSource.register(self)

  def doAction(self, filteredDataSource):
    if not self.filter(filteredDataSource):
      self.notify(filteredDataSource)
    else:
      self.notifyFiltered(filteredDataSource)

  def doFilter(self, rawDataSource):
    self.notifyFiltered(rawDataSource)

  def notifyFiltered(self, rawDataSource):
    for listener in self.listeners:
      if isinstance(listener, FilterListener):
        listener.doFilter(rawDataSource)

  def notify(self, rawDataSource):
    """ Notify all listener """
    for listener in self.listeners:
      listener.doAction(rawDataSource)

  def filter(self, dataSource):
    """ return True and listeners will not be notify even if raw datasource
      update succeed.
    """
    pass
