from datetime import datetime

from data_db_api.models import ActivityModel
from django.apps import apps
from django.test import TestCase

from data_db_service.services import activity_service

unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
for m in unmanaged_models:
    m._meta.managed = True


class ActivityServiceTestCase(TestCase):
    def test_save_get_delete(self):
        activity_service.save(ActivityModel(id=1, userId=1, comment="hello world"))
        activity = activity_service.get(1)
        self.assertIsNotNone(activity)
        self.assertEqual(1, activity.id)
        self.assertEqual("hello world", activity.comment)

    def test_recent(self):
        activity_service.save(ActivityModel(id=1, userId=1, date=datetime(2016, 1, 1)))
        activity_service.save(ActivityModel(id=2, userId=1, date=datetime(2016, 3, 1)))
        activity_service.save(ActivityModel(id=3, userId=1, date=datetime(2016, 2, 1)))
        activities = activity_service.recent(10)
        self.assertIsNotNone(activities)
        self.assertEqual(2, activities[0].id)
        self.assertEqual(3, activities[1].id)
        self.assertEqual(1, activities[2].id)

    def test_search(self):
        activity_service.save(ActivityModel(id=1, userId=1, comment="hi"))
        activity_service.save(ActivityModel(id=2, userId=1, comment="bye"))
        activities = activity_service.search({"simple_criteria": {"fullText": "hi"}})
        self.assertIsNotNone(activities)
        self.assertEqual(1, len(activities))
        self.assertEqual("hi", activities[0].comment)

    def test_max_id(self):
        self.assertEqual(0, activity_service.max_id())
        activity_service.save(ActivityModel(id=1, userId=1, comment="hi"))
        self.assertEqual(1, activity_service.max_id())

    def test_next_id(self):
        self.assertEqual(1, activity_service.next_id())
        activity_service.save(ActivityModel(id=1, userId=1, comment="hi"))
        self.assertEqual(2, activity_service.next_id())
