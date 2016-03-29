from rest_framework import serializers
from data_all_api.models import ActivitySearchCriteria

# http://www.django-rest-framework.org/api-guide/serializers/
# TODO: format date on serialization
from data_db_api.models import ActivityModel


class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityModel
        fields = (
            'id', 'activity', 'comment', 'date', 'distHour', 'distMin', 'distSec', 'distance', 'unit', 'userId')
