from data_all_api.models import Activity
from django.test import SimpleTestCase  # no db creation

from data_es_service.services import activity_service


class ActivityEsServiceTestCase(SimpleTestCase):
    def setUp(self):
        activity_service.index = 'com.activebeancoders.entity_test'
        activity_service.delete(1)

    def test_save_get_delete(self):
        self.assertIsNone(activity_service.get(1))
        activity_service.save(Activity(id=1, user_id=1, comment="hello world"))
        activity = activity_service.get(1)
        self.assertIsNotNone(activity)
        self.assertEqual(1, activity.id)
        self.assertEqual("hello world", activity.comment)
        activity_service.delete(activity.id)
        self.assertIsNone(activity_service.get(activity.id))

