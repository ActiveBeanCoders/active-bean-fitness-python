import data_es_api
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections

connections.connections.create_connection(hosts=['localhost'], timeout=20)
client = Elasticsearch()


def save(model, index, doc_type, refresh=False):
    return client.index(index=index, doc_type=doc_type, id=model.id, body=model.to_dict(), refresh=refresh)


def get(doc_id, index, doc_type):
    try:
        o = client.get(id=doc_id, index=index, doc_type=doc_type)
        class_ = getattr(data_es_api.models, doc_type)
        return class_(**o['_source'])
    except elasticsearch.exceptions.NotFoundError:
        return None
