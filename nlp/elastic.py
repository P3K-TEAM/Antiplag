import sys

from elasticsearch_dsl import Search, Document
from elasticsearch_dsl.query import MoreLikeThis


class Elastic(Document):
    class Index:
        name = "documents"

    @staticmethod
    def count():
        return Search(index="documents").count()

    @staticmethod
    def find_similar(document_text, similar_count):
        try:
            search = Search(index="documents").query(
                MoreLikeThis(fields=["meta", "text_preprocessed"], like=document_text)
            )

            similar_docs = [
                {
                    "name": doc.name,
                    "elastic_id": doc.meta["id"],
                    "text_preprocessed": doc.text_preprocessed,
                }
                for doc in search[:similar_count]
            ]
        except Exception as e:
            print(e, file=sys.stderr)
            return []

        return similar_docs
