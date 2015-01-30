from unittest import TestCase
from unittest.mock import patch, MagicMock
from datasource.jenkins import JenkinsJobAggregateResultDataSource

inputTest = {\
'assignedLabels': [\
],\
'mode': "NORMAL",\
'nodeDescription': "the master Jenkins node",\
'nodeName': "",\
'numExecutors': 3,\
'description': None,\
'jobs': [\
{\
'name': "job1",\
'url': "http://pacman-d-forge.nantes.keyconsulting.fr/jenkins/job/job1/",\
'color': "blue"\
},\
{\
'name': "job2",\
'url': "http://myurl/jenkins/job/job2/",\
'color': "yellow"\
},\
{\
'name': "job3",\
'url': "http://pacman-d-forge.nantes.keyconsulting.fr/jenkins/job/job3/",\
'color': "blue_anime"\
},\
{\
'name': "job4",\
'url': "http://pacman-d-forge.nantes.keyconsulting.fr/jenkins/job/job4/",\
'color': "yellow_anime"\
}\
],\
'overallLoad': { },\
'primaryView': {\
'name': "All",\
'url': "http://myurl/jenkins/"\
},\
'quietingDown': False,\
'slaveAgentPort': 0,\
'unlabeledLoad': { },\
'useCrumbs': False,\
'useSecurity': True,\
'views': [\
{\
'name': "All",\
'url': "http://myurl/jenkins/"\
},\
{\
'name': "myview",\
'url': "http://myurl/jenkins/view/myview/"\
}\
]\
}

class JenkinsTest(TestCase):

  def test_updateFalse_if_noResult(self):
    ds = JenkinsJobAggregateResultDataSource('ds_id', 'localhost', 'http://localhost/jenkins/api/json/', 'user', 'password', [ 'job1', 'job2' ])
    ds.getJsonData = MagicMock(return_value=None)
    self.assertFalse(ds.update())

  def test_updateTrue_if_result(self):
    ds = JenkinsJobAggregateResultDataSource('ds_id', 'localhost', 'http://localhost/jenkins/api/json/', 'user', 'password', [ 'job1', 'job2' ])
    ds.getJsonData = MagicMock(return_value=inputTest)
    self.assertTrue(ds.update())

  def test_status_true_with_blue_anime(self):
    ds = JenkinsJobAggregateResultDataSource('ds_id', 'localhost', 'http://localhost/jenkins/api/json/', 'user', 'password', [ 'job1', 'job3' ])
    ds.getJsonData = MagicMock(return_value=inputTest)
    self.assertTrue(ds.update())
    self.assertTrue(ds.status)

  def test_status_false_with_yellow_anime(self):
    ds = JenkinsJobAggregateResultDataSource('ds_id', 'localhost', 'http://localhost/jenkins/api/json/', 'user', 'password', [ 'job1', 'job4' ])
    ds.getJsonData = MagicMock(return_value=inputTest)
    self.assertTrue(ds.update())
    self.assertFalse(ds.status)

  def test_status_false_with_yellow(self):
    ds = JenkinsJobAggregateResultDataSource('ds_id', 'localhost', 'http://localhost/jenkins/api/json/', 'user', 'password', [ 'job1', 'job2' ])
    ds.getJsonData = MagicMock(return_value=inputTest)
    self.assertTrue(ds.update())
    self.assertFalse(ds.status)

  def test_status_false_with_no_blue(self):
    ds = JenkinsJobAggregateResultDataSource('ds_id', 'localhost', 'http://localhost/jenkins/api/json/', 'user', 'password', [ 'job4', 'job2' ])
    ds.getJsonData = MagicMock(return_value=inputTest)
    self.assertTrue(ds.update())
    self.assertFalse(ds.status)
