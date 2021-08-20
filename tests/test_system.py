import re

import responses

STATUS_JSON = """{
  "_class" : "hudson.model.Hudson",
  "assignedLabels" : [
    {
      "name" : "master"
    }
  ],
  "mode" : "NORMAL",
  "nodeDescription" : "the master Jenkins node",
  "nodeName" : "",
  "numExecutors" : 2,
  "description" : null,
  "jobs" : [
    {
      "_class" : "hudson.model.FreeStyleProject",
      "name" : "jobbb",
      "url" : "http://localhost:8080/job/jobbb/",
      "color" : "blue"
    },
    {
      "_class" : "com.cloudbees.hudson.plugins.folder.Folder",
      "name" : "teest_folder",
      "url" : "http://localhost:8080/job/teest_folder/"
    }
  ],
  "overallLoad" : {

  },
  "primaryView" : {
    "_class" : "hudson.model.AllView",
    "name" : "all",
    "url" : "http://localhost:8080/"
  },
  "quietDownReason" : null,
  "quietingDown" : false,
  "slaveAgentPort" : 50000,
  "unlabeledLoad" : {
    "_class" : "jenkins.model.UnlabeledLoadStatistics"
  },
  "url" : "http://localhost:8080/",
  "useCrumbs" : true,
  "useSecurity" : true,
  "views" : [
    {
      "_class" : "hudson.model.AllView",
      "name" : "all",
      "url" : "http://localhost:8080/"
    },
    {
      "_class" : "hudson.model.ListView",
      "name" : "test2",
      "url" : "http://localhost:8080/view/test2/"
    }
  ]
}
"""


@responses.activate
def test_get_status(client):
    responses.add(
        responses.GET,
        re.compile(r'.+/api/json'),
        content_type='application/json;charset=utf-8',
        body=STATUS_JSON
    )

    status = client.system.get_status()
    assert status['quietingDown'] is False


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.+/'),
        headers={'X-Jenkins': '2.0.129'}
    )

    version = client.system.get_version()
    assert version.major == 2
    assert version.minor == 0
    assert version.patch == 129


@responses.activate
def test_is_ready(client):
    responses.add(
        responses.GET,
        re.compile(r'.+/api/json'),
        content_type='application/json;charset=utf-8',
        body=STATUS_JSON
    )

    ready = client.system.is_ready()
    assert ready is True


@responses.activate
def test_quiet_down(client):
    responses.add(
        responses.POST,
        re.compile(r'.+/quietDown'),
    )

    client.system.quiet_down()