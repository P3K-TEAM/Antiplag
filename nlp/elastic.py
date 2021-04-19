from elasticsearch_dsl import Search, Document
from elasticsearch_dsl.query import MoreLikeThis


class Elastic:
    @staticmethod
    def count():
        return Search(index="documents").count()

    @staticmethod
    def find_similar(document_text, similar_count):
        search = Search(index="documents").query(
            MoreLikeThis(fields=["text_raw", "meta"], like=document_text)
        )

        similar_docs = [
            {"name": doc.name, "text": doc.text_raw, "id": doc.meta["id"]}
            for doc in search[:similar_count]
        ]

        return similar_docs

    @staticmethod
    def get(id):
        return Document.get(id=id, index="documents")
