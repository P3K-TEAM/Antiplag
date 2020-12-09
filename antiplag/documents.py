from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Document as DocumentModel


@registry.register_document
class DocumentModelDocument(Document):
    class Index:
        # TODO: implement

        # Name of the Elasticsearch index
        name = 'documents'
        # See Elasticsearch Indices API reference for available settings
        # settings = {'number_of_shards': 1,
        #            'number_of_replicas': 0}

    class Django:
        model = DocumentModel  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = []
