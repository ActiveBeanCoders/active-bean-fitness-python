from rest_framework import serializers
from data_all_api.models import Activity, ActivitySearchCriteria


# http://www.django-rest-framework.org/api-guide/serializers/
# TODO: format date on serialization
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id', 'activity', 'comment', 'date', 'dist_hour', 'dist_min', 'dist_sec', 'distance', 'unit',
            'user_id')


class ActivitySearchCriteriaSerializer(serializers.Serializer):
    simple_criteria = serializers.DictField()
