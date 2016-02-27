from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', include('fitness_db_service.urls')),
]

