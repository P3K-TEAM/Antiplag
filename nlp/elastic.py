from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis


class Elastic:
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
