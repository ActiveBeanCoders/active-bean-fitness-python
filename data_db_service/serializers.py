from rest_framework import serializers
from .models import Activity


# http://www.django-rest-framework.org/api-guide/serializers/
# TODO: format date on serialization
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id', 'activity', 'comment', 'date', 'dist_hour', 'dist_min', 'dist_sec', 'distance', 'unit',
            'user_id')
