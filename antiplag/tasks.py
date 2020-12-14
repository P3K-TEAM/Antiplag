from celery import shared_task

from .models import Result, Submission

from nlp.text_comparison import text_comparison
from nlp.elastic import Elastic


THRESHOLD = 0.15
SIMILAR_COUNT = 10


@shared_task(name="antiplag.tasks.compare_documents")
def compare_documents(submission_id):
    """
    Compare given documents against each other and N most similar documents from elastic
    """

    try:
        submission = Submission.objects.get(id=submission_id)
    except:
        return

    submission.status = Submission.SubmissionStatus.PROCESSING
    submission.save()

    documents = submission.documents.all()
    for doc in documents:
        # returns list of dictionaries
        # {
        #   "document_name": "referaty-zemegula"
        #   "text": "Co je zemegula? Je to hoax, zem je predsa plocha."
        # }
        similar_documents = Elastic.find_similar(doc.text, SIMILAR_COUNT)

        # make new list and remove current doc
        user_documents = list(documents)
        user_documents.remove(doc)

        result_similarity = 0
        compared_count = 0

        results = []
        # Compare current document with elastic docs
        for similar_doc in similar_documents:
            similarity = 0
            try:
                # returns percentage representing how similar docs are
                similarity = text_comparison(doc.text, similar_doc["text"])

                result_similarity += similarity
                compared_count += 1
            except:
                # TODO: Should uncomparable documents be included?
                similarity = None

            if similarity > THRESHOLD:
                results.append({"name": similar_doc["name"], "percentage": similarity})

        # Compare current document against user uploaded docs
        for user_doc in user_documents:
            try:
                # returns percentage representing how similar docs are
                similarity = text_comparison(doc.text, user_doc.text)

                result_similarity += similarity
                compared_count += 1
            except:
                # TODO: Should uncomparable documents be included?
                similarity = None

            results.append({"name": str(user_doc), "percentage": similarity})

        result_similarity /= compared_count
        Result.objects.create(
            document=doc, matched_docs=results, percentage=result_similarity
        )

    submission.status = Submission.SubmissionStatus.PROCESSED
    submission.save()
