from django.http import HttpResponse, JsonResponse
from .serializers import ActivitySerializer
from .models import Activity


def devnull(request):
    return HttpResponse()


def get(request, activityId):
    activity = Activity.objects.get(id=int(activityId))
    serializer = ActivitySerializer(activity)
    return JsonResponse(serializer.data)


def add(request):
    # TODO implement
    return HttpResponse("todo add an activity")


def recent(request, count):
    if count is None or int(count) <= 0:
        count = 10
    recent_activities = Activity.objects.order_by('-date')[:int(count)]
    serializer = ActivitySerializer(recent_activities, many=True)
    return JsonResponse(serializer.data, safe=False)


def search(request):
    # TODO implement
    return HttpResponse("todo search")
