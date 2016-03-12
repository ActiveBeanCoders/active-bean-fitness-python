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


def activity_decoder(o):
    if '_type' in o and o['_type'] == 'Activity':
        source = o['_source']
        return Activity(o['_id'], source['activity'], source['comment'], source['date'], source['distHour'],
                        source['distMin'], source['distSec'], source['distance'], source['unit'], source['userId'])
    return o


class ActivitySearchCriteriaSerializer(serializers.Serializer):
    simple_criteria = serializers.DictField()
