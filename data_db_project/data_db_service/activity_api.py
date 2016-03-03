import traceback

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from data_all_api.models import Activity
from data_all_api.serializers import ActivitySerializer, ActivitySearchCriteriaSerializer


def devnull(request):
    return HttpResponse()


@api_view(['GET', ])
def get(request, activityId):
    activity = Activity.objects.get(id=int(activityId))
    serializer = ActivitySerializer(activity)
    return Response(serializer.data)


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
    try:
        # get the full text search criterion
        criteria = ActivitySearchCriteriaSerializer(request.data).data
        full_text = criteria['simple_criteria']['fullText']

        # use the criterion to get search results
        results = Activity.objects.filter(alltext__contains=full_text)
        serializer = ActivitySerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"error": "Missing key %s" % str(e)}, status=status.HTTP_400_BAD_REQUEST)
