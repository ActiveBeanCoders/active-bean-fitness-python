import threading

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
    doc_type = 'ActivityEs'

    def get(self, doc_id):
        return esclient.get(doc_id=doc_id, index=self.index, doc_type=self.doc_type)

    def save(self, model):
        if not hasattr(model, 'id') or model.id is None:
            model.id = self.next_id()
        response = esclient.save(model=model, index=self.index, doc_type=self.doc_type)
        if 'created' in response:
            return response['created']
        return False

    def delete(self, doc_id):
        try:
            esclient.client.delete(index=self.index, doc_type=self.doc_type, id=doc_id)
            return True
        except Exception:
            return False

    def max_id(self):
        try:
            s = Search(using=esclient.client, index=self.index, doc_type=self.doc_type) \
                .sort("-%s" % ActivityEsFields.id) \
                .extra(size=1, _source='id')
            response = s.execute()
            return response.hits.hits[0]['_source']['id']
        except IndexError:
            return 1

    # TODO: this is a bottleneck.  Need to get around this somehow.
    @synchronized
    def next_id(self):
        if self.max_doc_id < 0:
            self.max_doc_id = self.max_id()
        self.max_doc_id += 1
        return self.max_doc_id


activity_service = ActivityService()
