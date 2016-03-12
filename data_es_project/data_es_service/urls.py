from django.conf.urls import url

from . import activity_api
from data_all_api import rest_endpoints

urlpatterns = [
    url(r'^$', activity_api.devnull, name='devnull'),
    url(rest_endpoints.ACTIVITY_BY_ID, activity_api.get, name='get'),
    url(rest_endpoints.ACTIVITY_ADD, activity_api.add, name='add'),
    url(rest_endpoints.ACTIVITY_RECENT, activity_api.recent, name='recent'),
    url(rest_endpoints.ACTIVITY_SEARCH, activity_api.search, name='search'),
    url(rest_endpoints.ACTIVITY_MAX_ID, activity_api.max_id, name='max_id'),
]
