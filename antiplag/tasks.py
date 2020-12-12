from celery import shared_task

from .models import Result

from nlp.text_comparison import text_comparison
from nlp.elastic import Elastic


THRESHOLD = 0.15
SIMILAR_COUNT = 10
ERROR_MESSAGE = "An error occured during similarity comparison"


@shared_task(name='antiplag.tasks.generate_result')
def compare_documents(documents):
    """
    Compare given documents against each other and N most similar documents from elastic
    """

    for doc in documents:
        # returns list of dictionaries
        # {
        #   "document_name": "referaty-zemegula"
        #   "text": "Co je zemegula? Je to hoax, zem je predsa plocha."
        # }
        similar_documents = Elastic.find_similar(doc.text, SIMILAR_COUNT)
        # make new list and remove current
        user_documents = list(documents).remove(doc)

        results = []
        # Compare current document with elastic docs
        for similar_doc in similar_documents:
            similarity = 0
            try:
                # returns percentage representing how similar docs are
                similarity = text_comparison(doc.text, similar_doc["text"])
            except:
                # Ignore document
                pass

            if similarity > THRESHOLD:
                results.append({
                    "name": similar_doc["name"],
                    "percentage": similarity
                })

        # Compare current document with user uploaded docs
        for similar_doc in user_documents:
            try:
                # returns percentage representing how similar docs are
                similarity = text_comparison(doc.text, similar_doc.text)
            except:
                similarity = {"error": ERROR_MESSAGE}

            results.append({
                "name": str(similar_doc),
                "percentage": similarity
            })

        Result(document=doc, matched_docs=results)

