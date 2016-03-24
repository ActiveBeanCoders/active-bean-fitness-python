from data_db_api.serializers import ActivityModelSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from data_db_service.services import activity_service
from data_all_api.serializers import ActivitySearchCriteriaSerializer


def devnull(request):
    return HttpResponse()


@api_view(['GET', ])
def get(request, doc_id):
    activity = activity_service.get(int(doc_id))
    serializer = ActivityModelSerializer(activity)
    return Response(serializer.data)


@api_view(['POST', ])
def add(request):
    # if ID is missing, assign it
    if not hasattr(request.data, 'id'):
        request.data['id'] = activity_service.next_id()

    serializer = ActivityModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def recent(request, count):
    recent_activities = activity_service.recent(count)
    serializer = ActivityModelSerializer(recent_activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def search(request):
    try:
        # get the full text search criterion
        criteria = ActivitySearchCriteriaSerializer(request.data).data

        # use the criterion to get search results
        results = activity_service.search(criteria)
        serializer = ActivityModelSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"error": "Missing key %s" % str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def max_id(request):
    return Response({'id': activity_service.max_id()}, status=status.HTTP_200_OK)

