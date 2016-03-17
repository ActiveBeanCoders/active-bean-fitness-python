from rest_framework import serializers
from data_all_api.models import Activity, ActivitySearchCriteria


# http://www.django-rest-framework.org/api-guide/serializers/
# TODO: format date on serialization
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id', 'activity', 'comment', 'date', 'distHour', 'distMin', 'distSec', 'distance', 'unit', 'userId')


class ActivitySearchCriteriaSerializer(serializers.Serializer):
    simple_criteria = serializers.DictField()
