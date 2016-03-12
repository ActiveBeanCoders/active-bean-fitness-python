from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections

index = "com.activebeancoders.entity"
doc_type = "Activity"
connections.connections.create_connection(hosts=['localhost'], timeout=20)
client = Elasticsearch()

