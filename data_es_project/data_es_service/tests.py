import datetime
import json
import urllib.request

import elasticsearch
from data_all_api.models import ActivitySearchCriteria
from data_es_api.models import ActivityEs
from django.test import SimpleTestCase  # no db creation
from rest_framework.test import APITestCase, APISimpleTestCase

from data_es_service import esclient
from data_es_service.services import activity_service


def assert_index_is_empty():
    for i in range(1, 5):
        if activity_service.get(i) is not None:
            raise AssertionError("index is not empty")


def pre_test():
    """Erases the Elasticsearch test index data."""
    activity_service.index = 'com.activebeancoders.entity_test'
    activity_service.refresh = True

    # re-create test index
    try:
        esclient.client.indices.delete(index=activity_service.index)
    except elasticsearch.exceptions.NotFoundError as e:
        pass
    esclient.client.indices.create(index=activity_service.index)

    # get existing mapping from non-test index
    index_name = 'com.activebeancoders.entity'
    doc_type = 'Activity'
    url = 'http://localhost:9200/' + index_name + '/' + doc_type + '/_mapping'
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    status = resp.status
    resp_content = resp.read().decode('utf8')
    resp_content = json.loads(resp_content)
    mapping = resp_content[index_name]['mappings'][doc_type]

    # create mapping
    esclient.client.indices.put_mapping(doc_type=activity_service.doc_type, index=activity_service.index, body=mapping)

    activity_service.max_doc_id = -1
    assert_index_is_empty()


class ActivityEsServiceTestCase(SimpleTestCase):
    def setUp(self):
        pre_test()

    def test_save_get_delete(self):
        activity_service.save(ActivityEs(id=1, userId=1, comment="hello world"))
        activity = activity_service.get(1)
        self.assertIsNotNone(activity)
        self.assertEqual(1, activity.id)
        self.assertEqual("hello world", activity.comment)
        activity_service.delete(activity.id)
        self.assertIsNone(activity_service.get(activity.id))

    def test_recent(self):
        activity_service.save(ActivityEs(id=1, userId=1, date=datetime.datetime(2016, 1, 1)))
        activity_service.save(ActivityEs(id=2, userId=1, date=datetime.datetime(2016, 3, 1)))
        activity_service.save(ActivityEs(id=3, userId=1, date=datetime.datetime(2016, 2, 1)))
        activities = activity_service.recent(10)
        self.assertIsNotNone(activities)
        self.assertEqual(2, activities[0].id)
        self.assertEqual(3, activities[1].id)
        self.assertEqual(1, activities[2].id)

    def test_search(self):
        activity_service.save(ActivityEs(id=1, userId=1, comment="hi"))
        activity_service.save(ActivityEs(id=2, userId=1, comment="bye"))
        criteria = ActivitySearchCriteria()
        criteria.simpleCriteria['fullText'] = "hi"
        activities = activity_service.search(criteria=criteria)
        self.assertIsNotNone(activities)
        self.assertEqual(1, len(activities))
        self.assertEqual("hi", activities[0].comment)

    def test_max_id(self):
        self.assertEqual(0, activity_service.max_id())
        activity_service.save(ActivityEs(id=1, userId=1, comment="hi"))
        self.assertEqual(1, activity_service.max_id())

    def test_next_id(self):
        self.assertEqual(1, activity_service.next_id())
        activity_service.save(ActivityEs(id=1, userId=1, comment="hi"))
        self.assertEqual(2, activity_service.next_id())


class ActivityRestApiTestCase(APISimpleTestCase):
    def setUp(self):
        pre_test()

    def test_add(self):
        data = dict(id=1, userId=1, comment="hello world")
        self.client.post('/api/activity/add', data=data, format='json')
        self.assertIsNotNone(activity_service.get(1))

    def test_recent(self):
        ids = []
        response = self.client.post('/api/activity/add', data=dict(userId=1, date=datetime.datetime(2016, 1, 1).strftime(esclient.datetime_format)), format='json')
        ids.append(response.data['id'])
        response = self.client.post('/api/activity/add', data=dict(userId=1, date=datetime.datetime(2016, 3, 1).strftime(esclient.datetime_format)), format='json')
        ids.append(response.data['id'])
        response = self.client.post('/api/activity/add', data=dict(userId=1, date=datetime.datetime(2016, 2, 1).strftime(esclient.datetime_format)), format='json')
        ids.append(response.data['id'])
        activities = self.client.get('/api/activity/recent/10')
        self.assertEqual(ids[1], activities.data[0]['id'])
        self.assertEqual(ids[2], activities.data[1]['id'])
        self.assertEqual(ids[0], activities.data[2]['id'])

    def test_search(self):
        self.client.post('/api/activity/add', data=dict(id=1, userId=1, comment="hi"), format='json')
        self.client.post('/api/activity/add', data=dict(id=2, userId=1, comment="bye"), format='json')
        data = dict(simpleCriteria=dict(fullText="hi"))
        activities = self.client.post('/api/activity/search', data=data, format='json')
        self.assertEqual(1, len(activities.data))
        self.assertEqual("hi", activities.data[0]['comment'])

    def test_maxid(self):
        maxid = self.client.get('/api/activity/maxid').data['id']
        self.assertEqual(0, maxid)
        activity_service.save(ActivityEs(id=1, userId=1, comment="hi"))
        maxid = self.client.get('/api/activity/maxid').data['id']
        self.assertEqual(1, maxid)
