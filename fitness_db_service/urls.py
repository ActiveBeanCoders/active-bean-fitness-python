from django.conf.urls import url

from . import activity_api

urlpatterns = [
    url(r'^$', activity_api.devnull, name='devnull'),
    url(r'^api/activity/(?P<activityId>[0-9]+)/?$', activity_api.get, name='get'),
    url(r'^api/activity/add/?$', activity_api.add, name='add'),
    url(r'^api/activity/recent/(?P<count>[0-9]+)?$', activity_api.recent, name='recent'),
    url(r'^api/activity/search/$', activity_api.search, name='search'),
]
