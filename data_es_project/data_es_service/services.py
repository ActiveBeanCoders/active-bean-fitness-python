import threading

import elasticsearch
from data_es_api.models import ActivityEsFields
from elasticsearch_dsl import Search

from data_es_service import esclient


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class ActivityService:
    max_doc_id = -1

    def get(self, doc_id):
        try:
            activity = esclient.client.get(index='com.activebeancoders.entity', doc_type='Activity', id=doc_id)
            return activity['_source']
        except elasticsearch.exceptions.NotFoundError:
            return None

    def add(self, body_as_dict):
        if not hasattr(body_as_dict, 'id'):
            body_as_dict['id'] = self.next_id()
        response = esclient.client.index(
                index=esclient.index,
                doc_type=esclient.doc_type,
                id=body_as_dict['id'], body=body_as_dict
        )
        if 'created' in response:
            return response['created']
        return False

    def max_id(self):
        s = Search(using=esclient.client, index=esclient.index, doc_type=esclient.doc_type) \
            .sort("-%s" % ActivityEsFields.id) \
            .extra(size=1, _source='id')
        response = s.execute()
        return response.hits.hits[0]['_source']['id']

    # TODO: this is a bottleneck.  Need to get around this somehow.
    @synchronized
    def next_id(self):
        if self.max_doc_id < 0:
            self.max_doc_id = self.max_id()
        self.max_doc_id += 1
        return self.max_doc_id


activity_service = ActivityService()
