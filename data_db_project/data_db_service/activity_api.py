from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from data_all_api.models import Activity
from data_all_api.serializers import ActivitySerializer


def devnull(request):
    return HttpResponse()


@api_view(['GET', ])
def get(request, activityId):
    activity = Activity.objects.get(id=int(activityId))
    serializer = ActivitySerializer(activity)
    return JsonResponse(serializer.data)


@api_view(['POST', ])
def add(request):
    serializer = ActivitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def recent(request, count):
    if count is None or int(count) <= 0:
        count = 10
    recent_activities = Activity.objects.order_by('-date')[:int(count)]
    serializer = ActivitySerializer(recent_activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def search(request):
    # TODO: use serializer to parse request data into ActivitySearchCriteria object.
    if 'fullText' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    criteria = request.data['fullText']
    results = Activity.objects.filter(alltext__contains=criteria)
    serializer = ActivitySerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
