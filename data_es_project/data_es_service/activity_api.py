from data_all_api.serializers import ActivitySearchCriteriaSerializer
from data_es_api.models import ActivityEsFields, ActivityEs
from django.http import HttpResponse
from elasticsearch_dsl import Search
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from data_es_service import esclient
from data_es_service.services import activity_service


def devnull(request):
    return HttpResponse()


@api_view(['GET', ])
def get(request, doc_id):
    activity = activity_service.get(doc_id)
    if activity is not None:
        return Response(activity.to_dict())
    else:
        return Response({}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def add(request):
    try:
        activity = ActivityEs(**request.data)
        activity_service.save(activity)
        return Response(activity_service.get(activity.id).to_dict(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
def recent(request, count):
    try:
        s = Search(using=esclient.client, index=activity_service.index, doc_type=activity_service.doc_type) \
            .sort("-%s" % ActivityEsFields.date) \
            .extra(size=count)
        response = s.execute()
        if not hasattr(response, 'hits') or not hasattr(response.hits, 'hits'):
            return Response({}, status=status.HTTP_200_OK)

        # create new array with just the model data without metadata
        results = []
        for hit in response:
            results.append(hit.to_dict())
        return Response(results, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', ])
def search(request):
    try:
        # TODO: should probably not be converting JSON -> objects -> JSON for every rest call.
        criteria = ActivitySearchCriteriaSerializer(data=request.data)
        criteria.is_valid()
        results = activity_service.search(criteria.create())
        response = []
        for hit in results:
            response.append(hit.to_dict())
        return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({'error': "Missing key %s" % str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def max_id(request):
    try:
        return Response({'id': activity_service.max_id()})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
