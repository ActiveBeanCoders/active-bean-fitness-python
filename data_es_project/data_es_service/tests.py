import time
from datetime import datetime

from data_all_api.models import ActivitySearchCriteria
from data_es_api.models import ActivityEs
from django.test import SimpleTestCase  # no db creation

from data_es_service.services import activity_service


def assert_index_is_empty():
    for i in range(1, 5):
        if activity_service.get(i) is not None:
            raise AssertionError("index is not empty")


class ActivityEsServiceTestCase(SimpleTestCase):
    def setUp(self):
        activity_service.index = 'com.activebeancoders.entity_test'
        activity_service.refresh = True
        for i in range(1, 5):
            activity_service.delete(i)
        assert_index_is_empty()

    def test_save_get_delete(self):
        assert_index_is_empty()
        activity_service.save(ActivityEs(id=1, user_id=1, comment="hello world"))
        activity = activity_service.get(1)
        self.assertIsNotNone(activity)
        self.assertEqual(1, activity.id)
        self.assertEqual("hello world", activity.comment)
        activity_service.delete(activity.id)
        self.assertIsNone(activity_service.get(activity.id))

    def test_recent(self):
        assert_index_is_empty()
        activity_service.save(ActivityEs(id=1, user_id=1, date=datetime(2016, 1, 1)))
        activity_service.save(ActivityEs(id=2, user_id=1, date=datetime(2016, 3, 1)))
        activity_service.save(ActivityEs(id=3, user_id=1, date=datetime(2016, 2, 1)))
        activities = activity_service.recent(10)
        self.assertIsNotNone(activities)
        self.assertEqual(2, activities[0].id)
        self.assertEqual(3, activities[1].id)
        self.assertEqual(1, activities[2].id)

    def test_search(self):
        assert_index_is_empty()
        activity_service.save(ActivityEs(id=1, user_id=1, comment="hi"))
        activity_service.save(ActivityEs(id=2, user_id=1, comment="bye"))
        criteria = ActivitySearchCriteria()
        criteria.simpleCriteria['fullText'] = "hi"
        activities = activity_service.search(criteria=criteria)
        self.assertIsNotNone(activities)
        self.assertEqual(1, len(activities))
        self.assertEqual("hi", activities[0].comment)

    def test_max_id(self):
        self.assertEqual(0, activity_service.max_id())
        activity_service.save(ActivityEs(id=1, user_id=1, comment="hi"))
        self.assertEqual(1, activity_service.max_id())

    def test_next_id(self):
        assert_index_is_empty()
        self.assertEqual(1, activity_service.next_id())
        activity_service.save(ActivityEs(id=1, user_id=1, comment="hi"))
        self.assertEqual(2, activity_service.next_id())
