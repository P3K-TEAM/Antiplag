from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis


class Elastic:
    @staticmethod
    def find_similar(document_text, similar_count):
        search = Search(index="documents").query(
            MoreLikeThis(fields=["text_raw"], like=document_text)
        )

        similar_docs = [
            {"name": doc.name, "text": doc.text_raw} for doc in search[:similar_count]
        ]

        return similar_docs
