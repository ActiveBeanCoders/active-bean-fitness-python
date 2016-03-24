from datetime import datetime

from data_db_api.models import ActivityModel
from django.apps import apps
from django.test import TestCase
from rest_framework.test import APITestCase

from data_db_service.services import activity_service

# noinspection PyProtectedMember
unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
for m in unmanaged_models:
    # noinspection PyProtectedMember
    m._meta.managed = True


class ActivityServiceTestCase(TestCase):
    def setUp(self):
        activity_service.max_doc_id = -1

    def test_save_get(self):
        activity_service.save(ActivityModel(id=1, user_id=1, comment="hello world"))
        activity = activity_service.get(1)
        self.assertIsNotNone(activity)
        self.assertEqual(1, activity.id)
        self.assertEqual("hello world", activity.comment)

    def test_recent(self):
        activity_service.save(ActivityModel(id=1, user_id=1, date=datetime(2016, 1, 1)))
        activity_service.save(ActivityModel(id=2, user_id=1, date=datetime(2016, 3, 1)))
        activity_service.save(ActivityModel(id=3, user_id=1, date=datetime(2016, 2, 1)))
        activities = activity_service.recent(10)
        self.assertIsNotNone(activities)
        self.assertEqual(2, activities[0].id)
        self.assertEqual(3, activities[1].id)
        self.assertEqual(1, activities[2].id)

    def test_search(self):
        activity_service.save(ActivityModel(id=1, user_id=1, comment="hi"))
        activity_service.save(ActivityModel(id=2, user_id=1, comment="bye"))
        activities = activity_service.search({"simpleCriteria": {"fullText": "hi"}})
        self.assertIsNotNone(activities)
        self.assertEqual(1, len(activities))
        self.assertEqual("hi", activities[0].comment)

    def test_max_id(self):
        self.assertEqual(0, activity_service.max_id())
        activity_service.save(ActivityModel(id=1, user_id=1, comment="hi"))
        self.assertEqual(1, activity_service.max_id())

    def test_next_id(self):
        self.assertEqual(1, activity_service.next_id())
        activity_service.save(ActivityModel(id=1, user_id=1, comment="hi"))
        self.assertEqual(2, activity_service.next_id())


class ActivityRestApiTestCase(APITestCase):
    def setUp(self):
        ActivityModel.objects.all().delete()
        activity_service.max_doc_id = -1

    def test_add(self):
        self.assertEqual(0, ActivityModel.objects.count())
        data = dict(id=1, user_id=1, comment="hello world")
        self.client.post('/api/activity/add', data=data, format='json')
        self.assertEqual(1, ActivityModel.objects.count())

    def test_recent(self):
        ids = []
        response = self.client.post('/api/activity/add', data=dict(user_id=1, date=datetime(2016, 1, 1)), format='json')
        ids.append(response.data['id'])
        response = self.client.post('/api/activity/add', data=dict(user_id=1, date=datetime(2016, 3, 1)), format='json')
        ids.append(response.data['id'])
        response = self.client.post('/api/activity/add', data=dict(user_id=1, date=datetime(2016, 2, 1)), format='json')
        ids.append(response.data['id'])
        activities = self.client.get('/api/activity/recent/10')
        self.assertEqual(ids[1], activities.data[0]['id'])
        self.assertEqual(ids[2], activities.data[1]['id'])
        self.assertEqual(ids[0], activities.data[2]['id'])

    def test_search(self):
        self.client.post('/api/activity/add', data=dict(id=1, user_id=1, comment="hi"), format='json')
        self.client.post('/api/activity/add', data=dict(id=2, user_id=1, comment="bye"), format='json')
        data = dict(simpleCriteria=dict(fullText="hi"))
        activities = self.client.post('/api/activity/search', data=data, format='json')
        self.assertEqual(1, len(activities.data))
        self.assertEqual("hi", activities.data[0]['comment'])

    def test_maxid(self):
        maxid = self.client.get('/api/activity/maxid').data['id']
        self.assertEqual(0, maxid)
        activity_service.save(ActivityModel(id=1, user_id=1, comment="hi"))
        maxid = self.client.get('/api/activity/maxid').data['id']
        self.assertEqual(1, maxid)

