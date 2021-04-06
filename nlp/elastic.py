from django.core.cache import cache
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis


class Elastic:
    @staticmethod
    def count():
        cached_value = cache.get("corpus_size", None)
        return cached_value if cached_value else Search(index="documents").count()

    @staticmethod
    def find_similar(document_text, similar_count):
        search = Search(index="documents").query(
            MoreLikeThis(fields=["text_raw", "meta"], like=document_text)
        )

        similar_docs = [
            {"name": doc.name, "text": doc.text_raw, "elastic_id": doc.meta["id"]}
            for doc in search[:similar_count]
        ]

        return similar_docs
