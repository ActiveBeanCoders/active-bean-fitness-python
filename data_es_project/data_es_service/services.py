import threading

import datetime
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
    index = 'com.activebeancoders.entity'
    doc_type = 'Activity'

    # By default, Elasticsearch flushes pending operations every 1 second.
    # We can force Elasticsearch to flush immeidately by passing the refresh=True
    # parameter to operations that modify data.
    refresh = False  # set to True for integration testing

    def get(self, doc_id):
        return esclient.get(doc_id=doc_id, index=self.index, doc_type=self.doc_type)

    def save(self, model):
        if not hasattr(model, 'id') or model.id is None:
            model.id = self.next_id()
        # http://strftime.org/
        if model.date is not None and isinstance(model.date, datetime.datetime):
            model.date = model.date.strftime(esclient.datetime_format)
        response = esclient.save(model=model, index=self.index, doc_type=self.doc_type, refresh=self.refresh)
        if 'created' in response:
            return response['created']
        return False

    def delete(self, doc_id):
        try:
            esclient.client.delete(index=self.index, doc_type=self.doc_type, id=doc_id, refresh=self.refresh)
            return True
        except Exception:
            return False

    def recent(self, count):
        s = Search(using=esclient.client, index=self.index, doc_type=self.doc_type) \
            .sort("-%s" % ActivityEsFields.date) \
            .extra(size=count)
        response = s.execute()
        if not hasattr(response, 'hits') or not hasattr(response.hits, 'hits'):
            return []

        results = []
        for hit in response:
            results.append(hit)
        return results

    def search(self, criteria):
        s = Search(using=esclient.client, index=activity_service.index, doc_type=activity_service.doc_type) \
            .query('match', _all=criteria.simpleCriteria['fullText'])
        response = s.execute()
        if not hasattr(response, 'hits') or not hasattr(response.hits, 'hits'):
            return []

        # create new array with just the model data without metadata
        results = []
        for hit in response:
            results.append(hit)
        return results

    def max_id(self):
        try:
            s = Search(using=esclient.client, index=self.index, doc_type=self.doc_type) \
                .sort("-%s" % ActivityEsFields.id) \
                .extra(size=1, _source=ActivityEsFields.id)
            response = s.execute()
            print(response)
            return response.hits.hits[0]['_source']['id']
        except IndexError:
            return 0

    # TODO: this is a bottleneck.  Need to get around this somehow.
    @synchronized
    def next_id(self):
        if self.max_doc_id < 0:
            self.max_doc_id = self.max_id()
        self.max_doc_id += 1
        return self.max_doc_id


activity_service = ActivityService()
